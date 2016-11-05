import sys
import pandas as pd

if __name__ == '__main__':
    # Create a dictionary with all the associations id -> new_id
    f_reduce = sys.argv[1]
    df_reduce  = pd.read_csv(f_reduce, delimiter=" ")
    dict_reduce = {}

    for row in df_reduce.itertuples():
        dict_reduce[row.id] = row.new_id

    # Replace in all docwords
    for f in sys.argv[2:]:
        df = pd.read_csv(f, delimiter=" ", encoding="iso8859_15")
        dict_doc = {}

        cpt_all = 0
        cpt_new = 0

        for row in df.itertuples():
            cpt_all += 1
            if row.doc_id not in dict_doc:
                dict_doc[row.doc_id] = {}

            new_id = dict_reduce[row.word_id]
            if row.word_id not in dict_doc[row.doc_id]:
                dict_doc[row.doc_id][new_id] = 0

            dict_doc[row.doc_id][new_id] +=  row.freq



        with open(f + ".new", "w") as output:
            for key, dict_word in dict_doc.items():
                for word, freq in dict_word.items():
                    cpt_new += 1
                    output.write("{} {} {}\n".format(key, word, freq))

        print("All: {}\tCount: {}".format(cpt_all, cpt_new))
