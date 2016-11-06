import sys
import pandas as pd

MIN_TF_IDF = 200

if __name__ == '__main__':
    f = sys.argv[1]
    df = pd.read_csv(f, delimiter=" ", encoding="iso8859_15")

    with open("docword_tf-idf_reduced.txt", "w") as output:
        output.write("doc_id word_id tf_idf\n")
        for row in df.itertuples():
            if row.tf_idf > MIN_TF_IDF:
                output

