import os
from bs4 import BeautifulSoup
import socket
import sys
import requests
import re

docIdList=[]
urlList=[]
graph={'':[]}

def generateDocIds(): 
        with open("task1E_URLs.txt","r") as f:
           for line in f:
                
                urlList.append(line.replace('\n',''))
                lineArray=line.split('/')
                docIdList.append(lineArray[len(lineArray)-1].replace('\n',''))
        #print urlList
                
        #print docIdList
        for line in docIdList:
                url='https://en.wikipedia.org/wiki/' + line
                #print url
                #source_txt=(urllib.request.urlopen(urlObj.url)).read()
                source_txt = requests.get(url)
                plain_txt = source_txt.text.encode('utf-8')
                soup = BeautifulSoup(plain_txt, "html.parser")
                for txt in soup.findAll('a'): # finding all the elements on the page
                        var = txt.get('href')
                        if var is not None:
                                # we do not need images and colon and main page
                                if checkUrl(var) and '.jpg' not in var and 'JPG' not in var and '.jpeg' not in var:
                                        if var.find('/wiki/') is 0:
                                                print(var);
                                                a = 'https://en.wikipedia.org' + var
                                                #print a
                                                if a in urlList:
                                                        docArr=a.split('/')
                                                        docId=docArr[len(docArr)-1].replace('\n','')
                                                        #print docId
                                                        if docId not in graph:
                                                                listD=[]
                                                                listD.append(line)
                                                                graph[docId]=listD
                                                                #print graph
                                                        else:
                                                                listD=graph[docId]
                                                                if line not in listD:
                                                                        listD.append(line)
                                                                        graph[docId]=listD
                                                        
        
        return graph


## Helper method to check if a given URL matches our conditions
## namely correct Wikipedia link, English link, non-administrative link,
## not a link of the same page and not the Wikipedia main page
def checkUrl(url):
    link = str(url);
    if(isWikiPattern(link)
       and not isMainPage(link)
       and not isAdministrativeLink(link)
       and not isSamePageLink(link)):
           return True;
    else:
       return False;

## Returns true iff the given link is the Wikipedia main page
def isMainPage(link):
    if("/wiki/Main_Page" in repr(link)):
        return True;
    else:
        return False;

## Returns true iff the given link is an administrative link (:)    
def isAdministrativeLink(link):
        link = re.sub('https:', '', link);
        if(":" in link):
            return True;
        else: 
            return False;

## Returns true iff the given link is a link of the same page (#)
def isSamePageLink(link):
        if("#" in link):
            return True
        else:
            return False

## Returns true iff the given URL has the correct wiki pattern 
def isWikiPattern(url): 
	wikiPattern = "/wiki/"
	wikipediaPattern = "//en.wikipedia.org"
	fullPattern = wikipediaPattern + wikiPattern
	if(url and wikiPattern in url[0:6] or fullPattern in url[0:50]):
	    return True
	else:
	    return False



def main():
        docGraph=generateDocIds()
        fileWrite=open("G1_2.txt","w")
        keys=docGraph.keys()
        for key in keys:
                inlinks=docGraph.get(key)
                fileWrite.write(key+' ')
                for docs in inlinks:
                        fileWrite.write(docs+' ')
                fileWrite.write('\n')
				
        #fileWrite.flush()
main()
