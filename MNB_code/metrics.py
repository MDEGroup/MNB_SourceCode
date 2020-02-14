from nltk.stem import PorterStemmer
import os, shutil
from shutil import  copyfile
import collections, operator
from distutils.dir_util import copy_tree
from sklearn.metrics import confusion_matrix

def get_topics(dict_actual,key_actual,dict_predicted,key_predicted):
    list_actual=dict_actual.get(key_actual)
    list_predicted=dict_predicted.get(key_predicted)
    return list_actual,list_predicted[0:5], list_predicted[0:2], list_predicted[0:8]


def stemming_topics(predicted,actual):
    stemmer = PorterStemmer()
    stemmed_pred=[]
    stemmed_act=[]
    for p in predicted:
        stemmed_pred.append(stemmer.stem(p))
    for a in actual:
        stemmed_act.append(stemmer.stem(a))
    return stemmed_pred , stemmed_act


def success_rate(predicted, actual, n):
    if actual:
        match = [value for value in predicted if value in actual]
        if len(match)>=n:
            return 1
        else:
            return 0
    else:
        return -1


def precision(predicted,actual):
    if actual:
        true_p = len([value for value in predicted if value in actual])
        false_p= len([value for value in predicted if value not in actual])
        return (true_p / (true_p + false_p))*100
    else:
        return -1


def recall(predicted,actual):
    if actual:
        true_p = len([value for value in predicted if value in actual])
        false_n=len([value for value in actual if value not in predicted])
        return (true_p/(true_p + false_n))*100
    else:
        return -1


def top_rank(predicted,actual):
    top = predicted.pop(0)
    if top in actual:
        predicted.insert(0, top)
        return 1
    else:
        return 0


def remove_dashes(actual):
    result=[]
    for topic in actual:
        if topic.find("-")!=-1:
            result.append(topic.replace("-",""))
        else:
            result.append(topic)
    return result



def find_repo_names(file_in, file_to_check, file_out):
    begin=open(file_in,"r", encoding="utf-8", errors="ignore").readlines()
    to_check=open(file_to_check,"r", encoding="utf-8", errors="ignore").readlines()
    out=open(file_out,"w", encoding="utf-8", errors="ignore")

    list_begin=[]
    list_check=[]
    for line1,line2 in zip(begin,to_check):
        if line1.strip().find("/")!=-1 and line2.strip().find("/") != -1:
            if line1.strip() != line2.strip():
                out.write(line1.strip()+"\n")

def add_lang(guess_list, repo_name, list_predicted):
    for elem in guess_list:
        if elem[0] == repo_name:
            if elem[2] > str(10):
                list_predicted.pop()
                list_predicted.append(elem[1])

    return list_predicted



def preprocess_names(test_folder, test_file):

    out=open(test_file,"w", encoding="utf-8", errors="ignore")
    for topic in os.listdir(test_folder):
        out.write(topic + "\n")
        for file in os.listdir(test_folder+"\\"+topic):
            file=file.replace(".txt","")
            out.write(file.replace(",","/")+"\n")
            # else:
            #     pos=file.find("-",0,10)
            #     list_f=list(file)
            #     list_f[pos]="/"
            #     out.write("".join(list_f)+"\n")


def remove_not_featured(file_topic, actual):
    topics=open(file_topic,"r", encoding="utf-8", errors="ignore")
    discarded_topic=open("discarded_topic.txt","a+", encoding="utf-8", errors="ignore")
    list_featured=[]
    for t in topics:
        list_featured.append(t.strip())
    featured=[value for value in actual if value in list_featured]
    not_featured=[value for value in actual if value not in list_featured]
    for nf in not_featured:
        discarded_topic.write(nf+"\n")

    return featured


