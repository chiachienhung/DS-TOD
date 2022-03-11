import random
import numpy as np
from sklearn.model_selection import train_test_split
import argparse
import re

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--random_seed', type = int, default = 10, help="set random seed")
    parser.add_argument('--train_size', type=int, default = 200000, help="size for training set")
    parser.add_argument('--test_size', type=int, default = 10000, help="size for testing set")
    parser.add_argument('--input_domain_file', type=str, help="input domain file path") #"./domain/taxi_en.txt"
    parser.add_argument('--save_train_file_name', type=str, default = "./train/train.txt", help = "file name for training data")
    parser.add_argument('--save_test_file_name', type=str, default = "./test/test.txt", help = "file name for testing data")
    return parser.parse_args()

def remove_puncts(text):
    return re.sub(r"\.+", ".", text)

def remove_email(text):
    text = re.sub(r"\[…\]", " ", text)
    text = re.sub(r"\S*@\S*\s?", "", text)
    return re.sub(r"\_+", " ", text)
    
def remove_url(text):
    text = re.sub(r"\w+\.com", "website", text)
    return re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', "website", text)

def save_file(file_name, corpus_list):
    with open(file_name, 'a') as s:
        for i, element in enumerate(corpus_list):
            element = remove_email(remove_puncts(remove_url(element)))
            s.write("{}\n".format(element))
            if i%10000==0:
                print(i)
            

if __name__ == '__main__':
    args = parse_args()
    random.seed(args.random_seed)
    np.random.seed(args.random_seed)
    with open(args.input_domain_file, 'r') as f:
        data = f.read().split('\n')
        data = data[0:500000]
    print("Original data size: {}".format(len(data)))
    random.shuffle(data)
    train, test = train_test_split(data, test_size=0.02, random_state=args.random_seed)
    train = train[0:args.train_size]
    test = test[0:args.test_size]
    print("Training data size: {}".format(len(train)))
    print("Testing data size: {}".format(len(test)))
    #print(test[-1])
    save_file(args.save_test_file_name, test)
    save_file(args.save_train_file_name, train)
    
    #cd ./XLM
    #from https://github.com/facebookresearch/XLM/tree/cd281d32612d145c6742b4d3f048f80df8669c30
    #cat ../test/restaurant_10K.txt | ./tools/tokenize.sh en | python ./tools/lowercase_and_remove_accent.py > ../test/restaurant_10K_prep.txt
