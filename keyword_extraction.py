import math,csv
from bs4 import BeautifulSoup
from urllib import request
from nltk.corpus import brown,reuters, words, stopwords
from nltk import *

def url_to_text(url):
    html = request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(html,'html.parser')
    filtered_soup = soup.find_all('p') #gets paras with <p> tag

    page_tokens = []
    for item in filtered_soup:
        para = item.get_text()
        para_tokens = word_tokenize(para)
        for token in para_tokens:
            page_tokens.append(token)
    
    return page_tokens            

def get_top_named_entities(tokens,n):
    d1 = defaultdict(list) # key = ending, value = list of entities with that ending
    d2 = defaultdict(int) # key = ending, value = combined frequency of entities with that ending
    
    endings_blacklist = {'Share','Pinterest','Twitter','Facebook','BBC','Messenger'} #modify if necessary}

    tagged_tokens = pos_tag(tokens)
    the_tree = ne_chunk(tagged_tokens,binary=True)

    for subtree in the_tree.subtrees():
        if subtree.label()=='NE' and type(subtree)==tree.Tree:
            entity_tokens = [node[0] for node in subtree.leaves()]
            entity = ' '.join(entity_tokens)
            
            ending = subtree[-1][0]
            if ending not in endings_blacklist:
                if entity not in d1[ending]:
                    d1[ending].append(entity)
                d2[ending]+=1

    entities = []
    endings = list(d2.keys())
    endings.sort(key = lambda x:d2[x],reverse=True) #sort by frequency
    for ending in endings:
        longest_phrase = max(d1[ending],key = lambda x:len(x)) #get longest entity for a given ending
        entities.append(longest_phrase)
    return entities[:n]


def read_idf():
    N = len(reuters.fileids())
    idf = defaultdict(lambda: math.log(N))
    with open('idf_reuters.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            idf[row[0]] = float(row[1])
    return idf

def calculate_tfidf(idf,tokens):
    tokens = [token.lower() for token in tokens]
    fd = FreqDist(tokens)
    tfidf = dict() 
    for token in tokens:
        tf = fd[token]/len(tokens)
        tfidf[token] = tf/idf[token]
    return tfidf

def get_top_tfidf_words(tfidf,n):
    words = []
    for word in sorted(tfidf, key = tfidf.get, reverse = True):
        tag = pos_tag([word])[0][1]
        if tag.startswith('NN'):
            words.append(word)
    return words[:n]

def main():
    #url = "https://www.bbc.com/news/health-53061281"
    url = "https://www.bbc.com/news/world-us-canada-53073526"
    #url = "https://www.bbc.com/news/world-asia-53073338"
    
    tokens = url_to_text(url)

    idf = read_idf()
    tfidf = calculate_tfidf(idf,tokens)
    tfidf_words = get_top_tfidf_words(tfidf,7)
    
    named_entities = get_top_named_entities(tokens,3)
    
    entity_endings = [word_tokenize(entity)[-1].lower() for entity in named_entities]
    tfidf_words = [word for word in tfidf_words if word.lower() not in entity_endings] # eliminate words in common if match by ending
    

    keywords = tfidf_words + named_entities
    print(keywords)

if __name__ == "__main__":
    main()

