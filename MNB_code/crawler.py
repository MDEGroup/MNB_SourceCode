from github import Github
import os
import csv

from pygit2 import clone_repository


#get authorization code
g = Github("claudioDsi","github17", per_page=100)

g3= Github("a3d3c26c8cf3683b1c18559051429f6cc6ecfb1f",per_page=100)
g4 = Github("391fa11a36c42f30d7d7147f2199a561fe131ecc", per_page=100)

# def get_langs(path):
#     file=open(path, "r")
#     ### comparison lang
#     writer = open("android_dataset.csv", "a+", encoding="utf-8", errors="ignore")
#     for repo in file.readlines():
#         writer.write(repo.strip() + ",")
#         print(repo)
#         try:
#             langs=g.get_repo(repo.strip()).get_languages().keys()
#             writer.write(','.join([str(elem) for elem in langs])+ "\n")
#             print("found langs")
#         except:
#             print("not found")
#             writer.write("not found" + "\n")
#         writer.flush()




# def get_issue():
#     out=open("pom_file.txt", "w", encoding="utf-8", errors="ignore")
#     content = g3.get_repo("claudioDsi/APIMaterials").get_contents(path="Simian")
#     for file in content:
#         print(file.name)
#         if str(file.name)=="pom.xml":
#             out.write(str(file.decoded_content).rstrip().replace("'b","").replace("\n","").replace("\t",""))
#
#     #print(content)




# def get_featured_repos_2(num_repo,file_path,list_topic):
#     i=0
#     out_file= open(file_path, "a+", encoding="utf-8",errors="ignore")
#     #find repos for a specifc topic
#     topics = open(list_topic,"r", encoding="utf-8",errors="ignore")
#
#     for t in topics:
#         repos = g.search_repositories(query="is:featured topic:"+t+" stars:100..80000 topics:>=2")
#         out_file.write(t.strip()+"\n")
#         #out_file.write(t.name+"\n")
#         for r in repos:
#             out_file.write(r.full_name+"\n")
#             print("write file")
#             i=i+1
#
#             if i==num_repo:
#                 i=0
#                 break
#         continue



def map_repos2topics(list_repo):
    list_mapping={}
    disc=open("not_found.txt","a+",encoding="utf-8", errors="ignore")
    #list_repo = open(file_test,"r",encoding="utf-8", errors="ignore")
    file_csv = open("repo_mapping.csv", "a+", encoding="utf-8", errors="ignore")

    for repo_name in list_repo:
        file_csv.write(repo_name.strip() + ",")
        try:
            key_repo=str(repo_name).strip()
            topics=g4.get_repo(str(repo_name).strip()).get_topics()

            if topics:
                file_csv.write(','.join([str(elem) for elem in topics]) + "\n")
            else:
                file_csv.write("no topic \n")
            #list_mapping.update({key_repo:topics})
            print("found topics")
        except:
            print("not found")
            disc.write(str(repo_name).strip()+"\n")

        file_csv.flush()

    # for key,value in list_mapping.items():
    #     file_csv.write(key+","+",".join([str(elem) for elem in value])+"\n")

    return list_mapping





def get_featured_repos(num_repo,file_path):
    i=0
    out_file= open(file_path, "w", encoding="utf-8",errors="ignore")
    #find repos for a specifc topic
    topics = g.search_topics(query="is:featured")
    for t in topics:
        repos = g.search_repositories(query="is:featured " + t.name)
        out_file.write(t.name+"\n")
        #out_file.write(t.name+"\n")
        for r in repos:
            out_file.write(r.full_name+"\n")
            print("write file")
            i=i+1

            if i==num_repo:
                i=0
                break
        continue


#topic_file = open("list_topic.txt","w",encoding="utf-8", errors="ignore")


# def get_java_projects(list_repo):
#     repos_java = g.search_repositories(query="language:java topics:<=5")
#     i=0
#     flag=False
#     file= open(list_repo,"w", encoding="utf-8", errors="ignore")
#     while i<=100:
#         for j in repos_java:
#             file.write(j.full_name+ "\n")
#             i=i+1
#             if i==100:
#                 flag = True
#             if flag:
#                 break
#



def test_topic(list_repo):
    path_topic = "C:\\Users\\claudio\\Desktop\\projects\\"
    list_repo = open(list_repo, "r", encoding="utf-8", errors="ignore").readlines()
    #list_topic=g.get_repo("YoKeyword/Fragmentation").get_topics()
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
            # var = input("Please enter a code snippet: ")
            #docs_new = [test.read()]


# def download_repos(file):
#     begin=open(file, "r", encoding="utf-8", errors="ignore")
#     # out=open("msr_list.txt", "w", encoding="utf-8", errors="ignore")
#     #
#     # for l in begin:
#     #     l = ''.join([i for i in l if not i.isdigit()])
#     #     out.write(l)
#     for line in begin:
#         url = os.path.join("git://", str(line.strip()) + ".git")
#         out_path="D:\\crawledRepository\\"+str()
#         print(url)
#         clone_repository(url,out_path)







# file_repos=open("CF_repos.txt", "r")
# map_repos2topics(file_repos)

#repos_category("list_java_repo.txt","map_to_topics.txt")
#create_topics_folder("C:/Users/claudio/Desktop/github_projects","list_topic.txt")
#test_topic("list_java_repo.txt")
# for t in topics:
#     print(t.name)
#     repos= g.search_repositories(query="is:featured "+t.name)
#     for r in repos:
#         print(r.full_name)
#     #clone repo
#     repo = g.get_repo(r.full_name)
#     url = os.path.join("https://github.com/",str(repo.full_name)+".git")
#     out_path="D:\\crawledRepository\\"+str(repo.name)
#     print(url)
#     cloning=clone_repository(url,out_path)


#v = repo.get_contents("DEPLOY.md").decoded_content
#print(v)


#get_issue()
#get_featured_repos_2(100,"test_featured_10.txt","left.txt")

# path="C:\\Users\\claudio\\Desktop\\ten_folder_135\\"
# for t in os.listdir(path):

#download_readme("already_crawled.txt",path_projects="C:\\Users\\\claudio\\Desktop\\projects_new_dataset\\")

#test_topic("another_two.txt")

#write_csv("C:\\Users\\claudio\\Desktop\\SCC_dataset\\java")
#map_repos2topics("ordered_list.txt")
#get_issue()

#download_repos("msr_list.txt")
#get_langs("export.csv")