from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from konlpy.utils import pprint
from konlpy.tag import Okt
okt = Okt()

driver = webdriver.Chrome(executable_path="chromedriver.exe")
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
    WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.XPATH, '//span[@class="bo_v_tit"]')))
    title = driver.find_element_by_xpath('//span[@class="bo_v_tit"]').text
    crawling_text += str(id_num) + " | "
    crawling_text += title
    crawling_text += " | "
    crawling_text += str(okt.nouns(title)) + " | "
    print(str(id_num) + " | " + str(driver.find_element_by_xpath('//strong[@class="if_date"]').text))
    crawling_text += str(driver.find_element_by_xpath('//strong[@class="if_date"]').text) + "\n"
    f.write(crawling_text)
    id_num += 1
    IsNoPage = 0
    f.close()
