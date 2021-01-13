from bs4 import BeautifulSoup
from selenium import webdriver
from collections import Counter
from konlpy.tag import Hannanum
from lxml import html
import pytagcloud
import webbrowser
import random
import sys

url = 'http://xnuna.me/'
r = lambda: random.randint(0,255)
color = lambda: (r(), r(), r())


def get_tags(text, ntags=50, multiplier=10):
    print("1")
    h = Hannanum()
    nouns = h.nouns(text)
    count = Counter(nouns)
    print(count)
    print("2")
    return [{'color': color(), 'tag': n, 'size': c*multiplier}\
        for n, c in count.most_common(ntags)]

def draw_cloud(tags, filename, fontname='Cantarell', size=(800, 600)):
    print("3")
    pytagcloud.create_tag_image(tags, filename, fontname=fontname, size=size)
    webbrowser.open(filename)
    print("4")

def crawler():
    driver = webdriver.PhantomJS(executable_path="./phantomjs")
    driver.implicitly_wait(10)
    driver.get(url)
    a = driver.find_elements_by_tag_name("a")
    count =0
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    #print(text)
    tags = get_tags(text)
    draw_cloud(tags, 'wordcloud.png')

    driver.quit()

if __name__ == "__main__":
    crawler()