from bs4 import BeautifulSoup
from urllib import parse
from selenium import webdriver
from subprocess import Popen, PIPE
import webbrowser
import mysql.connector
import time
import sys
import os


class url_struct:
    def __init__(self, internal, url, depth):
        self.internal = internal  # internal: 1, external: 0
        self.url = url
        self.depth = depth
        self.sc_path = null
        #self.site_type = null


url_list = []
crawled_url = []
crawled_list = []
#keywords = []
#hit_lists = []
#hit_score = []

internal_depth = 3
external_depth = 5
'''
# compare Keywords with texts of html, return matching(hit) list and the number of matched ones(score)
def get_hit_list(keywords, _text):
    hit_list = {}
    score = 0
    for keyword in keywords:
        keyword_count = _text.count(keyword)
        if keyword_count > 0:
            hit_list.update({keyword: keyword_count})
            score += keyword_count
    return [hit_list, score]


# sort by score with [list, [list, list]], the last list contains scores
def sort_by_sum(e):
    return e[1][1]
'''

def execute_command(command):
    result = Popen(command, shell=True, stdout=PIPE).stdout.read()
    if len(result) > 0 and not result.isspace():
        raise Exception(result)


def crop_image(name):
    command = [
        "convert",
        "./screenshot/" + name,
        "-crop",
        "1024x768+0+0",
        "./screenshot/" + name,
    ]
    execute_command(" ".join(command))

def add_url_to_db():
    try:
        query = "INSERT INTO url_info (url, sc_path) VALUES (?, ?);"
        mycursor.executemany(query, (crawled_list.url, crawled_list.sc_path))
        mydb.commit()

def crawler():
    while len(url_list):
        struct = url_list[0]
        crawled_list.append(struct.url)

        if (struct.internal and (struct.depth < internal_depth)) or (
            not struct.internal and (struct.depth < external_depth)
        ):
            driver = webdriver.PhantomJS(
                executable_path="C:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe"
            )
            driver.implicitly_wait(5)
            driver.get(struct.url)
            print("[O] Crawling " + struct.url + "...")
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            text = soup.text
            '''
            list_total_score = get_hit_list(keywords, text)
            hit_lists.append(list_total_score[0])
            hit_score.append(list_total_score[1])
            '''
            net = parse.urlparse(struct.url).netloc

            # get internal/external link and append to url list
            hrefs = soup.findAll("a")
            if len(hrefs):
                for href in hrefs:
                    is_exist = href.get("href")
                    if (
                        is_exist != None
                        and (href.attrs["href"] not in crawled_url)
                        and ("naver" not in href.attrs["href"])
                        and ("daum" not in href.attrs["href"])
                        and ("google" not in href.attrs["href"])
                        and ("nate" not in href.attrs["href"])
                        and ("youtube" not in href.attrs["href"])
                        and ("instagram" not in href.attrs["href"])
                        and ("facebook" not in href.attrs["href"])
                        and ("zum" not in href.attrs["href"])
                    ):
                        if href.attrs["href"].startswith("/"):  # internal link start with /
                            ap = url_struct(1, str(net + href.attrs["href"]), struct.depth + 1)
                            url_list.append(ap)
                            print("[-] Find Internal Link: " + href.attrs["href"])
                        elif parse.urlparse(href.attrs["href"]).netloc == net:  # internal link
                            ap = url_struct(1, str(href.attrs["href"]), struct.depth + 1)
                            url_list.append(ap)
                            print("[-] Find Internal Link: " + href.attrs["href"])
                        elif href.attrs["href"].startswith("http"):  # external link
                            ap = url_struct(0, str(href.attrs["href"]), struct.depth + 1)
                            url_list.append(ap)
                            print("[=] Find External Link: " + href.attrs["href"])
                        else:
                            pass
                    else:
                        pass
            '''
            # Print result of keyword matching
            result = list(zip(url_list, zip(hit_lists, hit_score)))
            result.sort(reverse=True, key=sort_by_sum)

            for r in result:
                print("총계: " + str(r[1][1]) + "\t", r[0], r[1][0])
            '''
            # Take a screenshot
            sc_name = time.strftime("%H%M%S") + net + ".png"
            driver.save_screenshot("./screenshot/" + sc_name)
            # If you wanna cropped image,
            crop_image(sc_name)
            struct.sc_path = sc_name

            print("[+] Take a Screenshot. Crawled Complete. Delete " + struct.url)

            if len(crawled_list) < swapDb:
                crawled_list.append(url_list[0])
            else:
                add_url_to_db()
                crawled_list.append(url_list[0])

            del url_list[0]

        else:
            print("[X] Out of Depth " + struct.url + " (Depth: " + struct.depth + ")...")


if __name__ == "__main__":
    if os.path.isdir("\Screenshot") == False:
        os.mkdir("\Screenshot")

    mydb = mysql.connector.connect(host="localhost", user="illegator", password="!11eGAt0R")
    mycursor = mydb.cursor()
    mycursor.execute("SHOW DATABASES")

    isDbExist = False
    isTableExist = False

    for db in mycursor:
        if db == "datas":
            isDbExist = True
    if isDbExist == False:
        mycursor.execute("CREATE DATABASE datas")

    mycursor.execute("USE datas")
    mycursor.execute("SHOW TABLES")

    for table in mycursor:
        if table == "url_info":
            isTableExist = True
    if isTableExist == False:
        mycursor.execute("CREATE TABLE url_info (
            id INT AUTO_INCREMENT PRIMARY KEY,
            url VARCHAR(255) NOT NULL,
            sc_path VARCHAR(50) NOT NULL,
            #site_type INT NOT NULL
        )")

    start_struct = url_struct(
        0, "https://www.size19.com/li.aspx?k=%ED%95%9C%EA%B5%AD%EC%95%BC%EB%8F%99", 0
    )
    url_list.append(start_struct)

    crawler()
