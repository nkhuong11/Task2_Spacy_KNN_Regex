import sys
import datetime

import spacy
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import English

import pandas as pd
import numpy as np 
import re

from stop_words import STOP_WORDS

nlp = spacy.load('en')
tokenizer = English().Defaults.create_tokenizer(nlp)

data = pd.read_csv('Data.csv', encoding='latin1')
data = data['Text'][0:10]


s = datetime.datetime.now()
# remove stop words USING REGEX
# remove_list = re.compile('[^a-zA-z0-9@ :\.\/]')
# remove_list2 = re.compile('(\n|\.$|(\.?=\s+)|(:(?!\/\/)))')
# remove_list3 = re.compile('(\s)(the|this|that|there|to|is|are|am|on|in|out|do|a|an|be|just|from|with|so|as|just|for|by|Ã¢Â€Â|)(?!\w)' )
# #txt = ' '.join(re.sub("[0-9]+","NUM",txt).split()

# def remove_stop_word(data):
#     l = len(data)
#     for index in range(0,l):
#         data.loc[index] = re.sub(remove_list, '', (data.loc[index]).lower())
#         data.loc[index] = re.sub(remove_list2, '', (data.loc[index]))
#         data.loc[index] = re.sub(remove_list3, '', (data.loc[index]))

#     return data


def remove_stop_word(data):
    l = len(data)
    #remove_list = re.compile('[^a-zA-z0-9@ :\.\/]')
    remove_list = re.compile('(:(?!\/\/))|(\.$)|(\.(?=\s+))|(\.(\.+))|([^a-zA-Z0-9@ :\'\.\/+=?-_])|(\'s|\'S)|(\s[+])|(\'RE|\'Re|\'re)') #remove icons and adundant characters
    for index in range(0,l):
        data.loc[index] = re.sub(remove_list, '', data.loc[index])
        data.loc[index] = ' '.join([word for word in data.loc[index].split() if word.lower() not in STOP_WORDS])
    return data
    
data = remove_stop_word(data)


# Tokenizer QUICK-WAY
'''
create dataframe to store all tweets' tokens (quick-way)
'''
l = len(data)
doc = pd.Series(data=(nlp(data.loc[index]) for index in range(0,l)))


class Token(object):
    def __init__(self, length=1):
        self.values = pd.Series(data=([] for index in range(0,length)))
        self.types = pd.Series(data=([] for index in range(0,length)))
        self.tokens = pd.Series(data=([] for index in range(0,length)))



#Lemmatization
def Lemma(data):
    '''
    data: Series that store all the tokens.
    This function return an object and also remove some adundant words leave in the token series
    '''
    length = len(data)
    token = Token(length)
    name_tag = re.compile('(@([a-zA-Z0-9_-]+))(?=(\s+|$))')
    for index in range(0, length):
        length2 = len(data.loc[index])
        for index2 in range(0, length2):
            t = data.loc[index][index2]       
            if(re.match(name_tag, t.text)):                   
                token.values.loc[index].append(t.text)
                token.types.loc[index].append('TAGNAME')
                token.tokens.loc[index].append(t)
            elif(t.pos_ == 'NOUN'):                 
                token.values.loc[index].append(t.lemma_)
                token.types.loc[index].append('NOUN')
                token.tokens.loc[index].append(t)
            elif(t.pos_ == 'VERB'):                 
                token.values.loc[index].append(t.lemma_)
                token.types.loc[index].append('VERB')
                token.tokens.loc[index].append(t)
            elif(t.pos_ == 'ADJ'):                 
                token.values.loc[index].append(t.lemma_)
                token.types.loc[index].append('ADJ')
                token.tokens.loc[index].append(t)
            elif(t.pos_ == 'PRON'):                 
                token.values.loc[index].append(t.lower_)
                token.types.loc[index].append('PRON')
                token.tokens.loc[index].append(t)
            elif(t.pos_ == 'ADV'):                 
                token.values.loc[index].append(t.lemma_)
                token.types.loc[index].append('ADV')
                token.tokens.loc[index].append(t)
            elif(t.pos_ == 'PROPN' or t.pos_ == 'GPE' or t.pos_ == 'ORG'):  
                token.values.loc[index].append(t.text)
                token.types.loc[index].append('NAME-ENT')
                token.tokens.loc[index].append(t)
            elif(t.like_url == True):                        
                token.values.loc[index].append(t.text)
                token.types.loc[index].append('URL')
                token.tokens.loc[index].append(t)
            elif(t.like_email == True):                      
                token.values.loc[index].append(t.text)
                token.types.loc[index].append('EMAIL')
                token.tokens.loc[index].append(t)
            elif(t.like_num == True):                     
                token.values.loc[index].append(t.text)
                token.types.loc[index].append('NUM')
                token.tokens.loc[index].append(t)  
            elif(t.pos_ == 'PUNCT'):
                continue
            elif(t.pos_ == 'INTJ'):                 
                token.values.loc[index].append(t.lemma_)
                token.types.loc[index].append('INTJ')
                token.tokens.loc[index].append(t)
            else:
                token.values.loc[index].append(t.lemma_)
                token.types.loc[index].append('X')
                token.tokens.loc[index].append(t)
    return token


