import sys
import pandas as pd
import math

MIN_TF_IDF = 35
MAX_TF_IDF = 300

# INPUT: Docwords files with the structure (and first line) "doc_id word_id freq"
# OUTPUT: A file named "docwords_all.txt" with the structure "doc_id word_id tf".
#         Only keep the lines where the TF-IDF is between [MIN_TF_IDF, MAX_TF_IDF[.

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
    with open("docword_all.txt", "w") as output:
        output.write("doc_id word_id tf\n")
        for doc, dict_word in dict_tf.items():
            for word, freq in dict_word.items():
                tf_idf = dict_tf[doc][word] * math.log(N/(1 + dict_idf[word]))
                if tf_idf > MIN_TF_IDF and tf_idf <= MAX_TF_IDF:
                    output.write("{} {} {}\n".format(doc, word, dict_tf[doc][word]))