def compute_metrics(act_topics,pred_topics, out_results,repo):
    out_results.write(repo + ",")
    if act_topics:
        act_topics = remove_not_featured("already_downloaded.txt", act_topics)

        ##add language
        guess_list = extractNames("results1.txt")
        pred_topics = add_lang(guess_list, repo.strip(), pred_topics)
        # pred_topics=pred_topics[:len(act_topics)]
        out_results.write("actual topics [" + ','.join([str(elem) for elem in act_topics]) + "]" + "\n")
        out_results.write("predicted topics [" + ','.join([str(elem) for elem in pred_topics]) + "]" + "\n")
        pred_topics = remove_dashes(pred_topics)
        act_topics = remove_dashes(act_topics)
        pred_topics, act_topics = stemming_topics(pred_topics, act_topics)

        for x in range(1, 6):
            ##act_topics = composed_word_h(act_topics)
            out_results.write(str(success_rate(pred_topics, act_topics, x)) + ",")
        out_results.write(str(precision(pred_topics, act_topics)) + ",")
        # avg_precision += precision(pred_topics, act_topics)
        out_results.write(str(recall(pred_topics, act_topics)) + ",")
        # avg_recall+=recall(pred_topics,act_topics)
        # out_results.write(str(pred_topics[0:1]))
        out_results.write(str(top_rank(pred_topics, act_topics)) + "\n")
        # total_top += top_rank(pred_topics,act_topics)






def calculate_metrics(test_dataset, out_results, out_results2, out_results3, actual, predicted):
    # avg_precision=0.0
    # avg_recall=0.0
    # total_top=0
    # test_avg_precision=0.0
    # test_avg_recall = 0.0
    # test_avg_top_rank = 0


    for repo in test_dataset:
        if repo.strip().find("/") != -1:
            ##get user topics
            act_topics, five_topics, two_topics, eight_topics = get_topics(actual, key_actual=str(repo).strip(), dict_predicted=predicted,
                                                 key_predicted= str(repo).strip().replace("/",",") + ".txt")
            compute_metrics(act_topics, five_topics,out_results,repo)
            compute_metrics(act_topics, two_topics, out_results2, repo)
            compute_metrics(act_topics, eight_topics, out_results3, repo)

            # out_results.write(repo+",")
            # if act_topics:
            #     act_topics = remove_not_featured("already_downloaded.txt", act_topics)
            #     if flag:
            #         append_new_topics("discarded_topic.txt", pred_topics)
            #
            #
            #     ##add language
            #     guess_list=extractNames("results.txt")
            #     pred_topics = add_lang(guess_list, repo.strip(), pred_topics)
            #     #pred_topics=pred_topics[:len(act_topics)]
            #     #out_results.write("actual topics [" + ','.join([str(elem) for elem in act_topics]) + "]" + "\n")
            #     #out_results.write("predicted topics [" + ','.join([str(elem) for elem in pred_topics]) + "]" + "\n")
            #     pred_topics=remove_dashes(pred_topics)
            #     act_topics=remove_dashes(act_topics)
            #     pred_topics, act_topics = stemming_topics(pred_topics, act_topics)
            #
            #     for x in range(1,6):
            #     ##act_topics = composed_word_h(act_topics)
            #         out_results.write(str(success_rate(pred_topics, act_topics,x)) + ",")
            #     out_results.write(str(precision(pred_topics, act_topics)) + ",")
            #     #avg_precision += precision(pred_topics, act_topics)
            #     out_results.write(str(recall(pred_topics, act_topics)) + ",")
            #     #avg_recall+=recall(pred_topics,act_topics)
            #     #out_results.write(str(pred_topics[0:1]))
            #     out_results.write(str(top_rank(pred_topics,act_topics)) + "\n")
            #     #total_top += top_rank(pred_topics,act_topics)

        else:
            #out_results.write("------------------------------" + "\n")
            #out_results.write(repo)
            continue
    # if len(actual)> 0:
    #     # out_results.write("avg precision: " + str(avg_precision/ len(actual))+"\n")
    #     # out_results.write("avg recall: " + str(avg_recall / len(actual)) + "\n")
    #     # out_results.write("top rank ratio: " + str(total_top * len(actual)) + "\n")
    #
    #     test_avg_precision += avg_precision
    #     test_avg_recall += avg_recall
    #     test_avg_top_rank += total_top





