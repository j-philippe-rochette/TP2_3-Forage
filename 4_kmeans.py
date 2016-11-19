import sys
import pandas as pd
import random
import math

NB_CLUSTERS = 100
NB_ITERATIONS = 50 


# INPUT: A docword-style type of file with the structure "doc_id word_id tf".
# OUTPUT: A file named "kmeans.txt" with the structure "cluster_id doc_id".
if __name__ == '__main__':
    f = sys.argv[1]
    df_doc_and_words = pd.read_csv(f, delimiter=" ").set_index('doc_id')

    # Create a list of all the docs with a random cluster
    # Create a set of all the words
    random.seed()
    list_doc = {}
    list_word = set()
    for row in df_doc_and_words.itertuples():
        if row.Index not in list_doc:
            list_doc[row.Index] = {'cluster': random.randint(0, NB_CLUSTERS)}
        if row.word_id not in list_word:
            list_word.add(row.word_id)

    df_doc_to_cluster = pd.DataFrame.from_dict(list_doc, orient='index').rename(columns={0:"cluster"})
    list_doc.clear()
    changed = True

    for it in range(NB_ITERATIONS):
        if not changed:
            break
        # Calculate the mean for every cluster
        # Key = Cluster
        # Value = Dictionary with Key = Word Id and Value = TF
        dict_means = {}
        for c in range(0, NB_CLUSTERS):
            dict_means[c] = {}
            # For every document in the cluster
            for doc in df_doc_to_cluster.loc[df_doc_to_cluster["cluster"] == c].index:
                # For all the words in the document
                words_in_doc = df_doc_and_words.loc[doc]['word_id'].tolist()
                if not isinstance(words_in_doc, list):
                    words_in_doc = [words_in_doc]

                for word in words_in_doc:
                    # Add the TF for the word for this cluster
                    tf = df_doc_and_words.loc[(df_doc_and_words.index == doc) &
                                              (df_doc_and_words['word_id'] == word), 'tf'].values[0]
                    if word not in dict_means[c]:
                        dict_means[c][word] = tf
                    else:
                        dict_means[c][word] += tf
            nb_docs_in_cluster = len(df_doc_to_cluster.loc[df_doc_to_cluster["cluster"] == c])
            for word, tf in dict_means[c].items():
                dict_means[c][word] = dict_means[c][word] / nb_docs_in_cluster

        # Change the cluster of each document for the one with the mean resembling it the most
        # For all documents
        nb_change = 0
        for doc in df_doc_to_cluster.itertuples():
            # For all clusters
            dict_calc = {}
            for c in range(0, NB_CLUSTERS):
                dict_calc[c] = 0

                words_in_doc = df_doc_and_words.loc[doc.Index]['word_id'].tolist()
                if not isinstance(words_in_doc, list):
                    words_in_doc = [words_in_doc]

                words_in_cluster = list(dict_means[c].keys())

                # For elements in both
                intersection = list(set(words_in_doc) & set(words_in_cluster))
                for word in intersection:
                    freq_doc = df_doc_and_words.loc[(df_doc_and_words.index == doc.Index) &
                                                    (df_doc_and_words['word_id'] == word), 'tf'].values[0]
                    freq_cluster = dict_means[c][word]
                    dict_calc[c] += math.pow((freq_doc - freq_cluster), 2)

                # For elements in the document but not in the intersection
                for word in [x for x in words_in_doc if x not in intersection]:
                    freq_doc = df_doc_and_words.loc[(df_doc_and_words.index == doc.Index) &
                                                    (df_doc_and_words['word_id'] == word), 'tf'].values[0]
                    dict_calc[c] += math.pow((freq_doc), 2)

                # For elements in the cluster but not in the intersection
                for word in [x for x in words_in_cluster if x not in intersection]:
                    freq_cluster = dict_means[c][word]
                    dict_calc[c] += math.pow((freq_cluster), 2)

            # Change the cluster of the document
            df_calc = pd.DataFrame.from_dict(dict_calc, orient='index')
            old_cluster = df_doc_to_cluster.loc[doc.Index]['cluster']
            df_doc_to_cluster.set_value(doc.Index, 'cluster', int(df_calc.idxmin().values[0]))
            new_cluster = df_doc_to_cluster.loc[doc.Index]['cluster']
            if old_cluster != new_cluster:
                nb_change += 1
        print("For iteration {}, {} were changed.".format(it, nb_change))
        if nb_change == 0:
            changed = False

    # Print the results
    with open("kmeans.txt", "w") as output:
        output.write("cluster_id doc_id\n")
        for c in range(0, NB_CLUSTERS):
            # For every document in the cluster
            for doc in df_doc_to_cluster.loc[df_doc_to_cluster["cluster"] == c].index:
                output.write("{} {}\n".format(c, doc))



