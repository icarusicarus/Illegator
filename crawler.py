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
    print("2")
    return [{'color': color(), 'tag': n, 'size': c*multiplier}\
        for n, c in count.most_common(ntags)]

def draw_cloud(tags, filename, fontname='Noto Sans CJK', size=(800, 600)):
    print("3")
    pytagcloud.create_tag_image(tags, filename, fontname=fontname, size=size)
    webbrowser.open(filename)
    print("4")

def crawler():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path="C:\\Users\\예령\\Desktop\\Illegator\\chromedriver.exe", options=chrome_options)
    driver.get(url)
    a = driver.find_elements_by_tag_name("a")
    count =0
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    #print(text)
    tags = get_tags(text)
    draw_cloud(tags, 'wordcloud.png')
    print('=================================================================')
    for element in a:
        print(element.get_attribute('innerHTML'))
        print(element.get_attribute('href'))
        count=count+1
        if (count>10) :
            break

    driver.quit()

if __name__ == "__main__":
    crawler()