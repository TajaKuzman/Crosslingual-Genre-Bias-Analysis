from prevert import *
import re
import argparse
from knockknock import discord_sender
import pandas as pd
from transformers import AutoTokenizer
import sys
import torch
import json
from scipy.special import softmax
from transformers import AutoModelForSequenceClassification

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("suffix", help="MaCoCu suffix, e.g. 'mt-2.0' from MaCoCu-mt-2.0.xml")
    args = parser.parse_args()

suffix = args.suffix

webhook_url = open("/home/tajak/Parlamint-translation/discord_key.txt", "r").read()
@discord_sender(webhook_url=webhook_url)
def clean_mixed_texts(suffix):
	# Open the dataset with lang distr info
	df = pd.read_json(f"/cache/tajak/macocu-mt/datasets/annotated/MaCoCu-{suffix}.tsv-genre-annotated-with-lang-distr.jsonl", orient="records", lines=True)

	print(df["lang"].value_counts().to_markdown())

	# Get a list of text ids for texts that need to be reprocessed
	text_ids = df[df["lang"] == "mix"]["document_id"].to_list()
	print(f"Number of texts to reprocess: {len(text_ids)}.")
		
	# Open the original dataset
	dataset_name = f"datasets/initial/MaCoCu-{suffix}.xml"
	target_lang = suffix.split("-")[0]

	output_file_name = f'datasets/initial/MaCoCu-{suffix}-cleaned-mixed-texts.tsv'
	f = open(output_file_name,'wt')

	dset = dataset(dataset_name)

	counter_mixed = 0
	counter_final = 0

	space_re=re.compile(r'\s+',re.UNICODE)

	for doc in dset:
		text = ""
		# Take only texts that were identified to be mixed
		if doc.meta["id"] in text_ids:
			counter_mixed += 1
			for par in doc:
				# short paragraphs don't have lang metadata,
				# because they are often faulty, so we just keep them
				if par.meta.get("lang", "None") == "None":
					text += str(par)
					text += "<p>"
				# otherwise, add to text only paragraph in target language
				elif par.meta["lang"] == target_lang:
					text += str(par)
					text += "<p>"
				else:
					# skip paragraphs not in target language
					continue

			# Calculate final text length
			text_length=len(text.split())

			# Apply the same rules as before - use only texts,
			# longer than 75 words and only the first 512 words from them
			if text_length>=75:
				f.write(doc.meta['id']+'\t'+' '.join(space_re.sub(' ',text).split(' ')[:512])+'\n')
				f.flush()
				counter_final += 1
			else:
				continue

	print(f"Processing of mixed lang texts finished. Processed {counter_mixed} texts with mixed lang, kept {counter_final} texts (removed {counter_mixed-counter_final} texts).")

	print(f"Saved the processed texts in {output_file_name}")
	f.close()



# Get notified once the code ends
webhook_url = open("/home/tajak/Parlamint-translation/discord_key.txt", "r").read()
@discord_sender(webhook_url=webhook_url)
def predict_genre(suffix):
	model = AutoModelForSequenceClassification.from_pretrained("classla/xlm-roberta-base-multilingual-text-genre-classifier")
	model.to("cuda:0")

	tokenizer = AutoTokenizer.from_pretrained("classla/xlm-roberta-base-multilingual-text-genre-classifier")

	labels = ["Other", "Information/Explanation", "News", "Instruction", "Opinion/Argumentation", "Forum", "Prose/Lyrical", "Legal", "Promotion"]

	def transcode(logit):
		cats=sorted(zip(labels,softmax(logit)),key=lambda x:-x[1])
		if cats[0][1]>=0.8:
			label=cats[0][0]
		else:
			label='Mix'
		return label

	texts=[]
	dids=[]

	dataset_name = f'datasets/initial/MaCoCu-{suffix}-cleaned-mixed-texts.tsv'
	f=open(f'datasets/annotated/MaCoCu-{suffix}-mixed-texts-genre-annotated.jsonl','wt')

	for line in open(dataset_name):
		did,text=line.strip().split('\t')
		texts.append(text)
		dids.append(did)
		if len(texts)==1000:
			inputs = tokenizer(texts, max_length=512, truncation=True, padding=True, return_tensors="pt").to("cuda:0")

			from time import time
			now=time()
			with torch.no_grad():
				logits = model(**inputs).logits
				print(time()-now)
			for idx in range(len(logits)):
				current_logit = logits[idx].tolist()
				instance={'document_id':dids[idx],'text': texts[idx],'genre': transcode(current_logit),'logit':current_logit}
				f.write(json.dumps(instance)+'\n')
				f.flush()
			texts=[]
			dids=[]
	if len(texts)>0:
		inputs = tokenizer(texts, max_length=512, truncation=True, padding=True, return_tensors="pt").to("cuda:0")
		from time import time
		now=time()
		with torch.no_grad():
			logits = model(**inputs).logits
			print(time()-now)
		for idx in range(len(logits)):
			current_logit = logits[idx].tolist()
			instance={'document_id':dids[idx],'text': texts[idx],'genre': transcode(current_logit),'logit':current_logit}
			f.write(json.dumps(instance)+'\n')
			f.flush()

	f.close()
	print("Prediction finished.")

clean_mixed_texts(suffix)

predict_genre(suffix)