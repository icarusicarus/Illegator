from bs4 import BeautifulSoup  as bs
import requests

gamble_keywords  = ['충전', '환전', '카지노', '이벤트', '출금', '신규가입','충환전','입금계좌', '게임머니', '베팅', '보장', '안전놀이터', '토토' ]
number_match     = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
hit_list = {}
url_list = ['http://betmoa03.com/','https://www.safenori.com/','https://mt-man.com/','https://www.dajaba.org/','https://pandora-club.com/','http://dii-129.com/',
            'http://7575yy.com/','http://raropiti.com/','http://covadao.com/']
hit_score = []
hit_lists = []

def sortBySum(e):
    return e[1][1]

for url in url_list:
    webpage = requests.get(url)
    soup = bs(webpage.content, "html.parser")
    text = soup.text

    score = 0
    for keyword in gamble_keywords:
        keyword_count = text.count(keyword)
        if (keyword_count > 0):
            hit_list.update({keyword : keyword_count})
            score += keyword_count
    hit_score.append(score)

    hit_lists.append(hit_list)
    hit_list = {}

result = list(zip(url_list,zip(hit_lists,hit_score)))
result.sort(reverse=True, key=sortBySum)
for r in result:
    print("총계: "+str(r[1][1])+'\t',r[0], r[1][0])
