import os
import re
import sys
import operator
from tqdm import *

# global variables
unigramsTF = {};
bigramsTF = {};
trigramsTF = {};
unigramsIndex = {};
bigramsIndex = {};
trigramsIndex = {};
unigramsDF = {};
bigramsDF = {};
trigramsDF = {};  

def generateNgrams():    # generate ngrams, n = {1, 2, 3}
    global unigrams, bigrams, trigrams;
    for filename in tqdm(os.listdir('Corpus')):
        f = open('Corpus' + '\\' + filename, 'r+');
        src = f.read();
        newSrc = src.split()   # tokenize
        filename = filename[:-4];
        # generate Unigrams
        for i in newSrc:
            if i in unigramsIndex:
                if filename not in unigramsIndex[i]:
                    unigramsIndex[i].update({filename: 1});
                else:
                    unigramsIndex[i][filename] = unigramsIndex[i][filename] + 1;
            else:
                unigramsIndex[i] = {filename: 1};

        # generate Bigrams
        for i in range(0, len(newSrc) - 1):
            bigrm = newSrc[i] + " " + newSrc[i + 1];
            if bigrm in bigramsIndex:
                if filename not in bigramsIndex[bigrm]:
                    bigramsIndex[bigrm].update({filename : 1});
                else:
                    bigramsIndex[bigrm][filename] = bigramsIndex[bigrm][filename] + 1;
            else:
                bigramsIndex[bigrm] = {filename: 1};
                

        # generate Trigrams
        for i in range(0, len(newSrc) - 2):
            trigrm = newSrc[i] + " " + newSrc[i + 1] + " " + newSrc[i + 2];
            if trigrm in trigramsIndex:
                if filename not in trigramsIndex[trigrm]:
                    trigramsIndex[trigrm].update({filename: 1});
                else:
                    trigramsIndex[trigrm][filename] = trigramsIndex[trigrm][filename] + 1;
            else:
                trigramsIndex[trigrm] = {filename: 1};
                
        f.close()

def getCount(dict): # frequency of term
    count = 0
    for i in dict:
        c = dict[i];
        count = count + c;
    return count

def getDocs(dict):  # doc list
    d = "";
    for i in dict:
        d = d + " " + str(i);
    return d;


def storeTFandDF():  # store generated TF and DF
    global unigramsTF, bigramsTF, trigramsTF, unigramsIndex, bigramsIndex, trigramsIndex, unigramsDF, bigramsDF, trigramsDF;

    for i in unigramsIndex: # unigrams
        unigramsTF[i] = getCount(unigramsIndex[i]);
    for i in bigramsIndex:  # bigrams
        bigramsTF[i] = getCount(bigramsIndex[i]);
    for i in trigramsIndex: # trigrams
        trigramsTF[i] = getCount(trigramsIndex[i]);

    # process TF and DF for unigram, bigram and trigrams
    
    processTFFile("Unigram TF.txt", unigramsTF);
    processTFFile("Bigram TF.txt", bigramsTF);
    processTFFile("Trigram TF.txt", trigramsTF);
    processDFFile("Unigram DF.txt", unigramsIndex);
    processDFFile("Bigram DF.txt", bigramsIndex);
    processDFFile("Trigram DF.txt", trigramsIndex);
    
    

def processTFFile(fname, f):  # format and write file with the given filename
    fileName = open(os.path.join("TF and DF", fname), "w");
    data = sorted(f.items(), key = lambda x: (-x[1], x[0]));
    for d in data:
        fileName.write(str(d) + "\n");
    fileName.flush();
    fileName.close();
        

def processDFFile(fname, f):    # format and write file with the given filename
    fileName = open(os.path.join("TF and DF", fname), "w");    
    data = sorted(f, key = operator.itemgetter(0));
    for d in data:
        doc = getDocs(f[d]);
        fileName.write(str(d) + "->" + doc + " " + str(len(f[d])) + "\n");
    fileName.flush();
    fileName.close();

def generateStoplist(): # stop list for very frequent words
    terms = [];
    count = 0;
    with open("TF and DF/Unigram TF.txt","r") as f:
        for line in f:
            line = line.replace("('",'');
            line = line.replace("'", '');
            line = line.replace(")", '');
            terms.append(line);
            count = count + int(line.split(', ')[1]);
    file = open("Stoplist.txt","w")
    for t in terms:
        tf = float(t.split(", ")[1]);
        pr = float(tf / count);
        if( pr <= 0.001):
            continue;   # not very frequent terms
        else:
            file.write(t.split(", ")[0]+"\n");
    file.flush()


def main(): # main method
    try:
        os.mkdir("TF and DF");
    except: # folder exists
        pass;

    generateNgrams();
    storeTFandDF(); # store TF and DF
    generateStoplist(); # generate stop words and store stoplist
    sys.stdout.write("All done ^.^\nLook for the files in root and folder TF and DF.");

main(); # run the program
