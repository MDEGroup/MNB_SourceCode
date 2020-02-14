# MNB_Topic Recommendation


This repository contains the source code related to the work done for EASE 2020 Conference

# Setting the environment 

To run the Python scripts, you need the following requirements:

- scikit-learn 0.22.1
- nltk 3.4.5
- guesslang 0.9.3
- PyGithub 1.44

Notice that guesslang module requires Python 3.6

# Crawler settings

To enable the crawler, you have to set a personal access token in this way:

access_token = Github ("your token", per_page=100)

To generate an access token from your Github profile, please refer the following [link](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)

The optional parameter per_page is useful to paginate the results

# Run the tool 

In main.py, you have to edit the following paths:

train_dir = "path_to_train_folder"
test_dir = "path_to_test_folder"


Then run:

main.py



# Dataset and experiments


The following link contains the dataset used in the evaluation as well as the results in CSV format:

https://drive.google.com/drive/folders/197LCCfBTcpbqqaPfxO4C8V0t3f-XFnKT


