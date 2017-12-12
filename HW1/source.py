import sys
import urllib.request
import re
import time
import re
from bs4 import BeautifulSoup

## Program constants which can be changed in one place
SEED_URL = "https://en.wikipedia.org/wiki/Tropical_cyclone";
MAX_DEPTH = 6;
MAX_URLS = 1000;

## Global Variables
urlsCrawled = [];    # List of all crawled URLs
visited = [];   # List of visited nodes
urlsFile = open('urls_file.txt', 'a'); # file to hold the scraped urls
filenameCount = 1;  # Counter used as label to name source files

## Helper method to parse and crawl the seed URL
def getUrls(url, keyword):
    global visited;
    if(checkUrl(url) and url not in visited):
        src = urllib.request.urlopen(url).read();
        if(keyword != None):
            if(checkMatch(url, keyword)):
                parseUrl(src);
            return crawlUrl(url, keyword);
        else:
            parseUrl(src);
            return crawlUrl(url, None);
    else:
        return 0;
    
## Parses the file and stores it with the respective label
def parseUrl(source):
    global filenameCount;
    soup = BeautifulSoup(source, "html.parser");
    fileSource = open("data_source_" + str(filenameCount) + ".txt", 'w');
    fileSource.write(str(soup.encode("utf-8")))
    fileSource.close();
    filenameCount += 1;
    sys.stdout.write('.');
    sys.stdout.flush();
    
## Helper method to crawl the given URL and return length of child URLs
def crawlUrl(url, keyword):
    global visited, urlsFile;
    visited.append(url);
    urlsFile.write(url + "\n");
    childUrls = getChildUrls(url, keyword);
    return len(childUrls) + 1;

## Get all child URLs of a given URL and return it as a list
def getChildUrls(url, keyword):
    global filenameCount, urlsCrawled, visited, urlsFile, MAX_URLS;
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser");
    for link in soup.findAll('a', href = True): # Traverse all links
        href = link.get('href');
        href = urllib.parse.urljoin(url, href);
        if(checkUrl(link['href'])
           and href not in visited
           and filenameCount <= MAX_URLS):   # Shallow levels (depth) given priority
               if(checkMatch(href, keyword)
                or checkMatch(link.text, keyword)):
                    urlsCrawled.append(href);   # Append to crawled
                    visited.append(href);   # Append to visited
                    urlsFile.write(href + "\n");    # Write URL to file
                    parseUrl(urllib.request.urlopen(href).read());  #Write source code to file
    urlsCrawled.pop(0); # Pop to avoid crawling again          
    return list(set(urlsCrawled));  # Return all child URLs found

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

## Returns true iff the keyword is present in the source file
def checkMatch(source, keyword):
    if(keyword == None):
        return True;
    source = source.lower();
    keyword = keyword.lower();
    pureMatches = re.findall(re.escape(keyword), str(source));
    secondaryMatches = re.findall(keyword + ".", str(source));
    if(pureMatches or secondaryMatches):
        return True;
    else:
        return False;

## Method to start the crawling process
def main(seedUrl, keyword):
        global urlsCrawled, SEED_URL, MAX_DEPTH, MAX_URLS;
        if(seedUrl == None):    # No arguments passed
            url = SEED_URL;
        else:
            url = seedUrl;
        urlsCrawled.append(url);
        depth = 1;
        totalUrls = getUrls(url, keyword);
        while depth <= MAX_DEPTH and filenameCount <= MAX_URLS: #Stop when depth = MAX_DEPTH or when file count reaches MAX_URLS whichever earlier
            count = 0;
            while totalUrls > 0 and filenameCount <= MAX_URLS and urlsCrawled: #Stop when either there are no more URLs or if we have reached MAX_URLS
                count += getUrls(urlsCrawled[0], keyword);    # Fresh crawling
                time.sleep(1);
                totalUrls -= 1;
                if totalUrls == 0:
                    totalUrls = count;
                    break;
            depth += 1;

def begin():
    print("Begun Crawling. Please be patient...");
    sys.stdout.write("Crawling.");
    sys.stdout.flush();
    if(len(sys.argv) == 3):
        main(sys.argv[1], sys.argv[2]);
    elif(len(sys.argv) == 1):
        main(None, None); # Calling the main method with no arguments

begin();    # Start the program
urlsFile.close();   # Close urlsFile
print('\nFinished crawling. Check dir for source files ^.^');

