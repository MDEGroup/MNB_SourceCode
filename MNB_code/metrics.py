from nltk.stem import PorterStemmer
import os
from distutils.dir_util import copy_tree


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


def compute_metrics(act_topics, pred_topics, out_results, repo):
    out_results.write(repo + ",")
    if act_topics:
        act_topics = remove_not_featured("topics_134.txt", act_topics)

        ##add language
        guess_list = extract_names("results1.txt")
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
        out_results.write(str(recall(pred_topics, act_topics)) + ",")
        out_results.write(str(top_rank(pred_topics, act_topics)) + "\n")


def calculate_metrics(test_dataset, out_results, out_results2, out_results3, actual, predicted):

    for repo in test_dataset:
        if repo.strip().find("/") != -1:
            ##get user topics
            act_topics, five_topics, two_topics, eight_topics = get_topics(actual, key_actual=str(repo).strip(), dict_predicted=predicted,
                                                 key_predicted= str(repo).strip().replace("/",",") + ".txt")
            compute_metrics(act_topics, five_topics,out_results,repo)
            compute_metrics(act_topics, two_topics, out_results2, repo)
            compute_metrics(act_topics, eight_topics, out_results3, repo)

        else:
            continue


def append_new_topics(file_topics,predicted):
    disc = open(file_topics, "r", encoding="utf-8", errors="ignore")
    for t in disc:
        predicted.append(t.strip())
    return predicted


def move_repos(path_train,path_dest):

    for folder in os.listdir(path_train):
        for file in os.listdir(path_train+"//"+folder):
            copy_tree(path_train+"\\"+folder+"\\"+file, path_dest+"\\"+file)


def extract_names(file_lang):

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

    return results
