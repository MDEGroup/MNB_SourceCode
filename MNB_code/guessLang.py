from guesslang import Guess
import os
from collections import Counter
import time
from github_crawling.repoDownloader import download_repos
import shutil

samples = 1000
size = 10000
main_dir = "C:\\Users\\claudio\\Desktop\\models\\"
ad = open("langs_results.txt", "r")
already_downloaded = ad.readlines()
ad.close()

def main():

    start_time = time.time()
    langs = []
    count = 0

    list_repo = open("global_list.txt", "r", encoding="utf-8", errors="ignore")

    for repo in list_repo:

        results = open("langs_results.txt", "a")

        if(repo not in already_downloaded):

            repo_path = download_repos(repo, main_dir)
            langs = []
            if(repo_path!=None):

                for dirname, dirnames, filenames in os.walk(repo_path):

                    # print path to all filenames.
                    for filename in filenames:
                        path = ((os.path.join(dirname, filename)))
                        if("/.git" not in path):
                            try:
                                file_size = os.path.getsize(path)
                                if(file_size<=size):
                                    if(filename.lower()=="readme"):
                                        continue
                                    try:
                                        t0 = time.time()
                                        file = open(path, "r", encoding="utf8", errors='ignore')
                                        print(file)
                                        data = file.read()

                                        if(time.time()-t0>1):
                                            continue

                                        else:
                                            lang = Guess().language_name(data)
                                            if(lang!="Markdown"):
                                                #print(filename)
                                                #print(lang)
                                                langs.append(lang)
                                                count += 1

                                    except Exception as e:
                                        True
                                        print(e)
                                        #result.write(pathlib.Path(path).suffix)
                                        #result.write("\n")
                                        #print("Error Opening: "+pathlib.Path(path).suffix)
                            except Exception as e:
                                   print(e)
                    if (count >= samples):
                        count = 0
                        break
                c = Counter(langs)
                results.write(repo+","+str(c) + "\n")
                results.close()
                shutil.rmtree(repo_path)
            else:
                results.write(repo)
        else:
            print("Already downloaded")


    final_time = time.time() - start_time
    print("Execution time: " + str(final_time))
main()