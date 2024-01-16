# pip install googletrans==4.0.0rc1

import argparse
from knockknock import discord_sender
import pandas as pd

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_name", help="MaCoCu dataset_name in JSON format, extracted with 2-predict_extended.py, e.g. datasets/annotated/MaCoCu-mt-2.0.tsv-genre-annotated.jsonl")
    parser.add_argument("corpus_suffix", help="Language code for the corpus, e.g. 'mt'")
    args = parser.parse_args()

# Define the scenario
dataset_name = args.dataset_name

dataset_suffix = args.corpus_suffix

df = pd.read_json(dataset_name, orient="records", lines=True)

print("Dataset opened.\n")
print(df.head().to_markdown())
print("\nDataset size: {}".format(df.shape[0]))
print("Classes distribution:")
print(df.genre.value_counts().to_markdown())

# Get notified once the code ends
webhook_url = open("/home/tajak/Parlamint-translation/discord_key.txt", "r").read()
@discord_sender(webhook_url=webhook_url)
def extract_genre_sample(df, source_lang):
	import googletrans
	from googletrans import Translator

	# We will extract all labels, except Mix and Other
	labels_list=['Information/Explanation', 'News', 'Instruction', 'Opinion/Argumentation', 'Forum', 'Prose/Lyrical', 'Legal', 'Promotion']

	# First create the initial df to which all others in the loop will be added
	final_sample = df[df["genre"] == labels_list[0]].sample(n=10)

	# Add all other domains
	remaining_list = labels_list[1:]

	for i in remaining_list:
		try:
			added_instances = df[df["genre"] == i].sample(n=10)
			final_sample = pd.concat([final_sample, added_instances])
		except:
			print(df[df["genre"] == i][:2].to_markdown())

	# Shuffle rows
	final_sample = final_sample.sample(frac=1)

	# Discard logit information
	final_sample = final_sample.drop(columns="logit")

	# Change <p> signs to actual new lines
	final_sample["text"] = final_sample["text"].str.replace("<p>", "\n\n")

	sentence_list = final_sample["text"].to_list()

	# Apply Google Translate and machine translate the data - documentation: https://py-googletrans.readthedocs.io/en/latest/

	# Define the translation model
	translator = Translator()

	# Create the final list
	translation_GT = []

	print("Starting translation.")

	# The suffix that GT uses for all languages is the same as the suffix used in the dataset names, except for Montenegrin
	# GT does not have a special model for Montenegrin, so we will use the Serbian model
	if source_lang == "cnr":
		lang = "sr"
	else:
		lang = source_lang

	# Loop through the list of original sentences,
	# translate each and append the translation to the final list
	for i in sentence_list:
		# Translate the sentence from source language, e.g. Slovene (src = "sl") to English (dest = "en")
			current_translation = translator.translate(i, src = lang, dest='en')
		# Append the translated sentence to the final list
			translation_GT.append(current_translation.text)

	print("Translation finished.")

	# Append translations to the sample

	final_sample["translation"] = translation_GT

	# Save to JSON lines
	final_sample.to_json("/datasets/annotated/MaCoCu-{}-genre-sample.jsonl".format(source_lang), orient="records", lines=True)

	print("Final file saved as MaCoCu-{}-genre-sample.jsonl".format(source_lang))

	# Create also a version for the annotation tool, only with translation and labels
	ann_df = final_sample[["translation","genre"]]

	# For annotation, each label should be in a list
	ann_df["genre"] = ann_df["genre"].apply(lambda x:[x])

	# Rename df
	ann_df.columns = ["text", "label"]

	# Add metadata
	text_ids = final_sample["document_id"].to_list()
	#domains = final_sample["domain"].to_list()

	metadata_list = []

	for i in list(zip(text_ids)):#,domains)):
		metadata = {"text_id": i[0]}#, "domain": i[1]}
		metadata_list.append(metadata)

	ann_df["metadata"] = metadata_list

	# Save to JSON lines
	ann_df.to_json("/datasets/annotated/MaCoCu-{}-genre-sample-for-annotation-tool.jsonl".format(source_lang), orient="records", lines=True)

	print("File for annotation saved as MaCoCu-{}-genre-sample-for-annotation-tool.jsonl".format(source_lang))
	
	return final_sample

extract_genre_sample(df, dataset_suffix)