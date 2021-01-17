from bs4 import BeautifulSoup
from urllib import parse
from selenium import webdriver
from subprocess import Popen, PIPE
import webbrowser
import time
import sys
import os


class url_struct:
    def __init__(self, internal, url, depth):
        self.internal = internal  # internal: 1, external: 0
        self.url = url
        self.depth = depth


url_list = []
crawled_list = []

internal_depth = 3
external_depth = 5


def execute_command(command):
    result = Popen(command, shell=True, stdout=PIPE).stdout.read()
    if len(result) > 0 and not result.isspace():
        raise Exception(result)


def crop_image(net):
    command = [
        "convert",
        "./screenshot/" + net + ".png",
        "-crop",
        "1024x768+0+0",
        "./screenshot/" + net + "_crop.png",
    ]
    execute_command(" ".join(command))


def crawler():
    while len(url_list):
        struct = url_list[0]
        crawled_list.append(struct.url)

        if (struct.internal and (struct.depth < internal_depth)) or (
            not struct.internal and (struct.depth < external_depth)
        ):
            driver = webdriver.PhantomJS(executable_path="./phantomjs")
            driver.implicitly_wait(5)
            driver.get(struct.url)
            print("[O] Crawling " + struct.url + "...")
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            net = parse.urlparse(struct.url).netloc

            # get internal/external link and append to url list
            hrefs = soup.findAll("a")
            if len(hrefs):
                for href in hrefs:
                    is_exist = href.get("href")
                    if (
                        is_exist != None
                        and (href.attrs["href"] not in crawled_list)
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

            driver.save_screenshot("./screenshot/" + net + time.strftime("%H%M%S") + ".png")
            # If you wanna cropped image,
            # crop_image(net)

            print("[+] Take a Screenshot. Crawled Complete. Delete " + struct.url)

            del url_list[0]

        else:
            print("[X] Out of Depth " + struct.url + " (Depth: " + struct.depth + ")...")


if __name__ == "__main__":
    start_struct = url_struct(0, "filtered", 0)
    url_list.append(start_struct)

    crawler()