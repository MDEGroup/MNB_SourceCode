from github import Github
import os
import csv

#get authorization code
g = Github("your token", per_page=100)
#g = Github("claudioDsi","github17", per_page=100)


def map_repos2topics(list_repo):
    list_mapping={}
    disc=open("not_found.txt","a+",encoding="utf-8", errors="ignore")
    file_csv = open("repo_mapping.csv", "a+", encoding="utf-8", errors="ignore")

    for repo_name in list_repo:
        if repo_name.strip().find("/") != -1:
            try:
                key_repo=str(repo_name).strip()
                topics=g.get_repo(str(repo_name).strip()).get_topics()

                list_mapping.update({key_repo: topics})

                if topics:
                    file_csv.write(key_repo + ','.join([str(elem) for elem in topics]) + "\n")
                else:
                    file_csv.write("no topic \n")
                print("found topics")
            except:
                print("not found")
                disc.write(str(repo_name).strip()+"\n")

        else:
            continue

        file_csv.flush()
    return list_mapping


def get_featured_repos(num_repo,file_path):
    i=0
    out_file = open(file_path, "w", encoding="utf-8",errors="ignore")
    topics = g.search_topics(query="is:featured")
    for t in topics:
        repos = g.search_repositories(query="is:featured " + t.name)
        out_file.write(t.name+"\n")
        for r in repos:
            out_file.write(r.full_name+"\n")
            print("write file")
            i=i+1

            if i==num_repo:
                i=0
                break
        continue


def test_topic(list_repo):
    path_topic = "C:\\Users\\claudio\\Desktop\\projects\\"
    list_repo = open(list_repo, "r", encoding="utf-8", errors="ignore").readlines()
    for repo in list_repo:
        print(repo.find("/"))
        if str(repo.find("/") != -1):
            list_topic = g.get_repo(repo.strip()).get_topics()
            for topic in os.listdir(path_topic):
                if topic in list_topic:
                    f = open(path_topic + topic + "\\readmeOf-" + str(repo.replace("/", "-").strip()) + ".txt",
                             "w", encoding="utf-8",
                             errors="ignore")
                    v = g.get_repo(str(repo).strip()).get_readme().decoded_content
                    f.write(str(v))
                    print("write file")
                    print(topic)
        else:
            continue


def read_topics(list_repo):
    path_topic = "C:\\Users\\claudio\\Desktop\\github_projects\\"
    list_repo = open(list_repo, "r", encoding="utf-8", errors="ignore")
    for topic in os.listdir(path_topic):
        for repo_name in list_repo:
            list_topics=g.get_repo(str(repo_name).strip()).get_topics()
            if topic in list_topics:
                try:
                    f = open(path_topic+topic+"\\readmeOf-" + str(repo_name.replace("/", "-").strip()) + ".txt", "w", encoding="utf-8",
                             errors="ignore")
                    v = g.get_repo(str(repo_name).strip()).get_readme().decoded_content
                    f.write(str(v))
                    print("write file")
                except:
                    print("not found")

def download_readme(list_repo,path_projects):
    list_repo = open(list_repo, "r", encoding="utf-8", errors="ignore")
    not_found=open("repos_not_found.txt","w",encoding="utf-8",errors="ignore")
    for repo_name in list_repo:
        if str(repo_name).strip().find("/")!=-1:
            try:
                f =open(path_projects+topic+"\\"+str(repo_name.replace("/",",").strip())+".txt","w",encoding="utf-8", errors="ignore")
                v = g.get_repo(str(repo_name).strip()).get_readme().decoded_content
                f.write(str(v))
                print("write readMe")
            except:
                not_found.write(repo_name+"\n")
                print("not found")
        else:
            topic=str(repo_name).strip()
            continue


def write_csv(test_data_path):
    with open('source_code.csv', mode='w',newline='') as employee_file:
        writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for f in os.listdir(test_data_path):
            test = open(test_data_path + "\\" + f, "r", encoding="utf-8", errors="ignore")
            writer.writerow([test.read()])







