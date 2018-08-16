#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import division
import pickle

with open("mpInfo.pkl", 'rb') as f:
    mpInfo = pickle.load(f)

for key in mpInfo:
    mp = mpInfo[key]
    totalSum = 0
    totalLength = 0
    for speech in mp['speeches']:
        text = speech.encode('utf-8')
        text = text.replace(".", "")
        text = text.replace(",", "")
        text = text.replace("?", "")
        text = text.replace("!", "")
        text = text.replace("\n", "")
        text = text.split(" ")
        text = list(filter(lambda a: a != "", text))
        lengths = [len(x.decode('utf-8')) for x in text]
        totalSum += sum(lengths)
        totalLength += len(lengths)
    mp['averageLength'] = totalSum/totalLength
    print(str(mp['name'].encode('utf-8')),  mp['averageLength'])
    
   


