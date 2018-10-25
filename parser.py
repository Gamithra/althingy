#!/usr/bin/python3

from urllib2 import urlopen
import pickle
from bs4 import BeautifulSoup


mpInfo = {}
names = ""


def data():
    try:
        page = urlopen("https://www.althingi.is/altext/cv/is/raedur?lthing=148")
    except:
        return "page not found"

    soup = BeautifulSoup(page, "lxml")
    contents = soup.body.find('div', attrs={'class': "article box news"})
    names = contents.text.split("\n")
    mp = dict()

    id = 1
    for i in range(len(names)):
        if str(names[i].encode('utf-8')) != "" and "1" not in str(names[i].encode('utf-8')):
            mp['name'] = names[i]
            mpInfo[id] = dict(mp)
            id += 1

    linkIndex = mpInfo.keys()[0]
    for link in contents.find_all('a'):
        try:
            mpInfo[linkIndex]['link'] = link.get('href')
            linkIndex += 1
        except: pass
    print ("got names")
    urlTemplate = "https://www.althingi.is/altext/cv/is/raedur"

    for key in mpInfo:
        mp = mpInfo[key]
        page = urlopen(urlTemplate + mp['link'])
        soup = BeautifulSoup(page, "lxml")
        contents = soup.body.find('div', attrs={'class': "article box news"})
        mp['speechLinks'] = []
        for link in contents.find_all('a'):
            newLink = link.get('href')
            if "raeda" in newLink:
                mp['speechLinks'].append(newLink)

        speechUrlTemplate = "https://www.althingi.is"
        mp['speeches'] = []
        for link in mp['speechLinks']:
            page = urlopen(speechUrlTemplate + link)
            soup = BeautifulSoup(page, "lxml")
            contents = soup.body.find('div', attrs={'id': "raeda_efni"}).text
            mp['speeches'].append(contents)


if __name__ == "__main__":
    data()
    with open("mpInfo.pkl", 'wb') as f:
        pickle.dump(mpInfo, f, pickle.HIGHEST_PROTOCOL)
