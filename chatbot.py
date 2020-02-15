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









