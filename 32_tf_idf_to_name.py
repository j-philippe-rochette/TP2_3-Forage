import sys
import pandas as pd

# INPUT: First file is a word file with the structure "id word".
#        Second file is a docword file with the structure "doc_id word_id {tf_idf or tf}"
# OUTPUT: Print the same docword but the id_word is replaced by the word itself.
if __name__ == '__main__':
    f_name = sys.argv[1]
    df_name = pd.read_csv(f_name, delimiter=" ", encoding="iso8859_15")

    dict_name = {}
    for row in df_name.itertuples():
        dict_name[row.id] = row.word

    f_tf_idf = sys.argv[2]
    df_tf_idf = pd.read_csv(f_tf_idf, delimiter=" ", encoding="iso8859_15")

    list_word = {}
    for row in df_tf_idf.itertuples():
        if row.word_id not in list_word:
            list_word[row.word_id] = 1

    for key, value in list_word.items():
        print(dict_name[key])

    print(len(list_word))
