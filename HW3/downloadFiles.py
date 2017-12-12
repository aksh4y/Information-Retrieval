from bs4 import BeautifulSoup
import urllib.request
import sys

## Parses the file and stores it with the respective label
def parse(source, link):
    soup = BeautifulSoup(source, "html.parser");
    fileSource = open(str(x[30:]) + ".txt", 'w');
    fileSource.write(str(soup.encode("utf-8")))
    fileSource.close();
    sys.stdout.write('.');
    sys.stdout.flush();
    
with open("urls_file.txt") as f:
    content = f.readlines()
# remove \n at the end of each line
content = [x.strip() for x in content]

for x in content:
    parse(urllib.request.urlopen(x).read(), x);

print("Done ^.^");