# def ten_folder(path_train,path_dest,cut,copy):
#
#     i=0
#
#     for file in sorted(os.listdir(path_train), key=lambda v: v.upper()):
#         print(file)
#         i = i + 1
#         if not copy:
#             shutil.move(path_train+file, path_dest+file)
#         else:
#             copyfile(path_train+file, path_dest+file)
#         if i == cut:
#             i = 0
#             break
#         continue
#

# def count_no_fet_topics(file):
#     disc=open(file,"r",encoding="utf-8",errors="ignore")
#     #print(Counter(disc.readlines()))
#     c= collections.Counter(disc.readlines())
#     for key, value in sorted(c.items(), key=operator.itemgetter(1),reverse=True):
#         print(key.strip()+ ": "+ str(value))


# def sort_repos(file_in, file_out):
#     begin=open(file_in,"r", encoding="utf-8", errors="ignore")
#     out=open(file_out,"w", encoding="utf-8", errors="ignore")
#     for repo in sorted(begin.readlines(), key=lambda v: v.upper()):
#         out.write(repo.strip()+"\n")


# def move_test_set(file_in, file_out):
#     begin = open(file_in, "r", encoding="utf-8", errors="ignore")
#     out = open(file_out, "w", encoding="utf-8", errors="ignore")
#     temp= open("temp.txt", "w", encoding="utf-8", errors="ignore")
#     n=10
#     # i=0
#     # temp_list=[]
#     # begin.seek(0)
#     # for repo in begin.readlines():
#     #     #out.write(repo.strip()+"\n")
#     #
#     #     temp_list.append(repo.strip())
#     #     i=i+1
#     #     if i == 10:
#     #         for s in temp_list:
#     #             out.write(s+"\n")
#     #
#     # for left in [value for value in temp_list if value not in begin.read().splitlines()]:
#     #     temp.write(left+"\n")
#     with open(file_in) as f:
#         mylist = f.read().splitlines()
#
#     newlist = mylist[:n]
#     for elem in newlist:
#         out.write(elem+"\n")
#
#     #os.remove(file_in)
#
#     thefile = open(file_in, 'w')
#
#     del mylist[:n]
#
#     for item in mylist:
#         thefile.write("%s\n" % item)


def append_new_topics(file_topics,predicted):
    disc = open(file_topics, "r", encoding="utf-8", errors="ignore")
    for t in disc:
        predicted.append(t.strip())
    return predicted
### copy=True mv=False


#actual=["phoenix","java","big-data","database","sql"]
#remove_not_fetured("already_downloaded.txt",actual)


# def tests_for_ten_folder():
#     sort_repos("discarded_topic.txt","ordered_list.txt")
#     for x in range(1,11):
#         print(x)
#         move_test_set("ordered_list.txt","C:\\Users\\claudio\\Desktop\\test_repo\\monitoring\\test"+str(x)+".txt")
# #count_no_fet_topics("discarded_topic.txt")





