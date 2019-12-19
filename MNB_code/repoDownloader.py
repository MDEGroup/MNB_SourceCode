from github import Github
from pygit2 import clone_repository

g = Github("2383e14c703b3857fda27d635d568537f926a881", per_page=100)

def download_repos(repo_name,base_dir):
    if str(repo_name).strip().find("/") != -1:
        try:
            url = "https://github.com/"+str(repo_name).strip()+".git"
            out_path=base_dir+"/"+str(repo_name).strip().replace("/", "-")
            print(url)
            clone_repository(url,out_path)
            return out_path
        except:
            print("not found")
    else:
        topic=str(repo_name).strip()