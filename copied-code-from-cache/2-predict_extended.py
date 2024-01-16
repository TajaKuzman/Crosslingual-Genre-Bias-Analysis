from transformers import AutoTokenizer
import sys
import torch
import json
from scipy.special import softmax
from transformers import AutoModelForSequenceClassification
import argparse
from knockknock import discord_sender

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_name", help="MaCoCu dataset_name in TSV format, extracted with select_for_xgenre.py, e.g. MaCoCu-mt-2.0.tsv")
    args = parser.parse_args()

# Define the scenario
dataset_name = args.dataset_name

# Get notified once the code ends
webhook_url = open("/home/tajak/Parlamint-translation/discord_key.txt", "r").read()
@discord_sender(webhook_url=webhook_url)
def predict_genre(dataset_name):
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

    f=open(f'datasets/annotated/{dataset_name}-genre-annotated.jsonl','wt')

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

predict_genre(dataset_name)