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

def vert_to_jsonl(corpus_path, gzip_file=True):
	"""
	Function to transform vertical format (vert) to jsonl format, based on the CLASSLA-web files. Change the function if the files contain other metadata.

	Args:
	- corpus_path: path to the dataset in VERT format
	- gzip_file: whether the file is gzipped. Defaults to true.
	"""
	if gzip_file == True:
		corpus = gzip.open(corpus_path, "rt")
	else:
		corpus = open(corpus_path, "r")

	# Open a new file to which we will append each json line
	new_file = open("{}.jsonl".format(corpus_path), "w")
	new_file.close()
	new_file = open("{}.jsonl".format(corpus_path), "a")

	text_id_re = re.compile('id="(.+?)"')
	url_re = re.compile('url="(.+?)"')
	domain_re = re.compile('domain="(.+?)"')
	genre_re = re.compile('genre="(.+?)"')

	text_counter = 0

	for line in corpus:
		if line.startswith("<text"):
			current_text = {}
			text_string = ""
			current_text["text_id"] = text_id_re.search(line).group(1)
			current_text["url"] = url_re.search(line).group(1)
			current_text["domain"] = domain_re.search(line).group(1)
			current_text["genre"] = genre_re.search(line).group(1)
			current_text["text"] = ""
			current_text["text_length"] = 0
			current_ling_anno = []
		elif line.startswith("<p"):
			continue
		elif line.startswith("<s"):
			continue
		elif line.startswith("</p"):
			text_string = text_string.rstrip()
			text_string += "\n"
		elif line.startswith("</s"):
			continue
		elif line.startswith("<g"):
			# Remove space before the last word if there is a symbol <g (= glue, meaning no space between words)
			text_string = text_string.rstrip()
		elif line.startswith("</text>"):
			current_text["ling_anno"] = current_ling_anno
			current_text["text"] = text_string
			current_text["text_length"] = len(text_string.split())
			new_file.write("{}".format(current_text))
			new_file.write("\n")
			text_counter += 1
			if text_counter%10 == 0:
				print("Processed {} files.".format(text_counter))
		else:
			current_line = line.split("\t")
			current_line_dict = {"word": current_line[0], "lemma": current_line[1], "xpos": current_line[2], "upos": current_line[3], "feats": current_line[4], "id": current_line[5].replace("\n", "")}
			current_ling_anno.append(current_line_dict)
			current_word = current_line[0]
			text_string += current_word
			text_string += " "
	
	new_file.close()
	print("Processing completed. The new file is saved as {}.jsonl".format(corpus_path))

if ".vert.gz" in corpus_path:
	vert_to_jsonl(corpus_path)
else:
	vert_to_jsonl(corpus_path, gzip_file=False)