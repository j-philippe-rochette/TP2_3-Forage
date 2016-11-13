import sys
import pandas as pd
import matplotlib.pyplot as plt

# INPUT: A docword file with the structure "doc_id word_id tf". Not part of the main algorithm.
if __name__ == '__main__':
    f = sys.argv[1]
    df = pd.read_csv(f, delimiter=" ", encoding="iso8859_15")
    df_short = df['tf']

    print(df_short.quantile([0, 0.25, 0.5, 0.75, 1]))
    print(len(df_short.index))

    list_doc = {}
    list_word = {}
    for row in df.itertuples():
        if row.doc_id not in list_doc:
            list_doc[row.doc_id] = 1
        if row.word_id not in list_word:
            list_word[row.word_id] = 1

    print("# of doc: {}\t# of words: {}".format(len(list_doc), len(list_word)))

    #df_short.plot(kind="hist", bins=1000)

    #plt.show()
