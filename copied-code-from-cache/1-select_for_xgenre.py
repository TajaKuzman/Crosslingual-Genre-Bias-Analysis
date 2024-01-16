from prevert import *
import re
import argparse
from knockknock import discord_sender

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_name", help="MaCoCu dataset_name, e.g. MaCoCu-mt-2.0.xml")
    args = parser.parse_args()

# Define the scenario
dataset_name = args.dataset_name

# Get notified once the code ends
webhook_url = open("/home/tajak/Parlamint-translation/discord_key.txt", "r").read()
@discord_sender(webhook_url=webhook_url)
def select_texts(dataset_name):
    space_re=re.compile(r'\s+',re.UNICODE)
    output_file_name = f'{dataset_name[:-len(".xml")]}.tsv'
    f=open(output_file_name,'w')

    for document in dataset(dataset_name):
        text_length=len(str(document).split())
        text = ""
        if text_length>=75:
            # Loop through paragraphs and add all text, separated by <p>
            for par in document:
                text += str(par)
                text += "<p>"
            f.write(document.meta['id']+'\t'+' '.join(space_re.sub(' ',text).split(' ')[:512])+'\n')

    print("The extracted corpus is created.")

select_texts(dataset_name)