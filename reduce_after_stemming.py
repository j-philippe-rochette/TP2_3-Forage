#!/usr/bin/env python
import sys
import pandas as pd


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
    