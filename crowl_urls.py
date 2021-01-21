
from bs4 import BeautifulSoup  as bs    #BeautifulSoup 을 bs로 명명하여 사용.
import requests




open_tags = []  #2차원
open_tags_num = []
cmp_url = []    #2차원

def crol_web_site():
        url_list = ['']      
            #3,4번같은것으로 의심됨.
        index = 0

        for url in url_list:

                webpage = requests.get(url)
                soup = bs(webpage.content, "html.parser")
                all_tags = [tag.name for tag in soup.find_all()]

                open_tags.append(all_tags[:int(len(all_tags)/2)])
                open_tags_num.append(int(len(all_tags)))

                index = index+1

        print(index)

        print(open_tags_num)



def extractMarkedText(target_text, compare_text):
    
    #: 입력된 두개의 인자를 가지고 테이블을 만들기
    width = len(target_text) + 1
    height = len(compare_text) + 1

    # 테이블 초기화 빈값으로 초기화시키기
    table = [''] * width * height

    def getTable(r, c):
        return table[r * width + c]

    def setTable(r, c, value):
        table[r * width + c] = value

    for i in range(1, height):
        for j in range(1, width):
                if target_text[ j - 1] == compare_text[ i - 1]:
                        value = getTable( i - 1, j - 1) + target_text[j - 1]
                        setTable(i, j, value)
                        continue

                searched_span_lcs = getTable(i - 1, j)
                text_lcs = getTable(i, j - 1)

                if len(searched_span_lcs) > len(text_lcs):
                        setTable(i, j, searched_span_lcs)

                else:
                        setTable(i, j, text_lcs)
    return getTable(height - 1, width - 1)

# 출처: https://sssunho.tistory.com/23 [개발자 Sunho Lee]


def compare_url_tags():
        url_sz = len(open_tags)
        i = 0
        for ith_open_tags  in open_tags:   #기준 url
                tmp_cmp = []

                tmp_ith_length = ",".join(open_tags[i])

                ith_sz = len(tmp_ith_length)

                print("and")
                for j in range(0,url_sz): #정확도 비교할 url
                        tmp_jth_length = ",".join(open_tags[j])
                        jth_sz = len(tmp_jth_length)
                        result = extractMarkedText(open_tags[i],open_tags[j])

                        if ith_sz > jth_sz :

                                tmp_res_leng = (len(result) /  ith_sz) 
                                tmp_cmp.append(round(tmp_res_leng , 5) )
                        else:

                                tmp_res_leng = (len(result) /  jth_sz) 
                                tmp_cmp.append(round(tmp_res_leng , 5) )

                i = i+1
                cmp_url.append(tmp_cmp)
        for x in cmp_url:
                print(x)
                # 0.7 이상은 자기 자신 or 같은 구조(같은 T로 추정됨).
                # 0.5~0.7 은 유사 구조.(그러나 다른 T)
                # 0.5 이하는 다른 구조.


crol_web_site()
compare_url_tags()



