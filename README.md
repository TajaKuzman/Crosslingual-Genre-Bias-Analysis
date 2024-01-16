# Analysis of genre prediction in CLASSLA-web and MaCoCu corpora

Final test corpus which consists of all manually evaluated corpora is: `manual-annotations/multilingual-genre-annotated-test-set.json`

It is a JSON file with the following values:
- language: language of the test set. Each language item then consists of the following values:
    - accuracy, micro_f1, macro_f1: the evaluation results in accuracy, micro F1 and macro F1 metric
    - dataset: the test dataset, which includes the automatically predicted labels (y_pred), the manually-evaluated labels (y_true), text, translation (the translation to English which was used for manual evaluation), text_id (the same as in the original MaCoCu or CLASSLA-web corpora) and metadata. The dataset can be opened as a pandas dataframe: `pd.DataFrame(json_dict["lang"]["dataset"])`

## Automatically annotated MaCoCu corpora

For automatic annotation, we only annotate texts that are longer (or the same size) than 75 words. Furthermore, due to model's limitations, we only take the first 512 words of each text (because the max_sequence_length that model can take is 512 tokens).

See the [spreadsheet CLASSLA genres](https://docs.google.com/spreadsheets/d/1-jZW_lEAyCdI-tcywjUJUgBgu46jr2el1AgFOGYUxyU/edit?usp=sharing) for all sizes and genre distributions. 

We use the code `1-select_for_xgenre.py` and `2-predict_extended.py` in `/cache/tajak/macocu-mt/`. The automatically annotated datasets are saved in `/cache/tajak/macocu-mt/datasets/annotated`.


### Download and unzip the relevant corpora

Run the following:
1. download the dataset: `curl -s --remote-name-all path`
2. unzip the dataset: `unzip -q downloaded_file`
3. remove the zipped dataset: `rm downloaded_file`
4. extract TSV file with texts that are longer than 75 words: `CUDA_VISIBLE_DEVICES=7 nohup python 1-select_for_xgenre.py "MaCoCu-mt-2.0.xml" > extraction.log &` Only the first 512 words are taken of each text. The paragraphs are separated by the `<p>` tag. The resulting file is dataset name, but with .tsv suffix (e.g., "MaCoCu-mt-2.0.tsv")
5. predict genres to all texts in the TSV file: `CUDA_VISIBLE_DEVICES=7 nohup python 2-predict_extended.py "MaCoCu-mt-2.0.tsv" > prediction.log &` The output is dataset name with "genre-annotated.jsonl" suffix (e.g., "MaCoCu-mt-2.0.tsv-genre-annotated.jsonl") in the `datasets/annotated` directory.
6. Extract a genre sample that will be used for manual evaluation: use the script `/cache/tajak/macocu-mt/analyze-entire-file-prepare-sample.ipynb` There are two outputs:
    - `/datasets/annotated/MaCoCu-{suffix}-genre-sample.jsonl` - the genre sample with all information
    - `/datasets/annotated/MaCoCu-{}-genre-sample-for-annotation-tool.jsonl` - the genre sample, prepared to be imported to the Docanno annotation tool (without source text and with less information)
7. Evaluate the sample after annotation: `/home/tajak/Crosslingual-Genre-Bias-Analysis/evaluation-of-annotation.ipynb`
8. If needed, annotate additional instances: see section `Add additional instances to the sample to achieve 10 instances per label` in `/cache/tajak/macocu-mt/analyze-entire-file-prepare-sample.ipynb` to prepare additional instances; and section `Add additionally annotated instances` in `/home/tajak/Crosslingual-Genre-Bias-Analysis/evaluation-of-annotation.ipynb` to merge them with initial sample and get final evaluations.

In case of CLASSLA-web corpora, we used the corpora that had the genre already predicted (with the same approach) and that were saved in VERT file. See section `Prepare similar JSONL corpora from CLASSLA corpora` in `/cache/tajak/macocu-mt/analyze-entire-file-prepare-sample.ipynb` to see how the corpora were transformed from VERT format to a JSONL format. The JSONL format is the same as the one that is used for MaCoCu corpora, so all further steps can then be applied to the corpora in the same manner.

Output:
- `manual-annotations/MaCoCu-{lang}-genre-sample-evaluated-complete-sample.jsonl` - manually evaluated samples (or `MaCoCu-{lang}-genre-sample-evaluated-complete-sample-run2.jsonl` in case there were two rounds of adding additional instances)- initial samples + additional instances (so that each label was evaluated on 10 instances); Multiple texts and Other texts are marked, but included in the sample - use the code in `/home/tajak/Crosslingual-Genre-Bias-Analysis/evaluation-of-annotation.ipynb` to discard them and evaluate them.


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

### Genre sample preparation

The genre samples are prepared in such way that we take 10 random instances of each genre from the entire corpus. We do not include the genres "Other" and "Mix", as they are not informative - the final sample size is 80 instances. If the manual evalutation shows that some instances had to be discarded, because they were "Multiple texts", "Incomprehensible" or would belong to the category "Other", we annotated additional instances so that each label was annotated on 10 instances.

Then we translate the source text in the sample to English using Google Translate. Google Translate provides models for all of our languages, except for Montenegrin, for which we used the Serbian MT model.

## Analyze the results

### Results

| Dataset        | Macro F1 | Micro F1 |
|----------------|----------|----------|
| MaCoCu-uk | 0.948     | 0.950     |
| CLASSLA.web-sl | 0.936     | 0.938     |
| CLASSLA.web-mk | 0.932     | 0.925     |
| MaCoCu-tr | 0.899     | 0.9     |
| CLASSLA.web-hr | 0.883     | 0.887     |
| MaCoCu-sq | 0.866    | 0.863     |
| MaCoCu-el | 0.844     | 0.850     |
| MaCoCu-ca | 0.827     | 0.825     |
| MaCoCu-is | 0.810     | 0.812     |
| MaCoCu-mt | 0.552     | 0.613     |


### CLASSLA.web-sl

Macro f1: 0.936, Micro f1: 0.938, Accuracy: 0.938


|                         |   precision |   recall |   f1-score |   support |
|:------------------------|------------:|---------:|-----------:|----------:|
| Forum                   |     1       | 1        |   1        |   10      |
| Information/Explanation |     0.9     | 0.9      |   0.9      |   10      |
| Instruction             |     1       | 1        |   1        |   10      |
| Legal                   |     1       | 0.909091 |   0.952381 |   11      |
| News                    |     0.9     | 0.9      |   0.9      |   10      |
| Opinion/Argumentation   |     0.7     | 1        |   0.823529 |    7      |
| Promotion               |     1       | 1        |   1        |   10      |
| Prose/Lyrical           |     1       | 0.833333 |   0.909091 |   12      |

![](figures/CLASSLA-sl-evaluation.png)

### CLASSLA.web-hr

Macro f1: 0.883, Micro f1: 0.887, Accuracy: 0.887

|                         |   precision |   recall |   f1-score |   support |
|:------------------------|------------:|---------:|-----------:|----------:|
| Forum                   |      1      | 0.833333 |   0.909091 |   12      |
| Information/Explanation |      1      | 0.909091 |   0.952381 |   11      |
| Instruction             |      0.6    | 1        |   0.75     |    6      |
| Legal                   |      1      | 1        |   1        |   10      |
| News                    |      0.9    | 1        |   0.947368 |    9      |
| Opinion/Argumentation   |      0.7    | 0.875    |   0.777778 |    8      |
| Promotion               |      1      | 0.769231 |   0.869565 |   13      |
| Prose/Lyrical           |      0.9    | 0.818182 |   0.857143 |   11      |

![](figures/CLASSLA-hr-evaluation.png)

### Corpus: CLASSLA.web-mk

Macro f1: 0.923, Micro f1: 0.925, Accuracy: 0.925

|                         |   precision |   recall |   f1-score |   support |
|:------------------------|------------:|---------:|-----------:|----------:|
| Forum                   |     1       | 1        |   1        |    10     |
| Information/Explanation |     0.8     | 0.888889 |   0.842105 |     9     |
| Instruction             |     1       | 1        |   1        |    10     |
| Legal                   |     0.9     | 1        |   0.947368 |     9     |
| News                    |     1       | 0.833333 |   0.909091 |    12     |
| Opinion/Argumentation   |     0.7     | 0.875    |   0.777778 |     8     |
| Promotion               |     1       | 0.909091 |   0.952381 |    11     |
| Prose/Lyrical           |     1       | 0.909091 |   0.952381 |    11     |

### Corpus: MaCoCu-sq

Macro f1: 0.866, Micro f1: 0.863, Accuracy: 0.863

|                         |   precision |   recall |   f1-score |   support |
|:------------------------|------------:|---------:|-----------:|----------:|
| Forum                   |      0.8    | 0.888889 |   0.842105 |    9      |
| Information/Explanation |      1      | 0.666667 |   0.8      |   15      |
| Instruction             |      0.9    | 1        |   0.947368 |    9      |
| Legal                   |      0.9    | 1        |   0.947368 |    9      |
| News                    |      0.8    | 1        |   0.888889 |    8      |
| Opinion/Argumentation   |      0.7    | 0.7      |   0.7      |   10      |
| Promotion               |      0.9    | 1        |   0.947368 |    9      |
| Prose/Lyrical           |      0.9    | 0.818182 |   0.857143 |   11      |

![](figures/MaCoCu-sq-evaluation.png)


### Corpus: MaCoCu-mt

Macro f1: 0.552, Micro f1: 0.613, Accuracy: 0.613

|                         |   precision |   recall |   f1-score |   support |
|:------------------------|------------:|---------:|-----------:|----------:|
| Forum                   |      0.1    | 1        |   0.181818 |    1      |
| Information/Explanation |      0.6    | 0.461538 |   0.521739 |   13      |
| Instruction             |      1      | 0.526316 |   0.689655 |   19      |
| Legal                   |      1      | 1        |   1        |   10      |
| News                    |      0.9    | 0.5625   |   0.692308 |   16      |
| Opinion/Argumentation   |      0.3    | 0.375    |   0.333333 |    8      |
| Promotion               |      0.9    | 0.75     |   0.818182 |   12      |
| Prose/Lyrical           |      0.1    | 1        |   0.181818 |    1      |

![](figures/MaCoCu-mt-evaluation.png)


### Corpus: MaCoCu-tr

Macro f1: 0.899, Micro f1: 0.9, Accuracy: 0.9

|                         |   precision |   recall |   f1-score |   support |
|:------------------------|------------:|---------:|-----------:|----------:|
| Forum                   |      0.8    | 1        |   0.888889 |       8   |
| Information/Explanation |      0.7    | 1        |   0.823529 |       7   |
| Instruction             |      0.9    | 0.9      |   0.9      |      10   |
| Legal                   |      1      | 1        |   1        |      10   |
| News                    |      1      | 0.909091 |   0.952381 |      11   |
| Opinion/Argumentation   |      0.9    | 0.75     |   0.818182 |      12   |
| Promotion               |      0.9    | 0.818182 |   0.857143 |      11   |
| Prose/Lyrical           |      1      | 0.909091 |   0.952381 |      11   |

### MaCoCu-el

Macro f1: 0.844, Micro f1: 0.85, Accuracy: 0.85

|                         |   precision |   recall |   f1-score |   support |
|:------------------------|------------:|---------:|-----------:|----------:|
| Forum                   |      1      | 0.909091 |   0.952381 |     11    |
| Information/Explanation |      0.8    | 0.615385 |   0.695652 |     13    |
| Instruction             |      0.6    | 0.857143 |   0.705882 |      7    |
| Legal                   |      1      | 1        |   1        |     10    |
| News                    |      0.9    | 0.9      |   0.9      |     10    |
| Opinion/Argumentation   |      1      | 0.769231 |   0.869565 |     13    |
| Promotion               |      0.5    | 0.833333 |   0.625    |      6    |
| Prose/Lyrical           |      1      | 1        |   1        |     10    |

### MaCoCu-is

Macro f1: 0.81, Micro f1: 0.812, Accuracy: 0.812

|                         |   precision |   recall |   f1-score |   support |
|:------------------------|------------:|---------:|-----------:|----------:|
| Forum                   |     0.9     | 1        |   0.947368 |    9      |
| Information/Explanation |     0.5     | 0.714286 |   0.588235 |    7      |
| Instruction             |     0.7     | 0.875    |   0.777778 |    8      |
| Legal                   |     0.8     | 0.888889 |   0.842105 |    9      |
| News                    |     0.8     | 0.666667 |   0.727273 |   12      |
| Opinion/Argumentation   |     0.9     | 0.75     |   0.818182 |   12      |
| Promotion               |     0.9     | 0.692308 |   0.782609 |   13      |
| Prose/Lyrical           |     1       | 1        |   1        |   10      |

### MaCoCu-ca

Macro f1: 0.827, Micro f1: 0.825, Accuracy: 0.825

|                         |   precision |   recall |   f1-score |   support |
|:------------------------|------------:|---------:|-----------:|----------:|
| Forum                   |      0.8    | 0.888889 |   0.842105 |     9     |
| Information/Explanation |      0.9    | 0.6      |   0.72     |    15     |
| Instruction             |      0.6    | 1        |   0.75     |     6     |
| Legal                   |      0.9    | 1        |   0.947368 |     9     |
| News                    |      0.7    | 1        |   0.823529 |     7     |
| Opinion/Argumentation   |      0.8    | 0.888889 |   0.842105 |     9     |
| Promotion               |      0.9    | 0.692308 |   0.782609 |    13     |
| Prose/Lyrical           |      1      | 0.833333 |   0.909091 |    12     |

### MaCoCu-uk

Macro f1: 0.948, Micro f1: 0.95, Accuracy: 0.95

|                         |   precision |   recall |   f1-score |   support |
|:------------------------|------------:|---------:|-----------:|----------:|
| Forum                   |     0.9     | 1        |   0.947368 |      9    |
| Information/Explanation |     1       | 1        |   1        |     10    |
| Instruction             |     1       | 0.909091 |   0.952381 |     11    |
| Legal                   |     1       | 1        |   1        |     10    |
| News                    |     1       | 1        |   1        |     10    |
| Opinion/Argumentation   |     1       | 0.833333 |   0.909091 |     12    |
| Promotion               |     0.7     | 0.875    |   0.777778 |      8    |
| Prose/Lyrical           |     1       | 1        |   1        |     10    |


## More information on sample evaluation

### First batch of languages: Slovenian, Croatian, Macedonian and Albanian

For the sample, I randomly sampled 10 instances of each of the genre classes from the first 100.000 texts in the corpora -> 90 instances per corpus. I included "Other" as the label in the sample. However, as this label is mostly used so that the classifier can use it for harder examples, when doing manual annotation, I tried to identify the actual label of these texts, so most of texts, labelled Other, were manually annotated as something else.

I evaluated three corpora: CLASSLA-web.sl, CLASSLA-web.hr and CLASSLA-web.mk. After the two rounds of evaluation of these three corpora, I also evaluated the Albanian corpus: MaCoCu-sq.

### Second batch: extended evaluation to all other MaCoCu corpora

The sample was prepared in the same way, except for the fact that we randomly sampled the texts from the entire corpus (not from the first 100.000 as in the first batch). Second difference is that we did not include the "Other" label in the sample, because this is used as a "throw-away" category to be used when the classifier doesn't recognize the text to be of any other, more concrete genres.

### Label distribution (y_true)

This is the distribution after the additionally evaluated instances were added.

For calculating the metrics of classifier's performance, I remove "Other" texts and "Multiple texts" (also "Incomprehensible" in case of Albanian) texts from the sample. Thus, we compare only the predictions of 8 labels, each having 10 instances.

Initial distribution (before post-processing):

MaCoCu-mt:

| y_true                  |   count |
|:------------------------|--------:|
| Instruction             |      19 |
| News                    |      16 |
| Information/Explanation |      13 |
| Promotion               |      12 |
| Legal                   |      10 |
| Opinion/Argumentation   |       8 |
| Multiple texts (3%)         |       2 |
| Forum                   |       1 |
| Prose/Lyrical           |       1 |

MaCoCu-el:

| y_true                  |   count |
|:------------------------|--------:|
| Opinion/Argumentation   |      13 |
| Information/Explanation |      13 |
| Forum                   |      11 |
| Prose/Lyrical           |      10 |
| Legal                   |      10 |
| News                    |      10 |
| Instruction             |       7 |
| Promotion               |       6 |
| Multiple texts (7%)         |       6 |

MaCoCu-tr:

| y_true                  |   count |
|:------------------------|--------:|
| Opinion/Argumentation   |      12 |
| News                    |      11 |
| Prose/Lyrical           |      11 |
| Promotion               |      11 |
| Instruction             |      10 |
| Legal                   |      10 |
| Forum                   |       8 |
| Information/Explanation |       7 |
| Multiple texts (4.7%)         |       4 |
| Other  (1.17%)                 |       1 |

MaCoCu-sq:

| y_true                  |   count |
|:------------------------|--------:|
| Information/Explanation |      17 |
| Opinion/Argumentation   |      12 |
| Forum                   |      12 |
| Prose/Lyrical           |      12 |
| Legal                   |       9 |
| Promotion               |       9 |
| Instruction             |       9 |
| News                    |       8 |
| Other (4.12%)                  |       4 |
| Multiple texts (3.1%)         |       3 |
| Incomprehensible (2.1%)       |       2 |

MaCoCu-is:

| y_true                  |   count |
|:------------------------|--------:|
| Promotion               |      13 |
| Opinion/Argumentation   |      12 |
| News                    |      12 |
| Prose/Lyrical           |      10 |
| Legal                   |       9 |
| Forum                   |       9 |
| Instruction             |       8 |
| Information/Explanation |       7 |
| Multiple texts (7.95%)         |       7 |
| Incomprehensible (1.14%)       |       1 |

MaCoCu-ca:

| y_true                  |   count |
|:------------------------|--------:|
| Information/Explanation |      15 |
| Promotion               |      13 |
| Prose/Lyrical           |      12 |
| Forum                   |       9 |
| Legal                   |       9 |
| Opinion/Argumentation   |       9 |
| News                    |       7 |
| Instruction             |       6 |
| Multiple texts (3.5%)         |       3 |
| Incomprehensible (2.35%)       |       2 |

MaCoCu-uk:

| y_true                  |   count |
|:------------------------|--------:|
| Opinion/Argumentation   |      12 |
| Instruction             |      11 |
| Prose/Lyrical           |      10 |
| Legal                   |      10 |
| News                    |      10 |
| Information/Explanation |      10 |
| Forum                   |       9 |
| Promotion               |       8 |
| Multiple texts  (9%)        |       8 |

In CLASSLA-web corpora, we initially also annotated the "Other" labels, that is why they are present here more than in other corpora.

CLASSLA-mk:

| y_true                  |   count |
|:------------------------|--------:|
| Promotion               |      13 |
| News                    |      12 |
| Prose/Lyrical           |      11 |
| Opinion/Argumentation   |      11 |
| Information/Explanation |      11 |
| Forum                   |      10 |
| Instruction             |      10 |
| Legal                   |       9 |
| Multiple texts  (8.3%)        |       8 |
| Other   (1%)                |       1 |

CLASSLA-hr:

| y_true                  |   count |
|:------------------------|--------:|
| Promotion               |      16 |
| Prose/Lyrical           |      12 |
| Forum                   |      12 |
| Information/Explanation |      11 |
| Legal                   |      10 |
| News                    |       9 |
| Opinion/Argumentation   |       8 |
| Multiple texts (7.2%)         |       7 |
| Other (6.19%)                  |       6 |
| Instruction             |       6 |

| y_true                  |   count |
|:------------------------|--------:|
| Promotion               |      13 |
| Prose/Lyrical           |      13 |
| Legal                   |      11 |
| Information/Explanation |      11 |
| News                    |      10 |
| Instruction             |      10 |
| Forum                   |      10 |
| Multiple texts (8.25%)         |       8 |
| Opinion/Argumentation   |       8 |
| Other   (3.1%)                |       3 |

Number of texts, annotated as problematic ("multiple texts") - mostly, they were not a coherent text (just a list of summaries, multiple texts concatenated):
- Slovenian, Croatian, Macedonian, Icelandic, Greek, Ukrainian: 6-9%
- Albanian, Maltese, Turkish, Catalan: 3-5% - there were less problematic texts. However, in Albanian sample, there were also some incomprehensible texts - probably due to bad machine translation - 2% of texts.


### Improved sample evaluation - comparison with the first run

I re-did the evaluation on the same dataset, but after some improvements: the text was clearly separated into paragraphs -> texts are much more comprehensible and easier to understand; I used the doccano annotation platform -> easier and (slightly) faster annotation.

When I compared my annotations from the two runs, there were disagreements between the labels in 40 instances - 15% of instances.

The reasons for the differences:

| reason | frequency (# instances) |
|---|---|
| improved second run (text annotated with a label, instead of "problematic") | 8 |
| detected "multiple texts" that I didn't in the first run | 9 |
| inter-annotator disagreement | 23 |

So we can see that the improved methodology (better shown texts, using doccano and paragraph structure) improved annotation of 17 cases - 6% of all texts (either we were able to annotate texts that were previously incomprehensible, or we detected problematic texts that we previously didn't due to the lacking text structure).

In 23 instances (9%), there was inter-annotator disagreement, which shows the level of difficulty of this task. However, 8 of these cases appeared when annotating texts that were predicted as "Other", which we decided that we won't include in the annotation campaign anyway. If we disregard these cases, disagreement happened in 15 instances - 6% of texts.