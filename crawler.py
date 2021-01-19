from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from konlpy.utils import pprint
from konlpy.tag import Okt
from bs4 import BeautifulSoup

okt = Okt()
# 옵션 생성
options = webdriver.ChromeOptions()
# 창 숨기는 옵션 추가
options.add_argument("headless")
options.add_argument('--disable-gpu')
options.add_argument("--log-level=3")
driver = webdriver.Chrome(executable_path="chromedriver.exe",options=options)
#url = "https://yadong2.2on.in/" #야동모아 라는 사이트
url = "http://xnuna.me/" 
DELAY = 1
#driver.get(url)
id_num = 1
i = 1
IsNoPage = 0


url_ = "http://xnuna.me/bbs/board.php?bo_table=ya_kor&wr_id="
#WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.XPATH,'//ul[@id="gnb_1dul"]')))
#print(driver.find_element_by_xpath('//ul[@id="gnb_1dul"]/child::li[2]').text)
while(True):
    crawling_text = ""
    f = open("CrawlingData.txt", 'a')
    driver.get(url_+str(id_num))
    try:
        result = driver.switch_to_alert()
        result.dismiss()
        id_num += 1
        IsNoPage += 1
        if(IsNoPage <= 20):
            continue
        else:
            if(i>=8):
                break
            driver.get(url)
            i += 1
            WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.XPATH, '//ul[@id="gnb_1dul"]')))
            driver.find_element_by_xpath('//ul[@id="gnb_1dul"]/child::li[' + str(i) + ']').click()
            WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.XPATH,'//div[@class="gall_con"]')))
            driver.find_element_by_xpath('//div[@class="gall_con"]').click()
            url_ = driver.current_url
            url_ = url_[:url_.find("id=")+3]
            print(url_)
            id_num = 1
            IsNoPage = 0
            driver.get(url_+str(id_num))
        pass
    except:
        pass
    WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.XPATH, '//i[contains(@class, "fa-clock")]')))
    #full_html = driver.page_source
    html = driver.page_source
    # soup에 넣어주기
    soup = BeautifulSoup(html, 'html.parser')
    date = str(driver.find_element_by_xpath('//i[contains(@class, "fa-clock")]/parent::node ()').text)
    title = soup.select_one('title').get_text()
    crawling_text += str(id_num) + ";"
    crawling_text += title
    crawling_text += ";"
    crawling_text += str(okt.nouns(title)) + ";"
    print(str(id_num) + " ; " + date)
    crawling_text += date + "\n"
    f.write(crawling_text)
    id_num += 1
    IsNoPage = 0
    f.close()

    
#다양한 웹사이트에 적용할수있도록 수정 , 크롤링하는게 안보이도록 수정하면좋음, 모듈화