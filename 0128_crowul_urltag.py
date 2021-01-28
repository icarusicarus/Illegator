#0128 crowl.py

from bs4 import BeautifulSoup  as bs    #BeautifulSoup 을 bs로 명명하여 사용.
import requests

find_url_list = []  
open_tags = []  #2차원
open_tags_num = []
cmp_url = []    #2차원
urls_cons = [] #2차원

def crol_web_site(url_list, target_url):

        #실제 합칠떄는 이렇게가 아니라, 다른 곳에서 url을 받아오는 방식.

    url_list.append(target_url)
    
    for url in url_list:

        webpage = requests.get(url)
        soup = bs(webpage.content, "html.parser")
        all_tags = [tag.name for tag in soup.find_all()]

        open_tags.append(all_tags[:int(len(all_tags)/2)])
        open_tags_num.append(int(len(all_tags)))

    al_tags = ['a', 'html','head','body','title','meta', 'div' , 'script',
    'i','link', 'img', 'span', 'li','ul', 'style', 'p','br', 'h2', 'input',
      'h1', 'form', 'h3', 'nav', 'footer','header','iframe','button','strong',
    'base','main']
    alt_tags = ['a','b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
     'l', 'm', 'n', 'o','p','q','r','x','t','u','v','w', 'x', 'y', 'z','1','2','3','4']
    etc_tag = '7'
    i = 0
    j = 0 
    k = 0
    for url in open_tags:
        j = 0
        for ith_url in url:
            k = 0
            for search_tag in al_tags:
                if search_tag == ith_url:
                    open_tags[i][j] = alt_tags[k]
                    break
                k = k+1
            if k >= len(alt_tags):
                open_tags[i][j] = etc_tag
            j = j+1
        i = i+1


def lcs_urlTag(target_url, compare_url):
    
    #: 입력된 두개의 인자를 가지고 테이블을 만들기
    width = len(target_url) + 1
    height = len(compare_url) + 1

    # 테이블 초기화 빈값으로 초기화시키기
    table = [''] * width * height

    def getTable(r, c):
        return table[r * width + c]

    def setTable(r, c, value):
        table[r * width + c] = value

    for i in range(1, height):
        for j in range(1, width):
                if target_url[ j - 1] == compare_url[ i - 1]:
                    value = getTable( i - 1, j - 1) + target_url[j - 1]
                    setTable(i, j, value)
                    continue

                searched_span_lcs = getTable(i - 1, j)
                text_lcs = getTable(i, j - 1)

                if len(searched_span_lcs) > len(text_lcs):
                    setTable(i, j, searched_span_lcs)

                else:
                    setTable(i, j, text_lcs)
    return getTable(height - 1, width - 1)


def compare_url_tags():

        i = 0
        target_str = "".join(open_tags[len(open_tags)-1])
        target_tag_len = len(target_str)

        tmp_cmp = []
        for ith_open_tags  in open_tags:   #기준 url
            
            tmp_ith_str = "".join(ith_open_tags)

            if i == (len(open_tags) - 1):
                break

            else:
                result = lcs_urlTag(target_str, tmp_ith_str)
                tmp_res_leng = (len(result) / target_tag_len) 
                tmp_cmp.append(round(tmp_res_leng , 4) )    
            i = i+1
        cmp_url.append(tmp_cmp)
        i = 0
        tmp_cmp = []
        for ith_open_tags  in open_tags:   #기준 url
            
            tmp_ith_str = "".join(ith_open_tags)
            ith_tag_len = len(tmp_ith_str)

            if i == (len(open_tags) - 1):
                break

            else:
                result = lcs_urlTag(tmp_ith_str, target_str)
                tmp_res_leng = (len(result) / ith_tag_len) 
                tmp_cmp.append(round(tmp_res_leng , 4) )    
            i = i+1
        cmp_url.append(tmp_cmp)

        for y in range(0 , 1):
            lis_x = 0
            tmp_cons = []
            print(cmp_url[y])
            print(cmp_url[y+1])
            for x in cmp_url[y]:
                if lis_x == len(cmp_url[y]):
                    break
                else:
                    if x > 0.7 and cmp_url[1][lis_x] > 0.7:
                        tmp_cons.append('동일')

                    elif x > 0.4 and cmp_url[1][lis_x] > 0.4:
                        tmp_cons.append('유사')

                    else:
                        tmp_cons.append('다름')
                
                    lis_x = lis_x + 1
            urls_cons.append(tmp_cons)
            
                # 0.7 이상은 자기 자신 or 같은 구조(같은 T로 추정됨).
                # 0.~0.7 은 유사 구조.(그러나 다른 T)
                # 0.5 이하는 다른 구조.
        for x in urls_cons:
            print(x)

crol_web_site(find_url_list, '')
compare_url_tags()
