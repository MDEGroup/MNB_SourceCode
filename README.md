# EASE 2020 Replication package


This repository contains the replication package and dataset of the paper to be published at EASE 2020 with the title **A Multinomial Naïve Bayesian (MNB) network to
automatically recommend topics for GitHub repositories**

All the resources, including the tool, the dataset, and the article have been realized by:

- Claudio Di Sipio 
- Riccardo Rubei
- Davide Di Ruscio
- Phuong T. Nguyen


We will provide the PDF version of the article in this repository



# Setting the environment 

To run the Python scripts, you need the following libraries:

- scikit-learn 0.22.1
- nltk 3.4.5
- guesslang 0.9.3
- tensorflow 1.6.0 (required by guesslang)
- PyGithub 1.44

Notice that guesslang module requires Python 3.6. More information about this module can be found [here](https://pypi.org/project/guesslang/)


# Code structure 

This folder contains the source code of the tool structured as follows:
```
MNB_code
    .
    |--- MNB.py         This file contains the MNB code to predict topics, including the topic aggregation phase
    |
    |--- crawler.py     It contains all teh utilities to mine Github repositories
    |
    |--- guessLang.py   This module performs the language prediction
    |
    |--- main.py        It is used to run the tools
    |
    |--- metrics.py     It contains all necessary scripts to compute the metrics         
```



# Crawler settings

To enable the crawler, you have to set a personal access token using the following function in **crawler.py**:
```
access_token = Github ("your token", per_page=100)
```

To generate an access token from your Github profile, please refer the following [link](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)

The optional parameter per_page is useful to paginate the results


# Running tool 

In **main.py**, you have to edit the following paths:

- train_dir = "path_to_train_folder"
- test_dir = "path_to_test_folder"


After the train data is loaded, you have to modify the following parameters in the predict_topics function: 

- dirs: the root folder that contains the test files
- test_dir: the test folder for a single round
- train_dir: the train folder for a single round
- labels: the list of topics to predict
- num_topics: number of predicted topics
- list_test: a txt file that contains the name of repository to test (available together with the datasets)

The output is a CSV files with all the metrics presented in the work:
- success rate (1..5)
- precision
- recall
- top rank



# Dataset and experiments

This [link](https://drive.google.com/drive/folders/197LCCfBTcpbqqaPfxO4C8V0t3f-XFnKT) contains all the datasets used in the evaluation as well as the results in CSV format. The table below shows the composition for each dataset:

| Dataset | # of testing file | # of training files |
|---------|-------------------|---------------------|
| D1      | 134               | 1,206               |
| D2      | 670               | 6,030               |
| D3      | 1,340             | 12,060              |


As discussed in the paper, we have build three different dataset by variating the number of files used in the training phase as shown in the table above. The structure is the following:

```
evaluation

test_files
    .
    |--- test_files_D1/            It contains the test projects of D1 for each evaluation round
    |
    |--- test_files_D2/            It contains the test projects of D2 for each evaluation round
    |
    |--- test_files_D3/            It contains the test projects of D3 for each evaluation round

results
    .
    |--- validation_10/            It contains the results computed for D1  
    |
    |--- validation_50/            It contains the results computed for D2 
    |
    |--- validation_100/           It contains the results computed for D3 


evaluation structure
    .
    |--- ten_folder_10.rar/        The ten-folder structure for D1
    |
    |--- ten_folder_50.rar/        The ten-folder structure for D2
    |
    |--- ten_folder_100.rar/       The ten-folder structure for D3
    
```




