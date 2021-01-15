from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium import webdriver
from collections import Counter
from konlpy.tag import Hannanum
from subprocess import Popen, PIPE
from lxml import html
import pytagcloud
import webbrowser
import random
import sys
import os

class url_struct:
    def __init__(self, internal, url, depth):
        self.internal = internal    # internal: 1, external: 0
        self.url = url
        self.depth = depth

url_list = []
crawled_list = []

internal_depth = 3
external_depth = 5

r = lambda: random.randint(0,255)
color = lambda: (r(), r(), r())

def execute_command(command):
    result = Popen(command, shell=True, stdout=PIPE).stdout.read()
    if len(result) > 0 and not result.isspace():
        raise Exception(result)

def get_tags(text, ntags=50, multiplier=10):
    h = Hannanum()
    nouns = h.nouns(text)
    count = Counter(nouns)
    print(count)
    return [{'color': color(), 'tag': n, 'size': c*multiplier}\
        for n, c in count.most_common(ntags)]

def draw_cloud(tags, filename, fontname='Cantarell', size=(800, 600)):
    pytagcloud.create_tag_image(tags, filename, fontname=fontname, size=size)
    webbrowser.open(filename)

def crawler():
    while(len(url_list)):
        struct = url_list[0]
        crawled_list.append(struct.url)

        if((struct.internal and (struct.depth < internal_depth)) or (not struct.internal and (struct.depth < external_depth))):
            driver = webdriver.PhantomJS(executable_path="./phantomjs")
            driver.implicitly_wait(3)
            driver.get(struct.url)
            print("[O] Crawling " + struct.url + "...")
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # get internal/external link and append to url list            
            net = urlparse(struct.url).netloc

            hrefs = soup.findAll("a")
            for href in hrefs:
                if href not in crawled_list:
                    if href.attrs["href"].startswith('/'):                                   # internal link start with /
                        ap = url_struct(1, str(net + href.attrs["href"]), struct.depth + 1)
                        url_list.append(ap)
                        print("[-] Find Internal Link: " + href.attrs["href"])
                    elif (urlparse(href.attrs["href"]).netloc == net):                      # internal link
                        ap = url_struct(1, str(href.attrs["href"]), struct.depth + 1)
                        url_list.append(ap)
                        print("[-] Find Internal Link: " + href.attrs["href"])
                    else:                                                                   # external link
                        ap = url_struct(0, str(href.attrs["href"]), struct.depth + 1)
                        url_list.append(ap)
                        print("[=] Find External Link: " + href.attrs["href"])
            
            driver.save_screenshot('./screenshot/' + net + '.png')

            # crop image
            # you need intall npm, nodejs, imagemagick
            
            command = [
                'convert',
                './screenshot/' + net + '.png',
                '-crop', '1024x768+0+0',
                './screenshot/' + net + '_crop.png'
            ]
            execute_command(' '.join(command))

            print("[+] Take a Screenshot. Crawled Complete. Delete " + struct.url)

            del url_list[0]

        # exit()  # for test. i will expand to continuos crawling

            #text = soup.get_text()
            #tags = get_tags(text)
            #draw_cloud(tags, 'wordcloud.png')

if __name__ == "__main__":
    start_struct = url_struct(0, "filterd", 0)
    url_list.append(start_struct)

    crawler()