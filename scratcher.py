from bs4 import BeautifulSoup
import requests
from googlesearch import search

import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

import re
import numpy as np
import pandas as pd
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')

import tensorflow_hub as hub
module_url = 'https://tfhub.dev/google/universal-sentence-encoder/4'
model = hub.load(module_url)


def information(query):
    string = ''
    res = search(query, tld="co.in", num=10, stop=10, pause=2)
    for i in res:
        response = requests.get(url=i)
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.find(id="bodyContent")
        
        txt = soup.find_all('p')
        if 'britannica' in i:
            txt = soup.find_all('p',class_='topic-paragraph')
        if(txt):
            for i in range(len(txt)):
                try:
                    string += txt[i].get_text()+" "
                except:
                    break
    return string

def clean_text(text):
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "cannot ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub("\[[0-9][0-9]\]","",text)
    text = re.sub("\[[0-9]\]","",text)
    text = text.replace("\n","")
    text = re.sub(r"[^a-zA-Z0-9]+", ' ', text)
    return text

def get_wordnet_pos(tag):
    if tag.startswith('J'): return wordnet.ADJ
    elif tag.startswith('V'): return wordnet.VERB
    elif tag.startswith('N'): return wordnet.NOUN
    elif tag.startswith('R'): return wordnet.ADV
    else: return wordnet.NOUN

class LemmaTokenizer:
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self,txt):
        tokens = word_tokenize(txt)
        words_and_tags = nltk.pos_tag(tokens)
        return [self.wnl.lemmatize(word,pos = get_wordnet_pos(tag)) for word,tag in words_and_tags]

def main_keywords(text,ans):
    text = clean_text(text)
    tfidf = TfidfVectorizer(max_features = 5000 , stop_words = 'english' ,tokenizer=LemmaTokenizer())
    x = tfidf.fit_transform([text])
    x1 = x.toarray().flatten()
    ind = (-x1).argsort()
    
    ans = clean_text(ans)
    ans = tfidf.transform([ans])

    sim = cosine_similarity(ans,x)

    voc = pd.DataFrame()
    index = []
    value = []
    for txt,i in tfidf.vocabulary_.items():
        index.append(i)
        value.append(txt)
    voc['index']=index
    voc['value']=value
    voc = voc.set_index('index')
    
    return sim,voc.reindex(ind)

def key_similarity(key,ans):
    v1 = model([key])
    v2 = model([ans])
    return cosine_similarity(v1,v2)