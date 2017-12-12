import sys
import os
import math
import operator
from collections import OrderedDict
from tqdm import *


def initialize():
    global invertedIndex, queries, corpusDict, corpusSize, k1, b, k2;

    #############################
    #######MAGIC NUMBERS#########
    k1 = 1.2;                   #
    b = 0.75;                   #
    k2 = 100;                   #
    #############################

    corpusDict = {};
    corpusSize = 0;
    invertedIndex = open("Inverted Index - Unigram.txt", "r");

    if not os.path.exists("Tables"):
        os.makedirs("Tables");

    queries = ["hurricane isabel damage",
                     "forecast models",
                     "green energy canada",
                     "heavy rains",
                     "hurricane music lyrics",
                     "accumulated snow",
                     "snow accumulation",
                     "massive blizzards blizzard",
                     "new york city subway"];

## Location string cleaner
def cleanLocation(location):
    location = location.replace('[','').replace(']','').replace('(','').replace(']','').replace('(','').replace('), ','#').replace(')','').replace(' ','').replace("'",'');
    return location;

## Content string cleaner
def cleanContent(content):
    content = content.replace(' ','').replace("\n","").replace("'","");
    return content;

## Build dictionary from locations of content
def buildDictionary(location):
    location = location.split('#');
    dictionary = {};
    for l in location:
        i = l.split(",");
        ref = i[0];
        freq = int(i[1]);
        dictionary[ref] = freq;
    return dictionary;

## Split index into Context and Locations
def indexToContextLocations(index):
    index = index.strip();
    index = index.split(" -> ");
    return index;

## Build the corpus dictionary
def buildCorpusDictionary(dictionary):
    d = {};
    for content in dictionary:
        for doc in dictionary[content]:
            if doc in d:
                d[doc] = d[doc] + dictionary[content][doc];
            else:
                d[doc] = dictionary[content][doc];
    return d;

## Write the output file into the disk in the given format
def writeOutputFile(id, fileName, dictionary):
    fileName = open(fileName,"w")
    rank = 1;
    fileName.write("query_id\t\tQ0\tdoc_id\t\trank\t\tBM25_score\t\tsystem_name\n");
    fileName.write("***********************************************************************************************************************************\n");
    for key in dictionary.keys():   # These are sorted per their BM25 scores
        fileName.write(str(id) + "\t\tQ0" + "\t" + str(key) + "\t\t" + str(rank) + "\t" + str(dictionary[key]) + "\t" + "BM25_System\n"); # System name = BM25_System
        rank = rank + 1;
    fileName.close();

## Return the number of occurances of query terms in the corpus dictionary (TF)
def getTermFrequency(queryTerms):
    global corpusDict;
    tf = {};
    for term in queryTerms:
        count = 0;
        term = term.replace(' ','').replace('\n','').replace("'","");
        if term not in corpusDict:
            docNos = corpusDict[term]
            for d in docNos:
                count = count + docNos[d];
        tf[term] = count;
    return tf;

## Build TD from query terms
def buildTermDocs(queryTerms):
    global corpusDict;
    td = {};
    for word in queryTerms:
        if word not in corpusDict:
            td[word] = None;
        else:
            countDoc = corpusDict[word]
            docs_term = set();
            for dc in countDoc:
                docs_term.add(dc)
                td[word] = docs_term
    return td;


## Build document set
def buildDocSet(queryTerms, td):
    documents = set();
    for term in queryTerms:
        docs = td[term]
        for d in docs:
            documents.add(d);
    return documents;

## Return BM25 Score for given document d
def generateScores(d, queryTerms, dictionary2, td):
    global corpusSize, k1, b, k2;
    arg = dictionary2[d] / float(corpusSize/float(len(dictionary2))); # divide by total number of keys
    score = 0;
    for term in queryTerms:
        if d not in corpusDict[term]:
            ifd = 0;
        else:
            ifd = corpusDict[term][d];
        eq1 = ifd * (k1+1);	  
        eq2 = queryTerms.count(term) * (k2 + 1);
        eq3 = (len(dictionary2) - len(td[term]));
        first = (eq1 /((b * arg) + (k1 * (1-b)) + ifd));
        second = (eq2 / (k2 + queryTerms.count(term)));
        thirdNumerator = 1;
        thirdDenominator = ((len(td[term]) + 0.5) / float (eq3 + 0.5));
        if (not (thirdNumerator < 0 and thirdDenominator > 0) or (thirdNumerator > 0 and thirdDenominator < 0)):
            interim = math.log(thirdNumerator/thirdDenominator) * first * second;
            score = score + interim;
    return score;

## Main method to run the program
def main():
    global invertedIndex, queries, corpusDict, corpusSize, k2;
    initialize();
    for index in tqdm(invertedIndex):
        index = indexToContextLocations(index);
        content = index[0];
        locations = index[1]; 
        
        # cleanup contant and location
        content = cleanContent(content);
        locations = cleanLocation(locations);

        # build dictionary
        dictionary = buildDictionary(locations);

        # map locations to content
        if content not in corpusDict:
            corpusDict[content] = dictionary

    # Build corpus dictionary and calculate size
    dictionary2 = buildCorpusDictionary(corpusDict);
    for key in dictionary2:
            corpusSize += dictionary2[key];

    # Process for each query           
    queryID = 0
    for query in tqdm(queries):
        queryID = queryID + 1;
        queryTerms = query.split(" ");  # split query into query terms
        td = buildTermDocs(queryTerms);  # generate td
        tf = getTermFrequency(queryTerms); # generate tf   
        documents = buildDocSet(queryTerms, td);    # build document set
        # Generate BM25 Scores
        BM25Scores = {};
        for d in documents:
            BM25Scores[d] = generateScores(d, queryTerms, dictionary2, td);

        # Sort dictionary by their BM25 scores
        sortedDict = OrderedDict(sorted(BM25Scores.items(), key=operator.itemgetter(1), reverse=True)[:k2]);

        # Write file to disk with given file name
        fileName = "Tables\\" + query.replace(" ",'_') + ".txt";
        writeOutputFile(queryID, fileName, sortedDict);
        

main(); # run the program
