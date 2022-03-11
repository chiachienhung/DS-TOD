import json
import argparse
import re, os
import random
import glob

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--domain', type=str, default="attraction", help="which domain")
    return parser.parse_args()

def load_dial_json(filename):
    with open(filename, "r") as f:
        dial_json = json.load(f)
    return dial_json

def save_dial_json(json_dial, filename):
    with open(filename, "w") as f:
        json.dump(json_dial, f, indent=2, separators=(",", ": "), sort_keys=False)

def context_response(data):
    context = []
    response = []
    for dial in data:
        context.append(dial['context'])
        response.append(dial['response'])
        response.append(dial['false_response'])
    return context, response
    
def get_data(data):
    context, response = context_response(data)
    all_data = []
    for dial in data:
        sing_dial = {}
        sing_dial['context']=clean_text(dial['context'])
        sing_dial['response']=clean_text(dial['response'])
        sing_dial['false_response']=[clean_text(dial['false_response'])]
        #sing_dial['label']=[1,0,0,0]
        negative_sampling = 3
        #print(negative_sampling)
        while(len(sing_dial['false_response'])<negative_sampling):
            f_resp = random.choice(response+context)
            if f_resp!=dial['response'] and f_resp!=dial['false_response'] and f_resp!=dial['context']:
                sing_dial['false_response'].append(clean_text(f_resp))
        all_data.append(sing_dial)
    return all_data

def clean_text(text):
    if '/u/' in text:
        return re.sub(r"\b[/u/]\w+", "", text).replace('/u', '').strip()
    else:
        return text


if __name__ == '__main__':
    args = parse_args()
    all_files = glob.glob("./" + args.domain + "/all/*")
    dialogues = []
    for i, file in enumerate(all_files):
        dialog = load_dial_json(file)
        if len(dialog)>1:
            print(len(dialog), file)
            new_data = get_data(dialog)
            dialogues += new_data
            print(len(dialog), len(dialogues))
            #save_dial_json(new_data, "./" + args.domain + '/all_concat_new_' + str(i) + '.json')
        save_dial_json(dialogues, "./" + args.domain + '/all_concat_new_trial.json')