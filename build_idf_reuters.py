from bs4 import BeautifulSoup
from urllib import request
from nltk import *
from nltk.corpus import stopwords, words, reuters
import math, csv

# BUILDS CSV FILE WITH IDF VALUES FOR EVERY WORD IN REUTERS CORPUS

files = dict() # key = filename,value = set of words in that file
for file_id in reuters.fileids():
    files[file_id]=set(reuters.words(file_id))

idf = dict()
N = len(reuters.fileids())
reuters_words = set(reuters.words())
for word in reuters_words:
    count = 0 # no need to avoid division by 0
    for file_id in reuters.fileids():
        if word in files[file_id]:
            count+=1
    idf[word] = math.log(N/count)

with open('idf_reuters.csv', 'w') as file:
    writer = csv.writer(file)
    for (word,idf_val) in idf.items():
        writer.writerow([word,idf_val])