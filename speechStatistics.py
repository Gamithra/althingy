#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import division
import pickle
import statistics
import copy

# TODO: get utf-8 decoding right
#       output data in human readable form
#       calculate things like occurrences of "ég", "við", ..
#       fetch data for speech lengths and divide by words/characters said
#       get numbers our as well
#       sort people based on parties

averageResults = []
modeResults = []
medianResults = []
meResults = []

junkCharacters = [".", ",", "?", "!", "\n", "-"]
with open("mpInfo.pkl", 'rb') as f:
        mpInfo = pickle.load(f)


def cleanText(speech):
    text = speech.encode('utf-8')
    for character in junkCharacters:
        text = text.replace(character, " ")
    text = text.split(" ")
    text = list(filter(lambda a: a != "", text))
    return text



if __name__ == "__main__":
    for key in mpInfo:
        mp = mpInfo[key]
        totalSum = 0
        totalLength = 0
        totalMe = 0
        for speech in mp['speeches']:
            lengths = [len(x.decode('utf-8')) for x in cleanText(speech)]
            totalSum += sum(lengths)
            totalLength += len(lengths)

            upperText = [x.decode('utf-8').upper() for x in cleanText(speech)]
            meCount = upperText.count("ég".decode('utf-8').upper())
            totalMe += meCount

        mp['totalWords'] = totalLength

        mp['averageLength'] = totalSum/totalLength
        averageResults.append([str(mp['averageLength']), mp['name']])

        try: mp['modeLength'] = statistics.mode(lengths)
        except: mp['modeLength'] = -1
        modeResults.append([str(mp['modeLength']), mp['name']])

        mp['medianLength'] = statistics.median(lengths)
        medianResults.append([str(mp['medianLength']), mp['name']])

        mp['meCount'] = totalMe
        meResults.append([mp['meCount'], mp['name'], mp['meCount']/mp['totalWords']*100])



    averageResults = list(reversed(sorted(averageResults)))
    modeResults = list(reversed(sorted(modeResults)))
    medianResults = list(reversed(sorted(medianResults)))
    meResults = sorted(meResults, key=lambda x: x[2] , reverse=True)

    print("TOP 5:")
    print("\nAverage word length: ")
    for i in range(5):
        print averageResults[i][0], " ", averageResults[i][1].encode('utf-8')
    print("\nWord length mode: ")
    for i in range(5):
        print modeResults[i][0], " ", modeResults[i][1].encode('utf-8')
    print("\nMedian word length: ")
    for i in range(5):
        print medianResults[i][0], " ", medianResults[i][1].encode('utf-8')

    print("\nMost occurrences of 'ég': ")
    for i in range(len(mpInfo.keys())):
        print meResults[i][0], " ", meResults[i][1].encode('utf-8'), " %: ", meResults[i][2]

