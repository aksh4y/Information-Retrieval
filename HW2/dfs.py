import urllib.request
import time
from bs4 import BeautifulSoup

#returns the seed url
def getSeedUrl():
    userurl = "https://en.wikipedia.org/wiki/Tropical_cyclone";
    return userurl

#function that returns true iff the conditions are met as specified in question
def checkCond(tagvalue):
    if tagvalue.startswith("/wiki/"):
        if (not tagvalue.__contains__(":")):
            if (not tagvalue.__contains__("Main_Page")):
                    if(not tagvalue.__contains__("#")):
                        return True
    else:
        return False

url = getSeedUrl()
urls = [url]   #a list implemented as a queue which stores the urls
visited = [url] #a list which stores the pages already crawled
urlsss = open('dfs_urls.txt', 'a') # the urls are stored in this file
urlsss.write(url + '\n')
urlwrite = 1 # counter that limits the urls in file to 1000

def getUrls (surl, d):
    global depth, urlwrite
    time.sleep(1) #politeness policy
    htmltext = urllib.request.urlopen(surl).read();
    #using BeautifulSoup to parse the html page
    soup = BeautifulSoup(htmltext, "html.parser") #gets the source code of the page
    for tag in soup.findAll('a', href=True):
        if checkCond(tag['href']):
            tag['href'] = urllib.parse.urljoin(url,tag['href'])
            #only unique URLs are allowed in the urls list and 1000 URLs are saved
            if tag['href'] not in urls and urlwrite < 1000:
                urlsss.write(tag['href']+ '\n')
                urls.append(tag['href'])
                urlwrite = urlwrite + 1
                visited.append(tag['href'])
                print(d);
                if d == 6:
                    continue
                getUrls(tag['href'], d + 1)

getUrls(url, 0)
urlsss.close()
print('Crawl Successful')
