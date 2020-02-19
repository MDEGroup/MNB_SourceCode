
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
import glob,os
import operator
from sklearn.feature_extraction.text import TfidfVectorizer
from github_crawling.metrics import calculate_metrics
from github_crawling.crawler import map_repos2topics


def load_data(path_topic):
    #Loading the dataset
    print('Loading the dataset')
    X = []
    y = []

    for topic in os.listdir(path_topic):
        code_loc_current=path_topic+topic+'\\'
        file_list = glob.glob(os.path.join(code_loc_current, "*.txt"))
        for file_path in file_list:
            f=open(file_path,'r', encoding="utf-8", errors="ignore")
            data=f.read()

            X.append(data)
            y.append(topic)
    print(len(X))
    print(len(y))
    return X, y


def predict_topics(dirs, test_dir, train_data, labels, num_topics, list_test):
    ###Extracting features
    print('Extracting features from dataset')
    count_vect = TfidfVectorizer(input='train', stop_words={'english'}, lowercase=True, analyzer='word')
    train_vectors = count_vect.fit_transform(train_data)
    train_vectors.shape
    tfidf_transformer = TfidfTransformer()
    train_tfidf = tfidf_transformer.fit_transform(train_vectors)
    train_tfidf.shape
    print('Training a Multinomial Naive Bayes (MNB)')
    ###train model
    out_dict = {}
    clf = MultinomialNB()

    predicted_topics = {}

    l = []
    lista = []
    file = open(list_test, "r")
    data = file.readlines()
    count = 0
    for elem in data:
        if ("/" not in elem):
            l.append(count)
            count += 1
        else:
            count += 1
    index = 0

    for dir in dirs:
        for f in os.listdir(test_dir + "/" + dir):

            test = open(test_dir + "/" + dir + "/" + f, "r", encoding="utf-8", errors="ignore")
            i = 0
            list_topics = []
            # var = input("Please enter a code snippet: ")
            docs_new = [test.read()]

            X_new_counts = count_vect.transform(docs_new)
            X_new_tfidf = tfidf_transformer.transform(X_new_counts)
            predicted = clf.fit(train_tfidf, labels).predict(X_new_tfidf)
            # print(X_new_tfidf)
            # print(clf.predict_proba(X_new_tfidf))
            for prob in clf.predict_proba(X_new_tfidf):
                for cat, p in zip(clf.classes_, prob):
                    # print(cat+":"+str(p))
                    out_dict.update({cat: str(p)})
                    ranked_dict = sorted(out_dict.items(), key=operator.itemgetter(1), reverse=True)

            while i < num_topics:
                for tupla in ranked_dict:
                    # print(str(i)+" "+tupla[0])
                    list_topics.append(tupla[0])
                    #print(str(tupla))

                    i = i + 1
                    if i == num_topics:
                        predicted_topics.update({f: list_topics})
                        break




        try:

            for c in range(l[index], l[index + 1]):
                lista.append(data[c].rstrip())
        except:
            print("index out bound")
            break

        actual = map_repos2topics(lista)

        out_results = open("results_5_topics.csv", "a+", encoding="utf-8",
                           errors="ignore")
        out_results2 = open("results_2_topics.csv", "a+", encoding="utf-8",
                           errors="ignore")
        out_results3 = open("results_8.csv", "a+", encoding="utf-8",
                            errors="ignore")

        calculate_metrics(lista, out_results, out_results2, out_results3, actual, predicted_topics)

        lista = []
        index += 1
        file_csv = open("training_data.csv", "a+", encoding="utf-8", errors="ignore")
    for key, value in predicted_topics.items():
        file_csv.write(key.replace(",", "/") + "," + ",".join([str(elem) for elem in value]) + "\n")



