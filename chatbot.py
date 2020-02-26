# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

## import libraries
import numpy as np
import tensorflow as tf
import re
import time
import pandas as pd

## import dataset
lines = open(r'E:\ChatBot\movie_lines.txt', errors='ignore', encoding='utf-8').read().split('\n')
conversations = open(r'E:\ChatBot\movie_conversations.txt', errors='ignore', encoding='utf-8').read().split('\n')

## from lines get only line id and the dialoge
## sample text from lines
##      L1045 +++$+++ u0 +++$+++ m0 +++$+++ BIANCA +++$+++ They do not!
##      L1044 +++$+++ u2 +++$+++ m0 +++$+++ CAMERON +++$+++ They do to!
## creating a dict to map the dialoge

id2line = {}
for line in lines:
    _line = line.split('+++$+++')
    if len(_line) == 5:
        id2line[_line[0].strip()] = _line[4]
    

## from conversations get all the conversation lists
## sample from conversation
## u0 +++$+++ u2 +++$+++ m0 +++$+++ ['L194', 'L195', 'L196', 'L197']
## u0 +++$+++ u2 +++$+++ m0 +++$+++ ['L198', 'L199']
conv_id = []
for conversation in conversations:
    _con_list = conversation.split('+++$+++')
    conv_id.append(_con_list[-1].strip())

## convert string to list
conv_id_list = []
for ids in conv_id:
    clean_text = ids.replace("'",'').replace("[","").replace("]","").replace(" ","")
    conv_id_list.append(clean_text.split(','))

## Getting the answers and queston separately
## Map the ID's with conversations

questions=[]
answers=[]

for conversations in conv_id_list:
    for i in range(len(conversations)-1):
        questions.append(id2line[conversations[i]])
        answers.append(id2line[conversations[i+1]])


## Cleaning text - changing the short forms

def clean_text(text):
    text = text.lower().strip()
    text = re.sub(r"we'd", "we would",text)
    text = re.sub(r"that's", "that is",text)
    text = re.sub(r"bout", "about",text)
    text = re.sub(r"i'm", "i am",text)
    text = re.sub(r"you're", "you are",text)
    text = re.sub(r"don't", "do not",text)
    text = re.sub(r"there's", "there is",text)
    text = re.sub(r"can't", "can not",text)
    text = re.sub(r"workin'", "working",text)
    text = re.sub(r"in'", "ing",text)
    text = re.sub(r"\re", " are",text)
    text = re.sub(r"\'s", " is",text)
    text = re.sub(r"\'ll", " will",text)
    text = re.sub(r"\'ve", " have",text)
    text = re.sub(r"can't", "can not",text)
    text = re.sub(r"won't", "will not",text)
    text = re.sub(r"didn't", "did not",text)
    text = re.sub(r"[-()\"#/@*%&';:<>{}`+=~|.!?,_]", "",text)
    return text
    
clean_questions = []
for question in questions:
    clean_questions.append(clean_text(question))

clean_answers = []
for answer in answers:
    clean_answers.append(clean_text(answer))

## Create a dict to contain the word count
wordcount = {}
for line in clean_questions:
    for word in line.split():
        if word not in wordcount:
            wordcount[word] = 1
        wordcount[word] += 1
    
for line in clean_answers:
    for word in line.split():
        if word not in wordcount:
            wordcount[word] = 1
        wordcount[word] += 1

##
## tokenize using dictionary
threshold = 20

questionword2int = {}
word_number = 0
for word,count in wordcount.items():
    if count > threshold:
        questionword2int[word] = word_number
        word_number += 1
        
answerword2int = {}
word_number = 0
for word,count in wordcount.items():
    if count > threshold:
        answerword2int[word] = word_number
        word_number += 1
        

## Adding last tokens
tokens = ['<PAD>','<EOS>','<OUT>','<SOS>']
for token in tokens:
    questionword2int[token] = len(questionword2int) + 1
    
for token in tokens:
    answerword2int[token] = len(answerword2int) + 1

## Create the inverse of the answerword2int
##answerword2int = {w_i: w for w, w_i in answerword2int.items()}

#Adding End of String token to the end of every answer
for i in range(len(clean_answers)):
    clean_answers[i] += ' <EOS>'
    
## translate all the words to unique associated numbers
question_into_int =[]
for questions in clean_questions:
    intlist = []
    for word in questions.split():
        if word not in questionword2int:
            intlist.append(questionword2int['<OUT>'])
        else:
            intlist.append(questionword2int[word])
    question_into_int.append(intlist)

## translate all the words to unique associated numbers
answer_into_int =[]
for answers in clean_answers:
    intlist = []
    for word in answers.split():
        if word not in answerword2int:
            intlist.append(answerword2int['<OUT>'])
        else:
            intlist.append(answerword2int[word])
    answer_into_int.append(intlist)
    
## Clean
sorted_clean_questions=[]
sorted_clean_answers=[]

for length in range(1, 26):
    for i in enumerate(question_into_int):
        if len(i[1]) == length:
            sorted_clean_questions.append(question_into_int[i[0]])
            sorted_clean_answers.append(answer_into_int[i[0]])

## setting up the hyper parameters for Seq2Seq model

















