### Running the program ###

TASK 1
------------
Step 1) Find a machine with Java 7+
Step 2) Create a Java project with the given HW4.java file (preferably using Eclipse)
Step 3) Add the required Lucene library jars to the project
Step 4) Ensure the corpus is provided in the "src/Corpus" folder or else change the location in line 59
Step 5) Queries are harcoded in line 95. Can be changed from there.
Step 6) Run the program using the IDE or java command depending on setup
Step 7) Find the relevant generated result printed in the console and the index files generated in the "src/index" folder

NOTE: A "Task 1 Output" folder is provided with the generated output for easy access

TASK 2
------------

Step 1) Find a machine with Python 2.7
Step 2) Ensure the inverted index of unigrams in given in the root folder as "Inverted Index - Unigram.txt" or change the name of the file in the invertedIndex variable in the program under the initialize() function
Step 3) Queries are hardcoded in the queries array. This can be found and changed under the initialize() function as well.
Step 4) All magic numbers i.e. k1, b, k2 are also given under the initialize() function and can be subsequently changed there.
Step 5) Run the program using the python command (python, python2, py <- depending on environment setup) followed by task2.py
Step 5) Wait for the algorithm to generate the table for each query
Step 6) Find the relevant files in the Tables folder in root

### Citations ###

Libraries: 	tqdm to display progress of program
Resources for BM25: https://www.quora.com/How-does-BM25-work and formula: https://xapian.org/docs/bm25.html