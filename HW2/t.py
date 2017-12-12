import urllib
from bs4 import BeautifulSoup
import requests

in_file = open("dfs_urls.txt", 'r')
domain_name = 'https://en.wikipedia.org/wiki/'
domain_name2 = 'https://en.wikipedia.org/'
inlink_dict = {}
count = 0
for links in in_file.readlines():
    link = links.strip('\n')[30:]
    inlink_dict[link] = []

print(inlink_dict)

for links in inlink_dict:
    count += 1
    print(count)
    seed_page = domain_name + links
    html_text = requests.get(seed_page).text.encode('ascii', 'replace')
    soup = BeautifulSoup(html_text, "html.parser")
    hrefs = soup.findAll('a', href=True)
    for tags in hrefs:
        tags['href'] = urllib.parse.urljoin(domain_name2, tags['href'])
        link = tags['href']
        if link[30:] in inlink_dict.keys() and links not in inlink_dict[link[30:]] and links != link[30:]:
            inlink_dict[link[30:]].append(links)

out_file = open("G2.txt", 'w')
for i in inlink_dict:
    out_file.write(i)
    for j in inlink_dict[i]:
        out_file.write(' ' + str(j))
    out_file.write('\n')

out_file.close()




