import math
import operator

## Program constants a.k.a. Magic Numbers which can be changed in one place

d = 0.85;   #d is the PageRank damping/teleportation factor

## Global variables

graphFile = open('G2.txt', 'r');    # graph file
graphPerplexity = open('__Perplexity.txt', 'w'); # graph perplexity file
P = []; # the set of all pages
N = len(P); # |P|
S = []; # the set of sink nodes
M = {}; # M(p) is the set (without duplicates) of pages that link to page p
L = {}; # L(q) is the number of out-links (without duplicates) from page q
pWithOutlinks = []; # pages that have out-links
perplexity = [];    # to check convergence
PR = {};    # page rank
newPR = {}; # new page rank score of each page

def buildInlinks():
    global M;
    for link in graphFile:
        links = link.split();
        if(len(links) <= 1):
            M[links[0]] = [];
        else:
            M[links[0]] = links[1:];

def buildOutlinks():
    global P, L;    
    for page in P:
        for p in M[page]:
            L[p].append(page);

def buildSetup():  # Setup sink nodes, and page with outlinks
    global P, L;
    for page in P:
        if(len(L[page]) == 0):   # No outlinks
            S.append(page);
        else:   # has outlinks
            pWithOutlinks.append(page);

def checkConvergence():
    global perplexity;
    oldP = 100;
    counter = 0;
    for p in perplexity:
        if(abs(oldP - p) < 1):
            counter += 1;
        else:
            counter = 0;
        oldP = p;

    if(counter >= 4):
        return True;
    return False;

def buildPerplexity():
    global PR, perplexity, graphPerplexity;
    entropy = 0;
    for rank in PR.values():
        entropy += (rank * math.log(rank, 2)) * -1;
    perplexity.append(math.pow(2, entropy));
    graphPerplexity.write(str(math.pow(2, entropy)) + "\n");

def buildPageRank():
    global N, P, PR, sinkPR, M, newPR, graphPerplexity, d;
    N = len(P);
    for page in P:
        PR[page] = 1.0/N;
    while not checkConvergence():
        buildPerplexity();
        sinkPR = 0;
        for page in S:  # sink nodes
            sinkPR += PR[page];
        for page in P:  # all pages
            newPR[page] = ((1.0-d) / N);
            newPR[page] += d * sinkPR / N;
            for q in M[page]:
                newPR[page] += d * PR[q]/len(L[q]);
        for page in P:  # update PR with new PR
            PR[page] = newPR[page];        
    graphPerplexity.close();

def initialize():   # set up inlinks and outlinks and variables
    global P, N, M, L, S;
    buildInlinks();
    P = M.keys();
    N = len(P);
    for page in P:  # initialize L as empty
        L[page] = [];
    buildOutlinks();
    buildSetup();

def main():
    initialize();
    buildPageRank();
    ## Sort and store pages by rank
    sortedPR = sorted(PR.items(), key=operator.itemgetter(1),reverse=True);
    prFile = open('__PRscore.txt', 'w') # the urls are stored in this file
    fileNum = 0;
    for i in sortedPR:
        if fileNum < 50:   # Top 50 pages
            prFile.write(str(i[0])+ " " + str(i[1]) +'\n');
            fileNum += 1;
    prFile.close();
    print("All done ^.^\nPlease find files __PRscore.txt and __Perplexity.txt in dir");

main();
        
