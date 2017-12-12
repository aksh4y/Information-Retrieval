import os
import sys
from tqdm import *

# global variables
unigrams = {};
bigrams = {};
trigrams = {};
unigramsIndex = {};
bigramsIndex = {};
trigramsIndex = {};
unigramTokens = {};
bigramTokens = {};
trigramTokens = {};  

def generateNgrams(content):    # generate ngrams, n = {1, 2, 3}
    global unigrams, bigrams, trigrams;
    # generate unigrams
    unigrams = content.split(); # tokenize
    # generate bigrams
    lst = list();
    for c in range(len(unigrams) - 1):
        lst.append(unigrams[c] + " " + unigrams[c+1]);
    bigrams = lst;
    # generate trigrams
    lst = list();   # empty lst
    for c in range(len(unigrams) - 2):
        lst.append(unigrams[c] + " " + unigrams[c+1] + " " + unigrams[c+2]);
    trigrams = lst;

def generateInvertedIndex(docID):   # generate inverted indexes
    global unigrams, bigrams, trigrams, unigramsIndex, bigramsIndex, trigramsIndex;
    createIndex(unigrams, docID, unigramsIndex, 1);
    createIndex(bigrams, docID, bigramsIndex, 2);
    createIndex(trigrams, docID, trigramsIndex, 3);

def createIndex(ngram, docID, index, i):   # helper function to
    global unigramsIndex, bigramsIndex, trigramsIndex;
    for term in set(ngram):
        i = (docID, ngram.count(term));
        if term in index:
            #unigramsIndex[term] = unigramsIndex[term].append(i);
            newIndex  = index[term];
            newIndex.append(i);
            index[term] = newIndex;
        else:
            index[term] = [i];
    if(i == 1):
        unigramsIndex = index;
    elif(i == 2):
        bigramsIndex = index;
    else:
        trigramsIndex = index;

def generateTokens(docID):  # generate tokens for ngrams
    global unigrams, bigrams, trigrams, unigramTokens, bigramTokens, trigramTokens;
    unigramTokens[docID] = len(set(unigrams));
    bigramTokens[docID] = len(set(bigrams));
    trigramTokens[docID] = len(set(trigrams));

def storeIndexandTokens():  # store generated indexes and tokens
    global unigramTokens, bigramTokens, trigramTokens, unigramsIndex, bigramsIndex, trigramsIndex;
    processFile("Inverted Index - Unigram.txt", unigramsIndex);
    processFile("Inverted Index - Bigram.txt", bigramsIndex);
    processFile("Inverted Index - Trigram.txt", trigramsIndex);
    processFile("Token Count - Unigram.txt", unigramTokens);
    processFile("Token Count - Bigram.txt", bigramTokens);
    processFile("Token Count - Trigram.txt", trigramTokens);
    

def processFile(fname, f):  # hekper function to pass params to write file
    fileName = open(os.path.join("Index and Tokens", fname), "w");
    writeFile(fileName, f);
    fileName.flush();
    fileName.close();

    
def writeFile(fname, f):    # format and write file with the given filename
    for term in f:
        fname.write(term + " -> " + str(f[term]) + "\n");
        

def main(): # main method
    try:
        os.mkdir("Index and Tokens");
    except: # folder exists
        pass;
    for file in tqdm(os.listdir("Corpus/")):    # iterate through all files in corpus
        f = open("Corpus/" + file, "r");
        content = f.read();
        generateNgrams(content);    # generate ngrams
        docID = str(file);  # assign article title as docID
        docID = docID[:-4]; # remove extension ".txt"
        generateInvertedIndex(docID);   # generate inverted index
        generateTokens(docID);  # generate token count
        f.close();
    storeIndexandTokens();  # store index and token count
    sys.stdout.write("All done ^.^\nLook for the files in folder Index and Tokens.");

main(); # run the program
