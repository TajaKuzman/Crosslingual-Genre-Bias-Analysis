import gzip
import regex as re
import sys
import pandas as pd
import json
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("corpus_path", help="path to the corpus in VERT format")
    args = parser.parse_args()

corpus_path = args.corpus_path

def vert_to_txt_sample(corpus_path, gzip_file=True):
	"""
	Function to transform vertical format (vert) to jsonl format, based on the CLASSLA-web files.
	We will only extract a sample of 250 000 texts.

	Args:
	- corpus_path: path to the dataset in VERT format
	- gzip_file: whether the file is gzipped. Defaults to true.
	"""
	if gzip_file == True:
		corpus = gzip.open(corpus_path, "rt")
	else:
		corpus = open(corpus_path, "r")

	# Open a new file to which we will append each json line
	new_file = open("{}-sample.txt".format(corpus_path), "w")
	new_file.write("text_id\turl\tdomain\tgenre\ttext\ttext_length\n")
	new_file.close()
	new_file = open("{}-sample.txt".format(corpus_path), "a")

	text_id_re = re.compile('id="(.+?)"')
	url_re = re.compile('url="(.+?)"')
	domain_re = re.compile('domain="(.+?)"')
	genre_re = re.compile('genre="(.+?)"')

	text_counter = 0

	for line in corpus:
		if text_counter < 100000:
			if line.startswith("<text"):
				current_text = {}
				text_string = ""
				current_text["text_id"] = text_id_re.search(line).group(1)
				current_text["url"] = url_re.search(line).group(1)
				current_text["domain"] = domain_re.search(line).group(1)
				current_text["genre"] = genre_re.search(line).group(1)
				current_text["text"] = ""
				current_text["text_length"] = 0
			elif line.startswith("<p"):
				continue
			elif line.startswith("<s"):
				continue
			elif line.startswith("</p"):
				text_string = text_string.rstrip()
				text_string += "<p>"
			elif line.startswith("</s"):
				continue
			elif line.startswith("<g"):
				# Remove space before the last word if there is a symbol <g (= glue, meaning no space between words)
				text_string = text_string.rstrip()
			elif line.startswith("</text>"):
				current_text["text"] = text_string
				current_text["text_length"] = len(text_string.split())
				#new_file.write("{}".format(current_text))
				#new_file.write("\n")
				new_file.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(current_text["text_id"],current_text["url"],current_text["domain"], current_text["genre"], current_text["text"], current_text["text_length"]))
				text_counter += 1
				if text_counter%10 == 0:
					print("Processed {} files.".format(text_counter))
			else:
				current_line = line.split("\t")
				current_word = current_line[0]
				text_string += current_word
				text_string += " "
		else:
			break
	
	new_file.close()
	print("Processing completed. The sample is saved as {}-sample.txt".format(corpus_path))

if ".vert.gz" in corpus_path:
	vert_to_txt_sample(corpus_path)
else:
	vert_to_txt_sample(corpus_path, gzip_file=False)

def extract_genre_sample(sample_path):
	df = pd.read_csv(sample_path, sep="\t")

	# We will extract all labels
	labels_list=['Other', 'Information/Explanation', 'News', 'Instruction', 'Opinion/Argumentation', 'Forum', 'Prose/Lyrical', 'Legal', 'Promotion']

	# Remove all texts, longer than 500 words
	df = df[df["text_length"] < 500]

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

	# Save sample
	final_sample.to_csv("{}-genre-sample.txt".format(sample_path), sep="\t")
	
	return final_sample

sample_path = "{}-sample.txt".format(corpus_path)

sample_df = extract_genre_sample(sample_path)

lang = corpus_path.split(".")[1]

sample_paths = {lang: sample_path}

def genre_sample_to_json(sample_paths, lang):
	""" Convert genre sample in TXT to JSON and add translations and paragraph structure.
	
		Args:
		- sample_paths: path to a file, created with the function extract_genre_sample
		- lang: hr, mk, sl"""
	
	sample_df = pd.read_csv(sample_paths[lang], sep="\t", index_col = 0)

	# Change <p> signs to actual new lines
	sample_df["text"] = sample_df["text"].str.replace("<p>", "\n\n")


	# Apply Google Translate and machine translate the data
	import googletrans
	from googletrans import Translator

	# Define the translation model
	translator = Translator()

	# Create the final list
	translation_GT = []

	sentence_list = sample_df["text"].to_list()

	print("Starting translation.")

	# Loop through the list of original sentences,
	# translate each and append the translation to the final list
	for i in sentence_list:
		# Translate the sentence from Slovene (src = "sl") to English (dest = "en")
			current_translation = translator.translate(i, src = lang, dest='en')
		# Append the translated sentence to the final list
			translation_GT.append(current_translation.text)

	print("Translation finished.")

	# Append translations to the sample

	sample_df["translation"] = translation_GT

	# Save to JSON lines
	sample_df.to_json("datasets/CLASSLA-web.{}.1.0.-translated-genre-sample.jsonl".format(lang), orient="records", lines=True)

	print("Final file saved as datasets/CLASSLA-web.{}.1.0.-translated-genre-sample.jsonl".format(lang))

	# Create also a version for the annotation tool, only with translation and labels
	ann_df = sample_df[["translation","genre"]]

	# For annotation, each label should be in a list
	ann_df["genre"] = ann_df["genre"].apply(lambda x:[x])

	# Rename df
	ann_df.columns = ["text", "label"]

	# Add metadata
	text_ids = sample_df["text_id"].to_list()
	domains = sample_df["domain"].to_list()

	metadata_list = []

	for i in list(zip(text_ids,domains)):
		metadata = {"text_id": i[0], "domain": i[1]}
		metadata_list.append(metadata)

	ann_df["metadata"] = metadata_list

	# Save to JSON lines
	ann_df.to_json("datasets/CLASSLA-web.{}.1.0.-translated-genre-sample-for-annotation.jsonl".format(lang), orient="records", lines=True)

	print("File for annotation saved as datasets/CLASSLA-web.{}.1.0.-translated-genre-sample-for-annotation.jsonl".format(lang))

	return sample_df
