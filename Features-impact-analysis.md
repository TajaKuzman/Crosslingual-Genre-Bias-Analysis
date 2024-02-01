## Corelation of genre frequency

Pearson and Spearman correlation for genre frequency for all corpora

According to p-value in Pearson correlation, higher than 0.05:

|                                       |   Pearson |   Pearson-p-value |   Spearman |   Spearman-p-value |
|:--------------------------------------|----------:|------------------:|-----------:|-------------------:|
| News-Information/Explanation          | -0.875348 |       4.11861e-05 |  -0.806593 |        0.000491113 |
| News-Forum                            | -0.707912 |       0.00461391  |  -0.564835 |        0.0353302   |
| Prose/Lyrical-Instruction             | -0.658999 |       0.0103677   |  -0.336264 |        0.239792    |
| News-Prose/Lyrical                    | -0.642166 |       0.0132784   |  -0.213187 |        0.464303    |
| News-Opinion/Argumentation            | -0.587845 |       0.0270476   |  -0.516484 |        0.0586372   |
| Prose/Lyrical-Promotion               | -0.583297 |       0.028556    |  -0.389011 |        0.169217    |
| Forum-Information/Explanation         |  0.538151 |       0.047128    |   0.217582 |        0.454919    |
| Forum-Opinion/Argumentation           |  0.566594 |       0.0346383   |   0.476923 |        0.0846484   |
| Forum-Prose/Lyrical                   |  0.622027 |       0.0175389   |   0.340659 |        0.233316    |
| Instruction-Promotion                 |  0.6428   |       0.0131586   |   0.63956  |        0.0137796   |
| Promotion-Legal                       |  0.705183 |       0.00484659  |   0.696703 |        0.00562868  |
| Information/Explanation-Prose/Lyrical |  0.827685 |       0.000257882 |   0.138462 |        0.636885    |

Correlations with p-value < 0.05 according to Spearman correlation:

|                              |   Pearson |   Pearson-p-value |   Spearman |   Spearman-p-value |
|:-----------------------------|----------:|------------------:|-----------:|-------------------:|
| News-Information/Explanation | -0.875348 |       4.11861e-05 |  -0.806593 |        0.000491113 |
| News-Forum                   | -0.707912 |       0.00461391  |  -0.564835 |        0.0353302   |
| Instruction-Promotion        |  0.6428   |       0.0131586   |   0.63956  |        0.0137796   |
| Legal-Promotion              |  0.705183 |       0.00484659  |   0.696703 |        0.00562868  |

## Data Sizes in XLM-R Pretraining


### Data Sizes

