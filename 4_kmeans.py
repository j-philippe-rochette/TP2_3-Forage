import sys
import pandas as pd
import random
import math

NB_CLUSTERS = 50
NB_ITERATIONS = 50
C = 1000


# INPUT: A docword-style type of file with the structure "doc_id word_id tf".
# OUTPUT: A file named "kmeans.txt" with the structure "cluster_id doc_id".
if __name__ == '__main__':
    f = sys.argv[1]
    df_doc_and_words = pd.read_csv(f, delimiter=" ").set_index('doc_id')

    # Create a dict of all the docs with a random cluster
    # Create a set of all the words
    random.seed()
    list_doc = {}
    list_word = set()
    for row in df_doc_and_words.itertuples():
        if row.Index not in list_doc:
            list_doc[row.Index] = {'cluster': random.randint(0, NB_CLUSTERS - 1)}
        if row.word_id not in list_word:
            list_word.add(row.word_id)

    df_doc_to_cluster = pd.DataFrame.from_dict(list_doc, orient='index').rename(columns={0:"cluster"})
    list_doc.clear()
    changed = True

    # Dictionary of our weights for each word in each cluster (at first, it's empty)
    dict_weights = {}

    for it in range(NB_ITERATIONS):
        if not changed:
            break
        # Calculate the mean for every cluster
        # Key = Cluster
        # Value = Dictionary with Key = Word Id and Value = TF
        dict_means = {}
        # Dictionary that will be used to calculate de standard deviation
        dict_stddev = {}
        for c in range(0, NB_CLUSTERS):
            dict_means[c] = {}
            dict_stddev[c] = {}
            # For every document in the cluster
            for doc in df_doc_to_cluster.loc[df_doc_to_cluster["cluster"] == c].index:
                # For all the words in the document
                words_in_doc = df_doc_and_words.loc[doc]['word_id'].tolist()
                if not isinstance(words_in_doc, list):
                    words_in_doc = [words_in_doc]

                for word in words_in_doc:
                    # Add the TF of the word for this cluster
                    tf = df_doc_and_words.loc[(df_doc_and_words.index == doc) &
                                              (df_doc_and_words['word_id'] == word), 'tf'].values[0]
                    if word not in dict_means[c]:
                        dict_means[c][word] = tf
                    else:
                        dict_means[c][word] += tf
                    # Add the freq of the word in the list to calculate the stddev later (when we'll have the mean)
                    if word not in dict_stddev[c]:
                        dict_stddev[c][word] = [tf]
                    else:
                        dict_stddev[c][word].append(tf)
            # Divide each of them by the number of docs in the cluster to get an average
            nb_docs_in_cluster = len(df_doc_to_cluster.loc[df_doc_to_cluster["cluster"] == c])
            sum_weights = 0
            for word, tf in dict_means[c].items():
                # Mean
                dict_means[c][word] /= nb_docs_in_cluster
                # Stddev
                if it == 0:
                    dict_weights[c] = {}
                    dict_weights[c][word] = 1
                else:
                    if c not in dict_weights:
                        dict_weights[c] = {}
                    stddev_num = 0
                    stddev_denom = 0
                    for freq in dict_stddev[c][word]:
                        stddev_denom += 1
                        stddev_num += math.pow((freq - dict_means[c][word]), 2)
                    if word in dict_weights[c]:
                        dict_weights[c][word] /= (1 + math.sqrt(stddev_num / stddev_denom))
                    else:
                        dict_weights[c][word] = 1 / (1 + math.sqrt(stddev_num / stddev_denom))
                sum_weights += math.pow(dict_weights[c][word], 2)

            # Normalization of the variance
            if c not in dict_weights:
                dict_weights[c] = {}
            if sum_weights == 0:
                continue
            for word, variance in dict_weights[c].items():
                dict_weights[c][word] = (C * variance) / math.sqrt(sum_weights)

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
                    if word in dict_weights[c]:
                        dict_calc[c] += (dict_weights[c][word] * math.pow((freq_doc - freq_cluster), 2))
                    else:
                        dict_calc[c] += math.pow((freq_doc - freq_cluster), 2)

                # For elements in the document but not in the intersection
                for word in [x for x in words_in_doc if x not in intersection]:
                    freq_doc = df_doc_and_words.loc[(df_doc_and_words.index == doc.Index) &
                                                    (df_doc_and_words['word_id'] == word), 'tf'].values[0]
                    if word in dict_weights[c]:
                        dict_calc[c] += (dict_weights[c][word] * math.pow((freq_doc), 2))
                    else:
                        dict_calc[c] += math.pow((freq_doc), 2)

                # For elements in the cluster but not in the intersection
                for word in [x for x in words_in_cluster if x not in intersection]:
                    freq_cluster = dict_means[c][word]
                    if word in dict_weights[c]:
                        dict_calc[c] += (dict_weights[c][word] * math.pow((freq_cluster), 2))
                    else:
                        dict_calc[c] += math.pow((freq_cluster), 2)

            # Change the cluster of the document
            df_calc = pd.DataFrame.from_dict(dict_calc, orient='index')
            old_cluster = df_doc_to_cluster.loc[doc.Index]['cluster']
            df_doc_to_cluster.set_value(doc.Index, 'cluster', int(df_calc.idxmin().values[0]))
            new_cluster = df_doc_to_cluster.loc[doc.Index]['cluster']
            if old_cluster != new_cluster:
               nb_change += 1
        # Create a new dataframe with the new clusters
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
