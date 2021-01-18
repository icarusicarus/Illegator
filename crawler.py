from bs4 import BeautifulSoup  as bs
import requests


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


if __name__ == "__main__":
    gamble_keywords = ['충전', '환전', '카지노', '이벤트', '출금', '신규가입', '충환전', '입금계좌', '게임머니', '베팅', '보장', '안전놀이터', '토토']
    url_list = ['http://betmoa03.com/', 'https://www.safenori.com/', 'https://mt-man.com/', 'https://www.dajaba.org/',
                'https://pandora-club.com/', 'http://dii-129.com/',
                'http://7575yy.com/', 'http://raropiti.com/', 'http://covadao.com/']

    hit_lists = []
    hit_score = []

    for url in url_list:
        webpage = requests.get(url)
        soup = bs(webpage.content, "html.parser")
        text = soup.text
        list_total_score = get_hit_list(gamble_keywords, text)
        hit_lists.append(list_total_score[0])
        hit_score.append(list_total_score[1])

    result = list(zip(url_list, zip(hit_lists, hit_score)))
    result.sort(reverse=True, key=sort_by_sum)

    for r in result:
        print("총계: " + str(r[1][1]) + '\t', r[0], r[1][0])