The data sizes are taken from the paper on XLM-R (Conneau et. al) and the language groups are defined based on Ethnologue platform (https://www.ethnologue.com/).

```python
# Sizes in GB, from https://aclanthology.org/2020.acl-main.747.pdf

sizes_mb = {
	"mt": 0,
	"el": 46.9,
	"tr": 20.9,
	"sq": 5.4,
	"is": 3.2,
	"uk": 84.6,
	"ca": 10.1,
	"mk": 4.8,
	"hr": 20.5 +0.1 + 9.1, #added Bosnian, Serbian (in that order), 
	"sl": 10.3,
	}

sizes_mb_with_related = {
	"mt": 0 + 28.0, # Central Semitic Arabic languages (Afro-Asiatic language family): Maltese, Arabic
	"el": 46.9, # is a separate branch of Indo-European language family and has no direct descendants that could be added
	"tr": 20.9 + 6.5, # Southern Turkic (Turkic language family): Turkish, Azerbaijani
	"sq": 5.4, # is a separate branch of Indo-European language family and has no direct descendants that could be added
	"is": 3.2 + 45.6 + 49.0 + 12.1, # North Germanic languages: Icelandic, Danish, Norwegian, Swedish
	"uk": 84.6 + 4.3 + 278.0, #East Slavic: Ukrainian, Belarusian, Russian
	"ca": 10.1 + 53.3 + 2.9 + 49.1, # Ibero-Romance: Catalan, Spanish, Galician, Portuguese
	"mk": 4.8 + 57.5, # Eastern South Slavic: Macedonian, Bulgarian
	"hr": 20.5 + 0.1 + 9.1 + 10.3, # Western South Slavic languages: Croatian, Bosnian, Serbian, Slovenian (in that order)
	"sl": 10.3 + 20.5 + 0.1 + 9.1 # Western South Slavic languages: Slovenian, Croatian, Bosnian, Serbian (in that order)
	}

#Sizes in M of tokens.
sizes = {
	"mt": 0,
	"el": 4285, 
	"tr": 2736,
	"sq": 918,
	"is": 505,
	"uk": 6500,
	"ca": 1752,
	"mk": 449,
	"hr": 3297 + 14 + 843, #added Bosnian, Serbian (in that order), 
	"sl": 1669,}

sizes_with_related = {
	"mt": 0 + 2869, # Central Semitic Arabic languages (Afro-Asiatic language family): Maltese, Arabic
	"el": 4285, # is a separate branch of Indo-European language family and has no direct descendants that could be added
	"tr": 2736 + 783,
	"sq": 918, # is a separate branch of Indo-European language family and has no direct descendants that could be added
	"is": 505 + 7823 + 8494 + 778, # North Germanic languages: Icelandic, Danish, Norwegian, Swedish
	"uk": 6500 + 362 + 23408, # East Slavic: Ukrainian, Belarusian, Russian
	"ca": 1752 + 9374 + 495 + 8405, # Ibero-Romance: Catalan, Spanish, Galician, Portuguese
	"mk": 449 + 5487, # Eastern South Slavic: Macedonian, Bulgarian 
	"hr": 3297 + 1669 + 14 + 843, # Western South Slavic languages: Croatian, Slovenian, Bosnian, Serbian (in that order)
	"sl": 1669 + 3297 + 14 + 843 # Western South Slavic languages: Slovenian, Croatian, Bosnian, Serbian (in that order)
	}
```

Plot of Macro F1 (x-axis) performance and sizes in GB (y-axis):

![](figures/sizes_impact.png)

Plot of Macro F1 (x-axis) performance and sizes (specific language + related languages) in GB (y-axis):

![](figures/sizes_with_related_lang_impact.png)

**Correlations on dataset-level:**

Sizes in tokens:

Pearsons correlation: 0.483
p-value: 0.15770106280572002
Spearmans correlation: 0.442
p-value: 0.20042268671194224

Sizes in GB:

Pearsons correlation: 0.415
p-value: 0.23343624750296876
Spearmans correlation: 0.588
p-value: 0.07387770688865801

Sizes in tokens + related languages:

Pearsons correlation: 0.240
p-value: 0.5035757809014645
Spearmans correlation: 0.280
p-value: 0.433925839676929

Sizes in GB + related languages:

Pearsons correlation: 0.298
p-value: 0.40378781012771897
Spearmans correlation: 0.122
p-value: 0.7379379712336098

### Per-label scores

Plot for size (in GB) and label F1 scores:

![](figures/size-label-scores-impact.png)

Pearsons correlation: 0.275
p-value: 0.013539468997046106
Spearmans correlation: 0.349
p-value: 0.0015106453984760197


Plot for size + related languages (in GB) and label F1 scores:

![](figures/size-related-label-scores-impact.png)

Pearsons correlation: 0.197
p-value: 0.07932862745724867
Spearmans correlation: 0.119
p-value: 0.2919649610699323

## Token overlap

We tokenised the X-GENRE classifier training set and the test sets with XLM-RoBERTa tokenizer (as the X-GENRE classifier is based on XLM-RoBERTa). For each text, we took only the first 512 tokens, since this is also the max sequence length that can be seen by the X-GENRE classifier. We removed the starting and ending token (s, \s).

#### Corpus-level

We count all occurences of the tokens from the test set in the training set. The train dataset has 699.465 tokens and 27.025 unique words. The token count is saved at `datasets/tokenized_datasets/X-GENRE-train-token-count.json`.

Overlap percentage: percentage of all tokens from the test set that occur in the training set. Calculated in such manner that we counted all tokens from test set that do not appear in training set and divided by number of all tokens from the test set to get "no overlap" percentage, then calculated the overlap percentage by "1-no_overlap_percentage".

Statistics for number of all tokens and types (unique tokens) and overlapping tokens and types, and the overlap percentage:

|    |   overlap percentage |   all_tokens |   overlapping_tokens |   all_types |   overlapping_types |
|:---|---------------------:|-------------:|---------------------:|------------:|--------------------:|
| mt |             0.817085 |        39040 |                31899 |        4787 |                3586 |
| el |             0.161428 |        31240 |                 5043 |        4751 |                 822 |
| tr |             0.521502 |        29578 |                15425 |        6272 |                2451 |
| sq |             0.605775 |        26769 |                16216 |        4891 |                2748 |
| is |             0.517575 |        29644 |                15343 |        4615 |                2122 |
| uk |             0.156675 |        31677 |                 4963 |        6507 |                 411 |
| ca |             0.744881 |        27544 |                20517 |        5314 |                2896 |
| mk |             0.145989 |        27639 |                 4035 |        5468 |                 656 |
| hr |             0.821517 |        26546 |                21808 |        6222 |                4383 |
| sl |             0.974289 |        26292 |                25616 |        5763 |                5281 |

Most frequent unique tokens in test sets:

|    | most_frequent_type                                                                                                                       |
|:---|:-----------------------------------------------------------------------------------------------------------------------------------------|
| ca | [(',', 1080), ('▁de', 1014), ('.', 675), ('s', 648), ('▁i', 564), ('▁la', 559), ('▁a', 529), ('▁que', 438), ("'", 360), ('’', 334)]      |
| el | [('▁', 1017), ('.', 801), (',', 782), ('▁και', 553), ('ς', 525), ('▁να', 351), ('▁το', 321), ('▁του', 292), ('▁την', 268), ('▁με', 264)] |
| hr | [(',', 878), ('.', 766), ('▁i', 546), ('▁u', 430), ('a', 413), ('▁je', 350), ('▁na', 282), ('▁za', 253), ('▁se', 239), ('e', 219)]       |
| is | [('.', 1017), ('▁og', 628), ('▁að', 613), (',', 600), ('▁', 528), ('▁í', 434), ('▁á', 388), ('▁er', 357), ('s', 326), ('▁sem', 279)]     |
| mk | [(',', 1021), ('▁на', 983), ('.', 738), ('▁и', 619), ('▁за', 475), ('▁да', 378), ('▁во', 376), ('▁се', 365), ('▁', 341), ('▁од', 324)]   |
| mt | [('-', 2119), ('ħ', 1807), (',', 884), ('.', 724), ('▁', 717), ('ġ', 519), ('▁l', 504), ('i', 466), ("'", 462), ('a', 460)]              |
| sl | [(',', 1154), ('.', 805), ('▁je', 455), ('▁in', 443), ('▁v', 373), ('▁na', 317), ('▁za', 296), ('a', 240), ('▁se', 227), ('▁da', 214)]   |
| sq | [('▁të', 890), (',', 807), ('▁e', 749), ('.', 641), ('▁në', 420), ('▁dhe', 416), ('▁me', 367), ('▁i', 307), ('t', 268), ('▁për', 266)]   |
| tr | [('.', 995), (',', 806), ('▁ve', 439), ('▁bir', 265), ("'", 244), ('n', 202), ('▁', 190), ('m', 158), ('i', 144), ('de', 143)]           |
| uk | [(',', 1352), ('.', 1031), ('▁', 531), ('▁в', 391), ('▁на', 307), ('▁і', 295), ('▁з', 284), ('▁не', 246), ('у', 239), ('і', 237)]        |


#### Label-level

We do the same as above, but separate all datasets according to genres, and calculate token overlap for each genre separatedly.

Number of tokens and types (unique tokens) in training dataset:

|                         |   token_count |   type_count |
|:------------------------|--------------:|-------------:|
| Information/Explanation |        124130 |        14678 |
| News                    |        136557 |        15319 |
| Instruction             |         83750 |         8929 |
| Opinion/Argumentation   |        103141 |        13088 |
| Forum                   |         58900 |         8555 |
| Prose/Lyrical           |         46860 |         5990 |
| Legal                   |         28496 |         4425 |
| Promotion               |         88626 |        12548 |

### Token overlap, calculated on normalized and transliterated texts

We transliterated Cyrillic and Greek script to Latin using [cyrtranslit](https://github.com/opendatakosovo/cyrillic-transliteration) and [transliterate](https://pypi.org/project/transliterate/) Python libraries. Then we also lowercased all texts and normalized all language-specific characters using the [unidecode](https://pypi.org/project/Unidecode/).

The idea of analysing normalized token overlap is in this that by transliterating all characters to Latin, we get closer to what is the semantic overlap (tokens representing units that carry meaning).

|    |   percentage |   overlap_list_size |   overlap_set_size |
|:---|-------------:|--------------------:|-------------------:|
| sl |     0.983558 |               26320 |               4485 |
| mt |     0.908776 |               35146 |               3691 |
| mk |     0.905123 |               27704 |               3293 |
| uk |     0.900191 |               31991 |               2957 |
| el |     0.895228 |               29231 |               2567 |
| hr |     0.873856 |               23588 |               3917 |
| ca |     0.810781 |               22290 |               2666 |
| is |     0.809069 |               24586 |               2447 |
| sq |     0.779926 |               21175 |               2597 |
| tr |     0.729727 |               22623 |               2468 |

### Based on cosine similarity

Another idea: we calculate cosine similarity of vectors of token distributions, comparing token distribution of train dataset with test set. For each test set, we create a list of token types that appear either in train dataset or test set. Then we create vectors of occurrences of these token types in 1) train dataset, and 2) test set. We calculate cosine similarity between these two vectors. Results:

|    |   cosine_similarity |   vector_size |
|:---|--------------------:|--------------:|
| sl |            0.633451 |         27507 |
| tr |            0.593847 |         30846 |
| uk |            0.584612 |         33121 |
| hr |            0.56621  |         28864 |
| el |            0.527321 |         30954 |
| ca |            0.525439 |         29443 |
| is |            0.525135 |         29518 |
| sq |            0.434489 |         29168 |
| mk |            0.422532 |         31837 |
| mt |            0.414248 |         28226 |

Correlation with Macro F1 (corpus level):

Pearsons correlation: 0.560
p-value: 0.0926047843840466
Spearmans correlation: 0.624
p-value: 0.053717767217167395

![](figures/correlation-token-overlap-cosine-similarity-macro-f1.png)
