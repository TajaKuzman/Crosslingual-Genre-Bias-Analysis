## Token overlap

We tokenised the X-GENRE classifier training set and the test sets with XLM-RoBERTa tokenizer (as the X-GENRE classifier is based on XLM-RoBERTa). For each text, we took only the first 512 tokens, since this is also the max sequence length that can be seen by the X-GENRE classifier. We removed the starting and ending token (s, \s).

Then we calculated the overlap of the datasets, where we counter each occurrence of the token from the test set in the training set. We also calculated how many of the words that overlap are non-short - are more than 1 character long.

| language | percentage | overlap_list | non_short | non_short_per |
|---:|---:|---:|---:|---:|
| mt | 0.817085 | ▁Angel, o, ▁Che, t, ,, ▁se, ▁j, kun, d, u, ▁p... | 23083 | 0.723628 |
| el | 0.161428 | asi, asi, ,, ,, ▁Re, ception, ., ▁driver, ▁es... | 1883 | 0.373389 |
| tr | 0.521502 | ▁A, L, ▁Der, s, i, ▁ve, ▁Beli, r, leme, ▁S, h... | 11141 | 0.722269 |
| sq | 0.605775 | ▁Blog, ▁“, U, ▁kam, ▁me, jet, .”, ▁Jer, ▁31, ... | 12459 | 0.768315 |
| is | 0.517575 | ▁[, is, ], ▁er, fi, ▁reg, ▁sett, ar, lag, sin... | 10915 | 0.711399 |
| uk | 0.156675 | ., ,, ,, ?, ▁-, ., ?, ▁-, ', ., ,, ., ▁, ▁(, ... | 1258 | 0.253476 |
| ca | 0.744881 | ▁P, à, gine, s, ▁En, nada, ▁Porto, ▁uns, ▁die... | 15657 | 0.763123 |
| mk | 0.145989 | ,, ▁T, CL, ,, ▁T, CL, :, ▁Alca, tel, ▁Mobile,... | 1270 | 0.314746 |
| hr | 0.821517 | ▁O, ▁proizvod, u, ▁Color, ▁Trans, ,, ▁za, ▁pa... | 17678 | 0.810620 |
| sl | 0.974289 | ▁Kita, jsko, ▁mesto, ▁duhov, ▁V, ▁Notranj, i,... | 21567 | 0.841935 |