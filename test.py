from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# 옵션 생성
options = webdriver.ChromeOptions()
# 창 숨기는 옵션 추가
options.add_argument("headless")
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(executable_path="chromedriver.exe",options=options)
url = "https://ddaltime42.com/bbs/board.php?bo_table=best&wr_id=5070" 

DELAY = 1
driver.get(url)
WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.XPATH, '//i[contains(@class, "fa-clock")]')))
a = driver.find_element_by_xpath('//i[contains(@class, "fa-clock")]/parent::node ()').text
print(a)
#full_html = driver.page_source
html = driver.page_source

# soup에 넣어주기
soup = BeautifulSoup(html, 'html.parser')
print(soup.select_one('title').get_text())
#soup = BeautifulSoup( full_html,'html.parser')

'''
import re
p = re.compile(r'(\d{1,2})-(\d{1,2})')
m = p.search('2021-01-26에는 생일입니다.')
print(m)
'''