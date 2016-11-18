import sys
import pandas as pd


# INPUT: At first, a file with the structure "cluster_id doc_id".
#        Then all "doctitles.txt" files that starts with the line "doc_id	title". The delimiter is a tab.
# OUTPUT: Print on the output, for each clusters, the title of the documents that are in it.
#         Also print the number of documents in each cluster.
if __name__ == '__main__':
    f_clusters = sys.argv[1]
    df_clusters = pd.read_csv(f_clusters, delimiter=" ")

    dict_docs = {}
    for f in sys.argv[2:]:
        df = pd.read_csv(f, delimiter="\t", encoding="iso8859_15")
        for row in df.itertuples():
            dict_docs[row.doc_id] = row.title

    num_doc = {}
    last_cluster = 0
    for row in df_clusters.itertuples():
        if row.cluster_id != last_cluster:
            num_doc[last_cluster] = len(df_clusters.loc[df_clusters["cluster_id"] == last_cluster])
            print("-------------------------------------------------------------------------------------------------\n")
            last_cluster = row.cluster_id
        if row.doc_id in dict_docs:
            print("{} {}".format(row.cluster_id, dict_docs[row.doc_id]))
        else:
            print("{} not in dictionary.".format(row.doc_id))
    num_doc[last_cluster] = len(df_clusters.loc[df_clusters["cluster_id"] == last_cluster])
    print("\n-------------------------------------------------------------------------------------------------\n")
    for c, nb_doc in num_doc.items():
        print("Number of documents in cluster {}:\t{}".format(c, nb_doc))