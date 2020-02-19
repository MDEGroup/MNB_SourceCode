from github_crawling.MNB import load_data, predict_topics

import os

train_dir = "D:\\backup_datasets\\EASE2020\\ten_folder_10\\train1\\"
test_dir = "D:\\backup_datasets\\EASE2020\\ten_folder_10\\test1\\"

dirs = os.listdir(test_dir)
train_data, train_labels = load_data(train_dir)
predict_topics(dirs, test_dir, train_data, train_labels, 20, "half_1.txt")



