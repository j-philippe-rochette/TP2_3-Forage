import sys
import pandas as pd
import math

if __name__ == '__main__':
    # Key= doc_id
    # Value= Dict (Key= word_id
    #              Value= freq)
    dict_tf = {}
    dict_idf = {}

    # TF
    for f in sys.argv[1:]:
        df = pd.read_csv(f, delimiter=" ", encoding="iso8859_15")
        for row in df.itertuples():
            if row.doc_id not in dict_tf:
                dict_tf[row.doc_id] = {}

            if row.word_id not in dict_tf[row.doc_id]:
                dict_tf[row.doc_id][row.word_id] = 0

            dict_tf[row.doc_id][row.word_id] += row.freq

    # IDF
    for doc, dict_word in dict_tf.items():
        for word, freq in dict_word.items():
            if word not in dict_idf:
                dict_idf[word] = 1
            else:
                dict_idf[word] += 1

    # TF-IDF
    N = len(dict_tf)
    with open("docword_tf-idf.txt", "w") as output:
        output.write("doc_id word_id tf-idf\n")
        for doc, dict_word in dict_tf.items():
            for word, freq in dict_word.items():
                tf_idf = dict_tf[doc][word] * math.log(N/(1 + dict_idf[word]))
                output.write("{} {} {}\n".format(doc, word, tf_idf))

