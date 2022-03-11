import json
import argparse
import re, os
import random
import glob
import numpy as np

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
        
def get_data(data):
    context = []
    response = []
    label = []
    for dial in data:
        context.append(dial['context'])
        response.append(dial['response'])
        label.append(1)
        context.append(dial['context'])
        response.append(dial['false_response'])
        label.append(0)
    for dial in data:
        negative_sampling = random.randint(1,3)
        #print(negative_sampling)
        i=0
        while(i<negative_sampling):
            f_resp = random.choice(response+context)
            if f_resp!=dial['response'] and f_resp!=dial['false_response'] and f_resp!=dial['context']:
                context.append(dial['context'])
                response.append(f_resp)
                label.append(0)
            i+=1
    return context, response, label

def convert_to_json(context, response, label):
    dialogues = []
    for c, r, l in zip(context, response, label):
        dials = {}
        dials['context'] = c
        dials['response'] = r
        dials['label'] = l
        dialogues.append(dials)
    return dialogues

# restaurant-attraction v
# hotel-attraction v
# restaurant-hotel v
# restaurant-train v
# restaurant-attraction-taxi v
# hotel-attraction-taxi v
# hotel-restaurant-taxi v
# attraction-train v
# hotel-train v
if __name__ == '__main__':
    args = parse_args()
    all_files = glob.glob("./" + args.domain + "/all/*")
    dialogues = []
    for file in all_files:
        dialog = load_dial_json(file)
        print(len(dialog), file)
        context, response, label = get_data(dialog)
        dialogues += convert_to_json(context, response, label)
        print(len(context), len(dialogues))
    save_dial_json(dialogues, "./" + args.domain + '/all_concat_trial.json')
    
#     args = parse_args()
#     dialogues_a = load_dial_json('./hotel/all_concat.json')
#     dialogues_b = load_dial_json('./attraction/all_concat.json')
#     dialogues_c = load_dial_json('./taxi/all_concat.json')
#     print(len(dialogues_a), len(dialogues_b))
#     print(len(dialogues_c))
    
#     random.seed(10)
#     random_permutation = list(range(len(dialogues_a)))
#     random.shuffle(random_permutation)
#     random_permutation = random_permutation[0:225000]
#     print(len(random_permutation))
#     print(random_permutation[0:200])
#     dialogues_a = list(np.array(dialogues_a)[random_permutation])
    
#     random.seed(10)
#     random_permutation = list(range(len(dialogues_b)))
#     random.shuffle(random_permutation)
#     random_permutation = random_permutation[0:225000]
#     print(len(random_permutation))
#     print(random_permutation[0:200])
#     dialogues_b = list(np.array(dialogues_b)[random_permutation])
    
#     random.seed(10)
#     random_permutation = list(range(len(dialogues_c)))
#     random.shuffle(random_permutation)
#     random_permutation = random_permutation[0:225000]
#     print(len(random_permutation))
#     print(random_permutation[0:200])
#     dialogues_c = list(np.array(dialogues_c)[random_permutation])
    
#     print(len(dialogues_a), len(dialogues_b))
#     print(len(dialogues_c))
#     dialogues = dialogues_a + dialogues_b
#     dialogues += dialogues_c
#     random.seed(10)
#     random.shuffle(dialogues)
#     print(len(dialogues))    
#     save_dial_json(dialogues, "./" + 'hotel-attraction-taxi' + '/all_concat.json')