from github import Github
import unicodedata
import base64
import codecs
import csv
import xml.etree.ElementTree as et


g3 = Github("claudioDsi","github17",per_page=100)
g = Github("7dd09093da17523189a8686362f276756aed5fd5", per_page=100)

def get_single_pom(groupdId, artifactId):
    out = open("repos_pom.txt", "a+", encoding="utf-8", errors="ignore")
    out2 = open("repos_pom2.txt", "a+", encoding="utf-8", errors="ignore")
    list_repo = g.search_repositories(query="language:java stars:>1000 " + groupdId + " " + artifactId)
    flag = False
    for repo_name in list_repo:

        content = g.get_repo(repo_name.full_name).get_contents(path="")
        groupid=False
        artifact=False
        for file in content:
            # print(file.name)
            if str(file.name) == "pom.xml":
                # out.write(str(file.decoded_content))
                s = file.decoded_content
                root = et.fromstring(s)
                print(s)
                for childe in root.findall("{http://maven.apache.org/POM/4.0.0}groupId"):
                    print(childe.text)
                    if childe.text == groupdId:
                        groupid = True
                for childe in root.findall("{http://maven.apache.org/POM/4.0.0}artifactId"):
                    print(childe.text)
                    if childe.text == artifactId:
                        artifact = True

        if artifact and groupid:
            out.write(str(repo_name.full_name))
            print("write file")
            break

        if artifactId and not groupdId:
            out2.write(str(repo_name.full_name))
            print("write file")
            break

def get_issue():
    out=open("repos_pom.txt", "a+", encoding="utf-8", errors="ignore")


    list_repo=g3.search_repositories(query="language:java ")
    flag=False
    for repo_name in list_repo:
        content = g3.get_repo(repo_name.full_name).get_contents(path="")
        for file in content:
            #print(file.name)
            if str(file.name) == "pom.xml":
                #out.write(str(file.decoded_content))
                s=file.decoded_content
                root=et.fromstring(s)


                for childe in root.findall("groupId"):
                    print(childe.text)


                    # if str(childe.tag) == "{http://maven.apache.org/POM/4.0.0}groupId":
                    #     for elem in childe:
                    #         print(elem.tag)
                    #         if elem.tag == "org.apache.commons":
                    #             out.write(repo_name.full_name+"\n")
                    #             print("write file")
                    #             flag=True
                    #         else:
                    #             print("no")
        if flag:
            break
            # stripped = lambda s: "".join(i for i in s if 31 < ord(i) < 127)
            # print(stripped(s))

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0] != "C")

def clean_file(pom_file):
    begin=codecs.open(pom_file, "r", encoding="base-64", errors="strict")
    out=open("parsed_pom.txt", "w", encoding="utf-8", errors="ignore")
    lines=begin.read()

    print(base64.b64decode(lines))




def parsing_csv():
    libname=""
    with open('C:\\Users\\claudio\\Desktop\\result_def2.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                #print(f'{row[1]} {row[2]}')
                libname=str(row[1])
                groupId=(str(row[2]).replace("/artifact/","").split("/")[0])
                artifactId=(str(row[2]).replace("/artifact/","").split("/")[1])

                print(artifactId)
                get_single_pom(groupId, artifactId)
                line_count += 1
        print(f'Processed {line_count} lines.')

#get_single_pom("org.reflections","reflections-maven")
parsing_csv()