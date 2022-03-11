# Data download from: http://data.statmt.org/cc-100/ (i.e., en.txt.xz)
import os
import lzma
import re

terms_b = ["\\bgallery", "college", "entrance", "entrance free",
             "swimming pool", "pounds", "jello gallery", "attraction", "sports", 
             "post code", "postcode", "attraction center", "attraction centre",
             "theatre", "theater", "church", "center area", "centre area", "downing college",
             "park", "trinity college",
             "town centre", "town center\\b"]

terms_l = ["museum", "college", "entertainment", "nightclub", "cinema", "theater", "theatre",
           "architecture", "attraction"]

pattern = '\\b|\\b'.join(terms_b) + "|"  + "|".join(terms_l)

def is_match(regex, text):
    pattern = re.compile(regex)
    return pattern.search(text, re.IGNORECASE) is not None
def match_num(regex, text):
    pattern = re.compile(regex, re.IGNORECASE)
    return pattern.findall(text)
    #return len(pattern.findall(text))

def store_line(filename):
    if os.path.exists(filename):
        mode = 'a'
    else:
        mode = 'w'
    return mode

if not os.path.exists("./domain"):
    os.makedirs("./domain")
    
count = 0
extract_list = []
num = []
with lzma.open('en.txt.xz', mode='rt') as file:
    for i, line in enumerate(file):
        check = match_num(pattern, line)
        if len(check)>=2 or "attraction" in check:
            extract_list.append(line)
            num.append(len(check))
        if len(extract_list)>1000:
            mode = store_line("./domain/attraction_en.txt")
            with open("./domain/attraction_en.txt", mode) as s:
                for element in extract_list:
                    s.write(element)
            count +=1000
            extract_list = []
        if i%100000==0 and i!=0:
            print("Load {}".format(i))
        if len(num)>500000:
            print(i)
            break
mode = store_line("./domain/attraction_en.txt")
if len(extract_list)!=0:
    with open("./domain/attraction_en.txt", mode) as s:
        for element in extract_list:
            s.write(element)
with open("./domain/attraction_count.txt", mode) as s:
    for element in num:
        s.write(str(element)+"\n")
