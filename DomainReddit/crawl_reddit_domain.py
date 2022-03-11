import difflib
import re
import requests
import json
import argparse
import os
import time
import datetime
import random

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_query', type = str, default="", help="input query to search")
    parser.add_argument('--after', type = str, default = "01/11/2020", help = "crawl data after the date")
    parser.add_argument('--before', type = str, default = "31/12/2020", help = "crawl data before the date")
    parser.add_argument('--subreddit', type = str, default = "", help="search for subreddit")
    parser.add_argument('--limit', type=int, default = 30, help="limit size for comments")
    parser.add_argument('--domain', type=str, default="", help="which domain")
    parser.add_argument('--save_file_name', type=str, default = "domain.json", help = "save_file_name")
    return parser.parse_args()

def compare_two_sent(a, b):
    if "&gt;" in b:
        d = difflib.Differ()
        diff = d.compare(a.split(), b.split())
        s = [k for k in diff if "  " in k]
        fix = b.replace("&gt;", "").replace(" ".join(" ".join(s).split()), " ").strip()
        #print("original", b)
        #print("fix", fix)
    else:
        fix = b
    return fix

def check_unk_response(comments, a, orig_context):
    false_resp = comments[random.choice(a)]['body']
    while false_resp in ["[removed]","[deleted]"] or false_resp==orig_context:
        print("False resp:", false_resp)
        false_resp = comments[random.choice(a)]['body']
        it+=1
        if it>=10:
            false_resp = "This is a nice weather, let's go hiking!"
            break
    return false_resp

def make_dir(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        print("Directory {} created!".format(dir_name))
    else:    
        print("Directory {} already exists!".format(dir_name))

def save_file(dict_to_save, filepath):
    with open(filepath, 'w') as file:
        json.dump(dict_to_save, file)

def get_pushshift_data(data_type, **kwargs):
    """
    Gets data from the pushshift api.
 
    data_type can be 'comment' or 'submission'
    The rest of the args are interpreted as payload.
 
    Read more: https://github.com/pushshift/api
    """
 
    base_url = f"https://api.pushshift.io/reddit/search/{data_type}/"
    payload = kwargs
    request = requests.get(base_url, params=payload)
    return request.json()


def convert_date_to_timestamp(date):
    """
    date: str, e.g. 01/12/2020 (01 Dec 2020)
    """
    return str(int(time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y").timetuple())))

def collect_com_infos(comments, data, i, query="bus", subreddit="travel"):
    all_com = []
    for j, _ in enumerate(comments):
        infos = {}
        if comments[j]['body'] not in ["[removed]","[deleted]"] and data[i]['body'] not in ["[removed]","[deleted]"]: 
            if comments[j]['id'] in data[i]['parent_id']: 
                infos = {}
                print(i, j, 'Parent')
                a = list(range(0,len(comments)))
                a.remove(j)
                infos['query'] = query
                infos['subreddit'] = comments[j]['subreddit']
                infos['link_id'] = comments[j]['link_id']
                infos['context_id'] = comments[j]['id']
                infos['response_id'] = data[i]['id']
                infos['context'] = comments[j]['body']
                infos['response'] = compare_two_sent(comments[j]['body'], data[i]['body'])
                infos['false_response'] = check_unk_response(comments, a, comments[j]['body']) #comments[random.choice(a)]['body']
                infos['created_utc_response'] = data[i]['created_utc']
                all_com.append(infos)
                ##https://www.reddit.com/r/{subreddit}/comments/{link_id.split('_')[1]}/xxxxx/{context_id}

            elif data[i]['id'] in comments[j]['parent_id']:
                infos = {}
                print(i, j, "Child")
                a = list(range(0,len(comments)))
                a.remove(j)
                ##https://www.reddit.com/r/{subreddit}/comments/{link_id.split('_')[1]}/xxxxx/{context_id}
                infos['query'] = query
                infos['subreddit'] = comments[j]['subreddit']
                infos['link_id'] = comments[j]['link_id']
                infos['context_id'] = data[i]['id']
                infos['response_id'] = comments[j]['id']
                infos['context'] = data[i]['body']
                infos['response'] = compare_two_sent(data[i]['body'], comments[j]['body'])
                infos['false_response'] = check_unk_response(comments, a, infos['context']) #comments[random.choice(a)]['body']
                infos['created_utc_response'] = comments[j]['created_utc']
                all_com.append(infos)
    return all_com


if __name__ == '__main__':
    args = parse_args()
    make_dir(args.domain)
    make_dir(args.domain+'/'+args.subreddit)
    before = convert_date_to_timestamp(args.before)
    after = convert_date_to_timestamp(args.after)
    print(args.input_query, args.domain)
    print(args.before, args.after)
    lasttimestamp = after
    all_collection = []
    iteration = 0
    while(int(lasttimestamp)>=int(after)):
        try:
            data = get_pushshift_data(data_type="comment",
                                      q=args.input_query,
                                      size=1000,
                                      before = before,
                                      after = after,
                                      sort = "desc",
                                      subreddit=args.subreddit).get("data")
            json_error = 0
        except ValueError:
            json_error = 1
            print('wrong')
            data = []
        if len(data)!=0 and json_error==0:
            k=0
            for i, d in enumerate(data):
                if k==1:
                    i=i-1
                if data[i]['parent_id']!=data[i]['link_id']:
                    try:
                        comments = get_pushshift_data(data_type="comment",
                                          link_id=data[i]['link_id'],
                                          subreddit=args.subreddit,
                                          size=1000).get("data")
                        all_com = collect_com_infos(comments, data, i, query=args.input_query, subreddit=args.subreddit)
                        #print(len(all_com))
                        all_collection += all_com
                        k=0
                    except:
                        k=1
            lasttimestamp = data[-1]['created_utc']
            before = lasttimestamp
            print("Iter: {}, NumOfDials: {}".format(iteration+1, len(all_collection)))
            iteration+=1
            print("No error:{} {}".format(before, after))
        elif json_error==1:
            print("Has error:{} {}".format(before, after))
            print("Do it again")
        else:
            break

    final_file_name = './'+args.domain+'/'+args.subreddit+'/'+args.save_file_name 
    save_file(all_collection, final_file_name)