
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
import glob,os
import operator
from sklearn.feature_extraction.text import TfidfVectorizer
from github_crawling.metrics import calculate_metrics
from github_crawling.crawler import map_repos2topics

import pickle

def load_data(path_topic):
    #Loading the dataset
    print('Loading the dataset')
    X = []
    y = []
    #projects_path'C:\\Users\\claudio\\Desktop\\github_projects\\'
    #name_file= ['c', 'c#', 'c++','java', 'css', 'haskell', 'html', 'java', 'javascript', 'lua', 'objective-c', 'perl', 'php', 'python','ruby', 'r', 'scala', 'sql', 'swift', 'vb.net','markdown','bash']
    #name_file = ["English", "Italian", "Jazz", "Metal", "Rock", "readMe"]
    #name_file =['google', 'apache', 'others']

    #path_topic = "C:\\Users\\claudio\\Desktop\\projects_50_readme\\"

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


# def create_tfidf_dumps(train_set, test_data_path):
#     print('Vectorize from train set')
#     count_vect = TfidfVectorizer(input='train', stop_words={'english'}, lowercase=True, analyzer='word')
#     train_vectors = count_vect.fit_transform(train_set)
#     train_vectors.shape
#     tfidf_transformer = TfidfTransformer()
#     train_tfidf = tfidf_transformer.fit_transform(train_vectors)
#     train_tfidf.shape
#
#     print("Saving train dump")
#     with open('train.pickle', 'wb') as fin:
#         pickle.dump(train_vectors, fin)
#
#     print("Vectorize test set")
#     for topic in os.listdir(test_data_path):
#         print(topic)
#         for f in os.listdir(test_data_path+topic):
#             test=open(test_data_path+topic+"\\"+f,"r",encoding="utf-8",errors="ignore")
#             #var = input("Please enter a code snippet: ")
#             docs_new = [test.read()]
#             #create_test_dump(docs_new)
#             X_new_counts = count_vect.transform(docs_new)
#             X_new_tfidf = tfidf_transformer.transform(X_new_counts)
#             print("Saving test dump")
#             with open('test.pickle', 'wb') as fil:
#                 pickle.dump(X_new_tfidf, fil)



# def predict_topics(train_data,labels, test_data_path, num_topics):
#     ###Extracting features
#     print('Extracting features from dataset')
#     count_vect = TfidfVectorizer(input ='train',stop_words = {'english'},lowercase=True,analyzer ='word')
#     train_vectors = count_vect.fit_transform(train_data)
#     train_vectors.shape
#     tfidf_transformer = TfidfTransformer()
#     train_tfidf = tfidf_transformer.fit_transform(train_vectors)
#     train_tfidf.shape
#     # with open('train.pickle', 'wb') as fin:
#     #      pickle.dump(train_vectors, fin)
#     print('Training a Multinomial Naive Bayes (MNB)')
#     ###train model
#     out_dict={}
#     #feature_extraction(train_data)
#     clf = MultinomialNB()
#
#     predicted_topics = {}
#
#     for f in os.listdir(test_data_path):
#         test=open(test_data_path+"\\"+f,"r",encoding="utf-8",errors="ignore")
#         i=0
#         list_topics = []
#         #var = input("Please enter a code snippet: ")
#         docs_new = [test.read()]
#         #create_test_dump(docs_new)
#         X_new_counts = count_vect.transform(docs_new)
#         X_new_tfidf = tfidf_transformer.transform(X_new_counts)
#         #
#         # with open('test.pickle', 'wb') as fin:
#         #     pickle.dump(X_new_tfidf, fin)
#
#         #file_train = open('train.pickle', 'rb')
#         #file_test = open('test.pickle', 'rb')
#         # dump information to that file
#         # train_tfidf = pickle.load(file_train)
#         # X_new_tfidf = pickle.load(file_test)
#         clf.fit(train_tfidf,labels).predict(X_new_tfidf)
#         #print(X_new_tfidf)
#         #print(clf.predict_proba(X_new_tfidf))
#         for prob in clf.predict_proba(X_new_tfidf):
#             for cat,p in zip(clf.classes_,prob):
#                 #print(cat+":"+str(p))
#                 out_dict.update({cat: str(p)})
#                 ranked_dict=sorted(out_dict.items(), key=operator.itemgetter(1), reverse=True)
#         # for tupla in ranked_dict:
#         #     print(tupla)
#         while i<num_topics:
#             for tupla in ranked_dict:
#                 #print(str(i)+" "+tupla[0])
#                 list_topics.append(tupla[0])
#                 i=i+1
#                 if i == num_topics:
#                     predicted_topics.update({f: list_topics})
#                     break
#     return predicted_topics

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

    #test_dir = "C:\\Users\\claudio\\Desktop\\ten_folder_validation\test5"
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
        # list_repo = open(test_file, "r", encoding="utf-8", errors="ignore")
        out_results = open("results_5_topics.csv", "a+", encoding="utf-8",
                           errors="ignore")
        out_results2 = open("results_2_topics.csv", "a+", encoding="utf-8",
                           errors="ignore")
        out_results3 = open("results_8_2.csv", "a+", encoding="utf-8",
                            errors="ignore")

        calculate_metrics(lista,out_results,out_results2,out_results3, actual, predicted_topics)

        lista = []
        index += 1
        file_csv = open("training_data.csv", "a+", encoding="utf-8", errors="ignore")
    for key, value in predicted_topics.items():
        file_csv.write(key.replace(",", "/") + "," + ",".join([str(elem) for elem in value]) + "\n")



#print("probabilties", clf.predict_proba(X_new_tfidf))