# def Lemma(data):
#     length = len(data)
#     tokenObject = Token(length)
#     name_tag = re.compile('(@([a-zA-Z0-9_-]+))(?=(\s+|$))')

#     for index in range(0, length):
#         token = nlp(data.loc[index])
#         length2 = len(token)
#         for index2 in range(0, length2):
#             t = token[index2]   
            # if(re.match(name_tag, t.text)):                   
            #     token.values.loc[index].append(t.text)
            #     token.types.loc[index].append('TAGNAME')
            #     token.tokens.loc[index].append(t)
            # elif(t.pos_ == 'NOUN'):                 
            #     token.values.loc[index].append(t.lemma_)
            #     token.types.loc[index].append('NOUN')
            #     token.tokens.loc[index].append(t)
            # elif(t.pos_ == 'VERB'):                 
            #     token.values.loc[index].append(t.lemma_)
            #     token.types.loc[index].append('VERB')
            #     token.tokens.loc[index].append(t)
            # elif(t.pos_ == 'ADJ'):                 
            #     token.values.loc[index].append(t.lemma_)
            #     token.types.loc[index].append('ADJ')
            #     token.tokens.loc[index].append(t)
            # elif(t.pos_ == 'PRON'):                 
            #     token.values.loc[index].append(t.lower_)
            #     token.types.loc[index].append('PRON')
            #     token.tokens.loc[index].append(t)
            # elif(t.pos_ == 'ADV'):                 
            #     token.values.loc[index].append(t.lemma_)
            #     token.types.loc[index].append('ADV')
            #     token.tokens.loc[index].append(t)
            # elif(t.pos_ == 'PROPN' or t.pos_ == 'GPE' or t.pos_ == 'ORG'):  
            #     token.values.loc[index].append(t.text)
            #     token.types.loc[index].append('NAME-ENT')
            #     token.tokens.loc[index].append(t)
            # elif(t.like_url == True):                        
            #     token.values.loc[index].append(t.text)
            #     token.types.loc[index].append('URL')
            #     token.tokens.loc[index].append(t)
            # elif(t.like_email == True):                      
            #     token.values.loc[index].append(t.text)
            #     token.types.loc[index].append('EMAIL')
            #     token.tokens.loc[index].append(t)
            # elif(t.like_num == True):                     
            #     token.values.loc[index].append(t.text)
            #     token.types.loc[index].append('NUM')
            #     token.tokens.loc[index].append(t)  
            # elif(t.pos_ == 'PUNCT'):
            #     continue
            # elif(t.pos_ == 'INTJ'):                 
            #     token.values.loc[index].append(t.lemma_)
            #     token.types.loc[index].append('INTJ')
            #     token.tokens.loc[index].append(t)
            # else:
            #     token.values.loc[index].append(t.lemma_)
            #     token.types.loc[index].append('X')
            #     token.tokens.loc[index].append(t)
#     return tokenObject


x = Lemma(doc)

e = datetime.datetime.now()
print('Time: ', int((e - s).total_seconds() *1000))    



x.values.to_csv('Values.csv')
x.types.to_csv('Types.csv')
x.tokens.to_csv('Token.csv')


#Task 2
#Spacy