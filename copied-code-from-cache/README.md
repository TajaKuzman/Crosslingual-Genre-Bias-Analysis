# Download and unzip the relevant corpora

Run the following:
1. download the dataset: `curl -s --remote-name-all path`
2. unzip the dataset: `unzip -q downloaded_file`
3. remove the zipped dataset: `rm downloaded_file`
4. extract TSV file with texts that are longer than 75 words: `CUDA_VISIBLE_DEVICES=7 nohup python 1-select_for_xgenre.py "MaCoCu-mt-2.0.xml" > extraction.log &` Only the first 512 words are taken of each text. The paragraphs are separated by the `<p>` tag. The resulting file is dataset name, but with .tsv suffix (e.g., "MaCoCu-mt-2.0.tsv")
5. predict genres to all texts in the TSV file: `CUDA_VISIBLE_DEVICES=7 nohup python 2-predict_extended.py "MaCoCu-mt-2.0.tsv" > prediction.log &` The output is dataset name with "genre-annotated.jsonl" suffix (e.g., "MaCoCu-mt-2.0.tsv-genre-annotated.jsonl") in the `datasets/annotated` directory.
6. Extract a genre sample that will be used for manual evaluation: `CUDA_VISIBLE_DEVICES=7 nohup python 3-prepare-sample.py "datasets/annotated/MaCoCu-is-2.0.tsv-genre-annotated.jsonl" "is" > genre_sample-is.log &` - the code takes two arguments: the path to the JSONL file, created in the previous step and the language suffix (the same as in the dataset name). There are two outputs:
    - `/datasets/annotated/MaCoCu-{suffix}-genre-sample.jsonl` - the genre sample with all information
    - `/datasets/annotated/MaCoCu-{}-genre-sample-for-annotation-tool.jsonl` - the genre sample, prepared to be imported to the Dockanno annotation tool (without source text and with less information)

In case of CLASSLA-web corpora, we used the corpora that had the genre already predicted (with the same approach) and that were saved in VERT file. See section `Prepare similar JSONL corpora from CLASSLA corpora` in `/cache/tajak/macocu-mt/analyze-entire-file-prepare-sample.ipynb` to see how the corpora were transformed from VERT format to a JSONL format. The JSONL format is the same as the one that is used for MaCoCu corpora, so all further steps can then be applied to the corpora in the same manner.

I later realised that there are texts in MaCoCu corpora which have paragraphs in multiple languages. We decided to clean these paragraphs out and reapply genre predictions on them to truly get predictions on the target language only. See `clean-entire-corpora-for-target-lang.ipynb` for code for analysing texts and preparation of the final code. I did the following:
- I added to the final annotated file information about lang distribution in each text (extracted from the initial XLM files): `datasets/annotated/MaCoCu-tr-2.0.tsv-genre-annotated-with-lang-distr.jsonl`
- Then I split this file into a file that has only texts that are in target language (`datasets/annotated/MaCoCu-tr-2.0.tsv-genre-annotated-only-target-lang.jsonl`) - these texts are okay and do not need reprocessing. These texts represent 91% to 99% of all texts in the initial file.
- Then I extracted the texts that need to be reprocessed and 1) removed all non-short paragraphs that are not in the target language from them; 2) if they were still long enough (> 75 - otherwise, they were skipped), I applied genre classifier on them. The code for this is: `CUDA_VISIBLE_DEVICES=2 nohup python 4-process-mixed-lang-texts.py "sq-1.0" > preparing_mixed_texts.log &`. The output are cleaned texts, annotated with genres: `datasets/annotated/MaCoCu-{suffix}-mixed-texts-genre-annotated.jsonl`
- Then I joined the target-lang texts and newly processed cleaned texts (see `clean-entire-corpora-for-target-lang.ipynb`) into: `/cache/tajak/macocu-mt/datasets/annotated/MaCoCu-{suffix}-genre-annotated-reprocessed-final.jsonl` which is now **the main dataset** on which genre distribution is to be calculated and instances for samples are to be taken.

Here are the paths to the files:
```json
corpora_location='{
    "mt": {
        "path":"https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1803/MaCoCu-mt-2.0.xml.zip",
        "downloaded_file": "MaCoCu-mt-2.0.xml.zip"},
    "ca": {
        "path":"https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1837/MaCoCu-ca-1.0.xml.zip",
        "downloaded_file": "MaCoCu-ca-1.0.xml.zip"},
    "el": {
        "path":"https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1839/MaCoCu-el-1.0.xml.zip",
        "downloaded_file": "MaCoCu-el-1.0.xml.zip"},
    "is": {
        "path":"https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1805/MaCoCu-is-2.0.xml.zip",
        "downloaded_file": "MaCoCu-is-2.0.xml.zip"},
    "tr": {
        "path":"https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1802/MaCoCu-tr-2.0.xml.zip",
        "downloaded_file": "MaCoCu-tr-2.0.xml.zip"},
    "uk": {
        "path":"https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1838/MaCoCu-uk-1.0.xml.zip",
        "downloaded_file": "MaCoCu-uk-1.0.xml.zip"},
    }'
```

## Genre sample preparation

The genre samples are prepared in such way that we take 10 random instances of each genre from the entire corpus. We do not include the genres "Other" and "Mix", as they are not informative - the final sample size is 80 instances.

Then we translate the source text in the sample to English using Google Translate. Google Translate provides models for all of our languages, except for Montenegrin, for which we used the Serbian MT model.

