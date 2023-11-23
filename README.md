# Analysis of genre prediction in CLASSLA-web corpora

## Sample preparation for manual evaluation

- Run: `CUDA_VISIBLE_DEVICES=0 python vert-to-txt-genre-sample.py corpus.vert.gz` - specify the corpus name. This code parses the first 100,000 texts in the corpus and the randomly samples out 10 instances of each of genre classes. Before sampling, we filter out texts, longer than 500 words. It saves the sample as a tab-separated TXT. Then it takes the TXT text, applies google translate over it and saves the text as JSONL, prepared to be imported to the Doccano annotation tool (as a file `datasets/CLASSLA-web.{lang}.1.0.-translated-genre-sample-for-annotation.jsonl`)

- I've also created a function that takes the entire .vert corpus, parses it and saves is as JSONL file: `CUDA_VISIBLE_DEVICES=0 python vert-to-json.py corpus.vert.gz`



## Sample evaluation

The manually annotated samples are *annotations/sample-evaluation-annotation-run1.tsv* and *annotations/manual-genre-evaluation-run2.tsv*.

For the sample, I randomly sampled 10 instances of each of the genre classes -> 90 instances per corpus. I included "Other" as the label in the sample. However, as this label is mostly used so that the classifier can use it for harder examples, when doing manual annotation, I tried to identify the actual label of these texts, so most of texts, labelled Other, were manually annotated as something else.

I evaluated three corpora: CLASSLA-web.sl, CLASSLA-web.hr and CLASSLA-web.mk.

Code for evaluation: `evaluation-of-annotation.ipynb`

The following results (label distributions and comparisons with y_pred) are based on the second, improved annotation run.

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


### Label distribution (y_true)

Corpus: mk

| y_true_run2             |   count |
|:------------------------|--------:|
| Promotion               |      12 |
| News                    |      11 |
| Prose/Lyrical           |      11 |
| Opinion/Argumentation   |      11 |
| Information/Explanation |      10 |
| Forum                   |       9 |
| Instruction             |       9 |
| Legal                   |       9 |
| Multiple texts  (8%)        |       7 |
| Other                   |       1 |

Corpus: hr

| y_true_run2             |   count |
|:------------------------|--------:|
| Promotion               |      14 |
| Prose/Lyrical           |      12 |
| Forum                   |      12 |
| Information/Explanation |       9 |
| Legal                   |       9 |
| News                    |       9 |
| Opinion/Argumentation   |       8 |
| Multiple texts (7%)         |       6 |
| Other                   |       6 |
| Instruction             |       5 |


Corpus: sl

| y_true_run2             |   count |
|:------------------------|--------:|
| Prose/Lyrical           |      13 |
| Promotion               |      12 |
| Legal                   |      11 |
| Forum                   |      10 |
| News                    |       9 |
| Instruction             |       9 |
| Information/Explanation |       9 |
| Multiple texts (8%)         |       7 |
| Opinion/Argumentation   |       7 |
| Other                   |       3 |


7-8% of texts were annotated to be problematic ("multiple texts") - mostly, they were not a coherent text (just a list of summaries, multiple texts concatenated).

Secondly, in most cases, I manually annotated the category Other as some other, more concrete label.

For calculating the metrics of classifier's performance, I will thus remove "Other" texts and "Multiple texts" texts from the sample.

### Comparing y_true and y_pred with F1 scores

In the evaluation, we compare only the predictions of 8 labels - not including "Other". In addition, I had to remove texts that I could not manually annotate (they were not coherent texts). Final evaluated sample consists of 223 instances.

Frequency of predicted labels after removal of "Other" and "Problematic" texts:

Corpus: mk

| y_pred                  |   count |
|:------------------------|--------:|
| Prose/Lyrical           |      10 |
| Information/Explanation |      10 |
| Legal                   |      10 |
| Forum                   |       9 |
| News                    |       9 |
| Instruction             |       9 |
| Promotion               |       9 |
| Opinion/Argumentation   |       9 |

Corpus: hr

| y_pred                  |   count |
|:------------------------|--------:|
| Opinion/Argumentation   |      10 |
| Forum                   |      10 |
| Prose/Lyrical           |      10 |
| News                    |      10 |
| Promotion               |       9 |
| Legal                   |       9 |
| Information/Explanation |       8 |
| Instruction             |       8 |

Corpus: sl

| y_pred                  |   count |
|:------------------------|--------:|
| Legal                   |      10 |
| Prose/Lyrical           |      10 |
| Forum                   |      10 |
| Opinion/Argumentation   |       9 |
| Instruction             |       9 |
| Promotion               |       9 |
| Information/Explanation |       9 |
| News                    |       8 |

**Results**

The top three labels with the lowest F1 score (in each dataset) are marked with bold.

**Corpus: CLASSLA.web-sl**

Macro f1: 0.943, Micro f1: 0.946, Accuracy: 0.946

|                         |   precision |   recall |   f1-score |   support |
|:------------------------|------------:|---------:|-----------:|----------:|
| News                    |    1        | 1        |   1        | 10        |
| **Instruction**             |    0.888889 | 1        |   0.941176 |  8        |
| Opinion/Argumentation   |    1        | 1        |   1        |  9        |
| Promotion               |    1        | 0.909091 |   0.952381 | 11        |
| **Legal**                   |    1        | 0.888889 |   0.941176 |  9        |
| **Information/Explanation** |    0.666667 | 1        |   0.8      |  6        |
| Prose/Lyrical           |    1        | 1        |   1        |  9        |
| **Forum**                   |    1        | 0.833333 |   0.909091 | 12        |


**Corpus: CLASSLA.web-hr**

Macro f1: 0.888, Micro f1: 0.892, Accuracy: 0.892

|                         |   precision |   recall |   f1-score |   support |
|:------------------------|------------:|---------:|-----------:|----------:|
| Promotion               |    1        | 0.833333 |   0.909091 | 12        |
| Information/Explanation |    1        | 0.888889 |   0.941176 |  9        |
| **Prose/Lyrical**           |    0.625    | 1        |   0.769231 |  5        |
| Forum                   |    1        | 1        |   1        |  9        |
| Opinion/Argumentation   |    0.9      | 1        |   0.947368 |  9        |
| **Legal**                   |    0.7      | 0.875    |   0.777778 |  8        |
| News                    |    1        | 0.818182 |   0.9      | 11        |
| **Instruction**             |    0.9      | 0.818182 |   0.857143 | 11        |


**Corpus: CLASSLA.web-mk**

Macro f1: 0.932, Micro f1: 0.933, Accuracy: 0.933

|                         |   precision |   recall |   f1-score |   support |
|:------------------------|------------:|---------:|-----------:|----------:|
| Forum                   |    1        | 1        |   1        |  9        |
| **News**                    |    0.8      | 1        |   0.888889 |  8        |
| Instruction             |    1        | 1        |   1        |  9        |
| Promotion               |    0.9      | 1        |   0.947368 |  9        |
| **Prose/Lyrical**           |    1        | 0.818182 |   0.9      | 11        |
| **Opinion/Argumentation**   |    0.777778 | 0.875    |   0.823529 |  8        |
| Legal                   |    1        | 0.9      |   0.947368 | 10        |
| Information/Explanation |    1        | 0.909091 |   0.952381 | 11        |

