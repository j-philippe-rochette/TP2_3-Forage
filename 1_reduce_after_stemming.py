#!/usr/bin/env python
import sys
import pandas as pd


# INPUT: File with all the words after Porter Stemming
# OUTPUT: File with {id of the word} {new id of the word}
if __name__ == '__main__':
    f = sys.argv[1]
    df = pd.read_csv(f, delimiter=" ", encoding="iso8859_15")
    dict_words = {}
    for row in df.itertuples():
        if row.word in dict_words:
            print("{} {}".format(row.id, dict_words[row.word]))
        else:
            dict_words[row.word] = row.id
            print("{} {}".format(row.id, row.id))
    