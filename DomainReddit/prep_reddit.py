import json
import argparse
import re, os
import glob

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--subreddit', type = str, default = "restaurant", help="search for subreddit")
    parser.add_argument('--domain', type=str, default="restaurant", help="which domain")
    parser.add_argument('--save_file_name', type=str, default = "restaurant_01012015_31122019.json", help = "save_file_name")
    return parser.parse_args()

def make_dir(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        print("Directory {} created!".format(dir_name))
    else:    
        print("Directory {} already exists!".format(dir_name))
        
def remove_puncts(text):
    return re.sub(r"\.+", ".", text)

def replace_this_and_n_dashes(text):
    text = text.replace("[This]", "This").replace("[this]", "this").replace("\n", " ")
    return text

def remove_email(text):
    text = re.sub(r"\[…\]", " ", text)
    text = re.sub(r"\S*@\S*\s?", "", text)
    text = text.replace("--&gt;", " ").replace("\\---", " ").replace("&gt;", " ").replace("&amp;", " ")
    return re.sub(r"\_+", " ", text)

def remove_url(text):
    text = re.sub(r'\(?\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*\)?', "website", text)
    text = re.sub(r"\(?http\S+\)?", "website", text)
    text = re.sub(r"\(?\w+\.com\)?", "", text)
    text = re.sub(r"www\d{0,3}[.]", "website", text)
    text = re.sub(r'\[(.*?)\]', r'\1', text)
    return text.replace("website", " [URL]").replace("Website", " [URL]").replace("[ [URL]", " [URL]")

def preprocess_text(text):
    return re.sub("\s+", " ", remove_email(remove_puncts(remove_url(replace_this_and_n_dashes(text)))).strip())

def trim(text, max_length):
    """Trims text to be at most `max_length`, without splitting apart words."""
    if len(text) <= max_length:
        return text

    text = text[:max_length + 1]

    # Trim until the last two characters are the boundary between an
    # alphanumeric character, and a non-alphanumeric character.
    while len(text) > 1 and (text[-1].isalnum() == text[-2].isalnum()):
        text = text[:-1]

    return text[:-1]

def check_dial_len(dial, min_len=10, max_len=1024):
    if len(dial['context'])<min_len or len(dial['response'])<min_len or len(dial['response'])<min_len:
        return True
    elif len(dial['context'])>max_len or len(dial['response'])>max_len or len(dial['response'])>max_len:
        return True
    else:
        return False
    
def check_dial(dial):
    if len(dial['context'])<10 or len(dial['response'])<10 or len(dial['response'])<10:
        return True
    elif dial['response']==dial['false_response'] or dial['context']==dial['false_response'] or dial['context']==dial['response']:
        return True
    else:
        return False
    
def load_dial_json(filename):
    with open(filename, "r") as f:
        dial_json = json.load(f)
    return dial_json

def save_file(dict_to_save, filepath):
    with open(filepath, 'w') as file:
        json.dump(dict_to_save, file)

def load_all_dials(files):
    all_dials = []
    for f in files:
        dialogues = load_dial_json(f)
        print(len(dialogues))
        all_dials+=dialogues
    print("{} dials loading...".format(len(all_dials)))
    return all_dials
    

if __name__ == '__main__':
    args = parse_args()
    make_dir("./" + args.domain + "/all")
    domain = args.domain
    subreddit = args.subreddit
    file = "./" + domain + "/" + subreddit + "/" + "*01012015_31122019.json"
    files = glob.glob(file)
    all_dials = load_all_dials(files)
    all_com = []
    for i, dial in enumerate(all_dials):
        del dial['query']
        dial['context'] = preprocess_text(dial['context'])
        dial['response'] = preprocess_text(dial['response'])
        dial['false_response'] = preprocess_text(dial['false_response'])
        if not check_dial_len(dial, min_len=10, max_len=1024):
#             print(i)
#         else:
            dial['context'] = trim(dial['context'], 512)
            dial['response'] = trim(dial['response'], 512)
            dial['false_response'] = trim(dial['false_response'], 512)
        if not check_dial(dial):
#             print(i)
#         else:
            all_com.append(dial)
        if i%1000==0 and i!=0:
            print("Load {} dials".format(i))
    print("Number of dials after preprocessing: {}".format(len(all_com)))
    save_file(all_com, "./" + args.domain + "/all/" + args.save_file_name)