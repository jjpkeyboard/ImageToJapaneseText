import pandas as pd
import re
import string
from fugashi import Tagger
import os
from jamdict import Jamdict
from PIL import Image

wakati = Tagger("-Owakati")
jam = Jamdict(db_file='C:/Users/jaxon/AppData/Roaming/Python/Python313/site-packages/jamdict/data/jamdict.db')

def is_japanese_syllabary(s):
    return bool(re.fullmatch(r'[\u3040-\u309F\u30A0-\u30FF]+', s))

def contains_latin(text):
    return bool(re.search(r'[A-Za-z]', text))

def is_punctuation(s):
    s = s.strip()
    return all(char in string.punctuation + '…' + '“' + '”' for char in s) and len(s) > 0

def contains_japanese_punctuation(s):
    pattern = r'[\u3000-\u303F\uFF01-\uFF0F\uFF1A-\uFF20\uFF3B-\uFF40\uFF5B-\uFF65]'
    return bool(re.search(pattern, s))


docList = []

ep_num = 934
ep_str = str(ep_num) + '話'
sub_folder = 'onepiece(892-999)'
if os.path.isdir(sub_folder):
    for filename in os.listdir(sub_folder):
        if (re.findall(ep_str, filename)):
            sub_file = 'onepiece(892-999)\\' + filename
else: 
    print("no folder")
    
hundred_days_file = '[Japanese] 【100DAYS】で見る「これがマインクラフト」 [DownSub.com].txt'
terrace_house_file = 'ipv6-c060-sea003-ix.1.oca.nflxvideo.net - Copy.txt'


with open(sub_file, 'r', encoding = 'utf-8') as file:
    for line in file:
        token = wakati.parse(line).split()

        for element in token:
            if ((not element.isdigit() and not contains_latin(element) and not is_punctuation(element) and not contains_japanese_punctuation(element)) and not ((len(element) < 2) and is_japanese_syllabary(element))):
                docList.append(element)




doc = pd.DataFrame(data = docList)
doc = doc.value_counts()


pd.set_option('display.max_rows', 501)
frequency_count_df = doc[doc > 3][:500].sort_values(ascending = True)
# for word_index in range(len(frequency_count_df)):
#     definition = jam.lookup(frequency_count_df.index[word_index][0])
#     print(definition)
print(frequency_count_df)
print(jam.lookup(frequency_count_df.index[-2][0]))