# def ultimate_ten_folder():
# ### ten folder validation
#     path1="C:\\Users\\claudio\\Desktop\\projects_new_dataset\\"
#     path2="C:\\Users\\claudio\\Desktop\\half_50"
#     #
#     for t in os.listdir(path1):
#         ##group1
#         ten_folder(path1 + t + "\\", path2 + "\\root\\"+t+"\\", 50, True)
#         ten_folder(path2+"\\root\\"+t+"\\",path2+"\\test1\\"+t+"\\",5, False)
#         ten_folder(path2 + "\\root\\" + t + "\\", path2 + "\\train1\\" + t + "\\", 45, True)
#         ten_folder(path2+"\\train1\\"+t+"\\",path2+"\\temp\\"+t+"\\",45, True)
#         # ##group2
#         ten_folder(path2 + "\\temp\\" + t + "\\", path2 + "\\test2\\" + t + "\\", 5, False)
#         ten_folder(path2 + "\\temp\\" + t + "\\", path2 + "\\train2\\" + t + "\\",40 , True)
#         ten_folder(path2 + "\\test1\\" + t + "\\", path2 + "\\train2\\" + t + "\\", 5, True)
#         # #group3
#         ten_folder(path2 + "\\temp\\" + t + "\\", path2 + "\\test3\\" + t + "\\", 5, False)
#         ten_folder(path2 + "\\temp\\" + t + "\\", path2 + "\\train3\\" + t + "\\", 35, True)
#         ten_folder(path2 + "\\test1\\" + t + "\\", path2 + "\\train3\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test2\\" + t + "\\", path2 + "\\train3\\" + t + "\\", 5, True)
#         # ##group4
#         ten_folder(path2 + "\\temp\\" + t + "\\", path2 + "\\test4\\" + t + "\\", 5, False)
#         ten_folder(path2 + "\\temp\\" + t + "\\", path2 + "\\train4\\" + t + "\\", 30, True)
#         ten_folder(path2 + "\\test1\\" + t + "\\", path2 + "\\train4\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test2\\" + t + "\\", path2 + "\\train4\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test3\\" + t + "\\", path2 + "\\train4\\" + t + "\\", 5, True)
#
#         # ##group5
#         ten_folder(path2 + "\\temp\\" + t + "\\", path2 + "\\test5\\" + t + "\\", 5, False)
#         ten_folder(path2 + "\\temp\\" + t + "\\", path2 + "\\train5\\" + t + "\\", 25, True)
#         ten_folder(path2 + "\\test1\\" + t + "\\", path2 + "\\train5\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test2\\" + t + "\\", path2 + "\\train5\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test3\\" + t + "\\", path2 + "\\train5\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test4\\" + t + "\\", path2 + "\\train5\\" + t + "\\", 5, True)
#         #
#         # ##group6
#         ten_folder(path2 + "\\temp\\" + t + "\\", path2 + "\\test6\\" + t + "\\", 5, False)
#         ten_folder(path2 + "\\temp\\" + t + "\\", path2 + "\\train6\\" + t + "\\", 20, True)
#         ten_folder(path2 + "\\test1\\" + t + "\\", path2 + "\\train6\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test2\\" + t + "\\", path2 + "\\train6\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test3\\" + t + "\\", path2 + "\\train6\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test4\\" + t + "\\", path2 + "\\train6\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test5\\" + t + "\\", path2 + "\\train6\\" + t + "\\", 5, True)
#         # ##group7
#         ten_folder(path2 + "\\temp\\" + t + "\\", path2 + "\\test7\\" + t + "\\", 5, False)
#         ten_folder(path2 + "\\temp\\" + t + "\\", path2 + "\\train7\\" + t + "\\", 15, True)
#         ten_folder(path2 + "\\test1\\" + t + "\\", path2 + "\\train7\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test2\\" + t + "\\", path2 + "\\train7\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test3\\" + t + "\\", path2 + "\\train7\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test4\\" + t + "\\", path2 + "\\train7\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test5\\" + t + "\\", path2 + "\\train7\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test6\\" + t + "\\", path2 + "\\train7\\" + t + "\\", 5, True)
#
#         # ##group8
#         ten_folder(path2 + "\\temp\\" + t + "\\", path2 + "\\test8\\" + t + "\\", 5, False)
#         ten_folder(path2 + "\\temp\\" + t + "\\", path2 + "\\train8\\" + t + "\\", 10, True)
#         ten_folder(path2 + "\\test1\\" + t + "\\", path2 + "\\train8\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test2\\" + t + "\\", path2 + "\\train8\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test3\\" + t + "\\", path2 + "\\train8\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test4\\" + t + "\\", path2 + "\\train8\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test5\\" + t + "\\", path2 + "\\train8\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test6\\" + t + "\\", path2 + "\\train8\\" + t + "\\",5, True)
#         ten_folder(path2 + "\\test7\\" + t + "\\", path2 + "\\train8\\" + t + "\\", 5, True)
#
#         # ##group9
#         ten_folder(path2 + "\\temp\\" + t + "\\", path2 + "\\test9\\" + t + "\\", 5, False)
#         ten_folder(path2 + "\\temp\\" + t + "\\", path2 + "\\train9\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test1\\" + t + "\\", path2 + "\\train9\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test2\\" + t + "\\", path2 + "\\train9\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test3\\" + t + "\\", path2 + "\\train9\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test4\\" + t + "\\", path2 + "\\train9\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test5\\" + t + "\\", path2 + "\\train9\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test6\\" + t + "\\", path2 + "\\train9\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test7\\" + t + "\\", path2 + "\\train9\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test8\\" + t + "\\", path2 + "\\train9\\" + t + "\\", 5, True)
#
#         # ##group10
#         ten_folder(path2 + "\\temp\\" + t + "\\", path2 + "\\test10\\" + t + "\\", 5, False)
#         #ten_folder(path2 + "\\temp\\" + t + "\\", path2 + "\\train9\\" + t + "\\", 0, True)
#         ten_folder(path2 + "\\test1\\" + t + "\\", path2 + "\\train10\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test2\\" + t + "\\", path2 + "\\train10\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test3\\" + t + "\\", path2 + "\\train10\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test4\\" + t + "\\", path2 + "\\train10\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test5\\" + t + "\\", path2 + "\\train10\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test6\\" + t + "\\", path2 + "\\train10\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test7\\" + t + "\\", path2 + "\\train10\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test8\\" + t + "\\", path2 + "\\train10\\" + t + "\\", 5, True)
#         ten_folder(path2 + "\\test9\\" + t + "\\", path2 + "\\train10\\" + t + "\\", 5, True)


