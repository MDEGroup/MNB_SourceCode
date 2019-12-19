from github_crawling.SCC import load_data,predict_topics, create_tfidf_dumps, predict_topics2
from github_crawling.metrics import calculate_metrics, preprocess_names, find_repo_names
from github_crawling.loader import map_repos2topics
import os

main_f= False


train_dir = "C:\\Users\\claudio\\Desktop\\ten_folder_50\\train1\\"
test_dir = "C:\\Users\\claudio\\Desktop\\ten_folder_50\\test1\\"
#count_vect = TfidfVectorizer(input='train', stop_words={'english'}, lowercase=True, analyzer='word')

dirs = os.listdir(test_dir)

    # if main_f:
    #     train_data, train_labels=load_data("C:\\Users\\claudio\\Desktop\\ten_folder_validation\\train1\\")
    #     predicted = predict_topics(train_data,train_labels,test_data_path="C:\\Users\\claudio\\Desktop\\ten_folder_validation\\test1\\"+topic+"\\",num_topics=5)
    #     test_file="temp.txt"
    #     actual=map_repos2topics(test_file)
    #     list_repo = open(test_file,"r",encoding="utf-8", errors="ignore")
    #     out_results=open("results_ten_folder_langs_confB_no_langs.txt", "a+", encoding="utf-8",errors="ignore")
    #     calculate_metrics(list_repo,out_results,actual,predicted,False)

if main_f:
    train_data, train_labels = load_data(train_dir)


    l = []
    lista = []
    file = open("test2_list.txt", "r")
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
        try:
            for c in range(l[index], l[index + 1]):
                lista.append(data[c].rstrip())
        except:
            break
        predicted = predict_topics(train_data, train_labels, test_data_path=test_dir + "/" + dir, num_topics=5)
        print(lista)
        print("\n")
        actual = map_repos2topics(lista)
        #list_repo = open(lista,"r",encoding="utf-8", errors="ignore")


        out_results=open("results_ten_folder_no_langs.txt", "a+", encoding="utf-8",errors="ignore")
        precision, recall, top = calculate_metrics(lista,out_results, actual,predicted,False)

        print("writing metrics")
        lista = []
        index += 1


else:
    # train_data, train_labels = load_data(train_dir)
    # create_tfidf_dumps(train_data, test_dir)
    # path="C:\\Users\\claudio\\Desktop\\test_dataset"
    #
    # #preprocess_names("C:\\Users\\claudio\\Desktop\\test_dataset\\")
    # find_repo_names("test_featured_10.txt","featured_repo_crawled.txt", "app.txt")
    train_data, train_labels = load_data(train_dir)
    predict_topics2(dirs, test_dir, train_data, train_labels, 20)



