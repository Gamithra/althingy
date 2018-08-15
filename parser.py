#!/usr/bin/python3

from urllib2 import urlopen
from bs4 import BeautifulSoup

##TODO: refactoring
## after MVP: compare minutes

mpInfo = {}
names = ""

def findnames(_str):
    pass

def data():
    try: 
        page = urlopen("https://www.althingi.is/altext/cv/is/raedur?lthing=148")
    except: 
        return "neibb 1"
    soup = BeautifulSoup(page)
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
    
    urlTemplate = "https://www.althingi.is/altext/cv/is/raedur"

    for key in mpInfo:
        mp = mpInfo[key]
        page = urlopen(urlTemplate + mp['link'])
        soup = BeautifulSoup(page)
        contents = soup.body.find('div', attrs={'class': "article box news"})
        mp['speechLinks'] = []
        for link in contents.find_all('a'):
            newLink = link.get('href')
            if "raeda" in newLink:
                mp['speechLinks'].append(newLink)
    
    
    print(mpInfo[1])
    print(mpInfo[2])

if __name__ == "__main__":
    data()
    mpNames = names
    with open("mp-names.txt", "w") as f:
        f.write(mpNames.encode('utf-8'))