def move_repos(path_train,path_dest):

    for folder in os.listdir(path_train):
        for file in os.listdir(path_train+"//"+folder):
            copy_tree(path_train+"\\"+folder+"\\"+file, path_dest+"\\"+file)


def extractNames(file_lang):

    f = open(file_lang, "r", encoding="utf-8", errors="ignore")
    results = []
    result = []
    guessLangResults = f.readlines()
    for elem in guessLangResults:
        if("/" in elem):
            result = []
            result.append(elem.rstrip())
        if("({" in elem):
            index = elem.find("'")+1
            findex = elem.find("'", index)
            lang = elem[index:findex]

            if lang=="C++":
                lang="cpp"
            elif lang=="C#":
                lang="csharp"
            result.append(lang.lower())


            index = elem.find(":", findex)+2
            findex = elem.find(",", index)
            occor = elem[index:findex]
            result.append(occor)
            results.append(result)

    print(results)
    return results



# def split_metrics(file_in, file_precision, file_recall, file_top):
#     f=open(file_in, "r")
#     out_precision=open(file_precision,"w")
#
#     for line in f:
#         if line.find("no") != -1:
#             out_precision.write(line.strip() + "\n")
#



# def create_topics_folder(root,file_topic):
#     list_folders= open(file_topic,"r", encoding="utf-8", errors="ignore")
#     print(root)
#     list_topic="C:\\Users\\claudio\\Desktop\\projects_new_dataset\\"
#     for folder in os.listdir(root):
#         print(folder)
#         for f in os.listdir(list_topic):
#
#             try:
#                 #print("no")
#                 os.mkdir(os.path.join(root,folder,str(f).strip()))
#             except:
#                 print("already created")
# begin="C:\\Users\\claudio\\Desktop\\projects_100_readme_ConfB\\"
# begin2="C:\\Users\claudio\\Desktop\\ten_folder_135\\"
# end="C:\\Users\claudio\\Desktop\\ten_folder_135\\"
#
# for topic in os.listdir(begin):
#     for x in range(1, 11):
#         print(x)
#         copy_tree(begin, end+topic+"\\train"+str(x)+"\\")

#split_metrics("C:\\Users\\claudio\\Desktop\\topics_134.txt","left.txt", "recall_test2.csv", "top_test2.csv")
# for x in range(1,11):
#     print(x)
#     preprocess_names("C:\\Users\\claudio\\Desktop\\half_50\\test"+str(x)+"\\","half_"+str(x)+".txt")
# #move_repos("D:\\crawledRepository","D:\\MSR_repo")
#ultimate_ten_folder()

# list_predicted = ["3d", "unity", "game-engine", "aws"]
# guess_langs=[["usr/repo","cpp",49], ["another/repo", "java", 30]]
# repo_to_guess="usr/repo"
# print(add_lang(guess_langs, repo_to_guess, list_predicted))
#create_topics_folder("C:/Users/claudio/Desktop/half_50", "10_folder.txt")
#extractNames("results.txt")