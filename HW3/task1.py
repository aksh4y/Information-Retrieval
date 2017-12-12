import os
from bs4 import BeautifulSoup
from tqdm import *
import re
import sys

def cleanup(content):   # Remove unsupported ASCII, tabs, carriage return and backspaces
        content = removeNewline(content);
        content = removeBackspace(content);
        content = removeTabs(content);
        content = removeSymbols(content);
        content = removeExtendedASCII(content);
        return content;
        

def removeExtendedASCII(content):   # remove unnecessary ASCII characters
    newContent = '';
    for char in content:
        if ord(char) > 128 or ord(char) == 11 or ord(char)==9 or ord(char)==13:
            char = '';
        newContent+= char;
    return newContent;

def foldCase(content):  # convert upper case English alphabets to lower case
    newContent = '';
    for char in content:
        if ord(char) >= 65 and ord(char)<=91:
            char=chr(ord(char)+32);
        newContent+= char;
    return newContent;

def removeBackspace(content):   # remove all backspaces
    content = content.replace('\\b', '');
    return content;

def removeNewline(content): # remove all new lines
    content = content.replace('\\n', '');
    return content;

def removeTabs(content):    # remove all tabs
    content = content.replace('\\t', '');
    return content;

def removeUrls(content):    # remove URLs from content using the given regEx
    regEx='http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+';
    urls=re.findall(regEx,content);
    for url in urls:
        content = content.replace(url,'');
    return content;

def removePunctuation(content): # remove punctuations that are not in between digits
    symbols = ['.',',']
    digits = ['0','1','3','4','5','6','7','8','9'];
    i = 1;
    newContent = '';
    for char in content:
        if char in symbols and i != len(content) - 1 and (content[i - 1] not in digits or content[i + 1] not in digits):  # preserve punctuation between digits
            char = '';
        newContent = newContent + char;
        i+= 1;
    return newContent;

def removeSymbols(content): # remove extra symbols
    symbols = ['%', '&', '@', '#', '$', '*','~','|','\\','/'];
    newContent = '';
    for char in content:
        if char in symbols:
            char = '';
        newContent+= char;
    return newContent;

def buildCorpus(extra): # method to build the corpus
    try:
        os.mkdir('Corpus');
    except:     # folder exists
        pass;

    for file in tqdm(os.listdir("Source files")): # parse and tokenize each file in dir
        with open('Source files/'+file, 'r') as source:
            content = source.read();
            content = content.decode('utf-8');
            soup = BeautifulSoup(content,"html.parser");
            for tags in soup('script'): # remove all html tags
                tags.extract();
            text = soup.get_text(); # main content
            if(extra != "-c"):
                text = removePunctuation(text); # remove punctuations
                text = foldCase(text);  # fold case
            text = removeUrls(text);    # remove URLs
            text = cleanup(text);   # extended cleanup
            treatedFile = open('Corpus/'+file,"w"); # create new file for writing
            treatedFile.write(text);    # write file
            treatedFile.flush();
    sys.stdout.write('All done ^.^\nFind the generated corpus in the Corpus folder.');

def main(): # main method to check options for building corpus
    sys.stdout.write("Generating Corpus...\n");
    if(len(sys.argv) == 2 and sys.argv[1] == "-c"):
        buildCorpus(sys.argv[1]);   # build corpus without text folding and punctuation handling. Other cleanup methods are not optional
    elif(len(sys.argv) == 1):
        buildCorpus(None); # Default for building corpus with text folding and punctuation handling
    
main(); # run the program
