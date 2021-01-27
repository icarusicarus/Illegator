from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
from selenium import webdriver

def extract_external_link(url, _driver):
    external_link = []

    _driver.get(url)
    html = driver.page_source
    soup = bs(html, 'html.parser')
    a_tags = soup.findAll('a')
    net = urlparse(url).netloc

    for tag in a_tags:
        if not ('href' in tag.attrs):
            continue
        if tag.attrs['href'].startswith('/') or urlparse(tag.attrs['href']).netloc == net:
            continue
        else:
            external_link.append(tag.attrs['href'])

    return external_link



def compare_banner_link(links1, links2):

    count = 0
    for link in links1:
        if links2.__contains__(link):
            count += 1

    print("links1 length: ", len(links1))
    print("links2 length: ", len(links2))
    print("count: ", count)

    result = 0 if count == 0 else count / len(links1 if len(links1) < len(links2) else links2) * 100
    return result


if __name__ == "__main__":
    driver = webdriver.PhantomJS("/usr/local/bin/phantomjs")
    driver.implicitly_wait(3)
    ''' or use chrome webdriver. 
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(
        executable_path="chromedriver_path",
        options=chrome_options)
    '''
    external_link1 = extract_external_link("url1", driver)
    external_link2 = extract_external_link("url2", driver)
    print(compare_banner_link(external_link1, external_link2))
