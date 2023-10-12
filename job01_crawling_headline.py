from bs4 import BeautifulSoup           # HTML과 XML 문서들의 구문을 분석
import requests                         # HTTP 요청을 만들기 위한 라이브러리
import re                               # 정규식 지원을 제공. 정규식 패턴과 문자열을 사용하여 문자열 내에서 해당 패턴을 검색
import pandas as pd
import datetime

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'Science']
url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100'

df_titles = pd.DataFrame()          # 빈 데이터 프레임 생성
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}
# resp = requests.get(url, headers=headers)
# # 인터넷 페이지에 내용을 달라고 요청 requests 만 전송시 반응X header 정보를 같이 전송함
# # headers -> 인터넷 페이지 -> F12 -> Network -> headers
# # print(list(resp))
# print(type(resp))
# soup = BeautifulSoup(resp.text, 'html.parser')
# # print(soup)
# title_tags = soup.select('.sh_text_headline')       # 클래스의 요소를 불러오기 위해 .을 찍음
# print(title_tags)
# print(type(title_tags[0]))
#
# titles=[]
# for title_tag in title_tags:
#     titles.append(re.compile('[^가-힣|a-z|A-Z]').sub(' ',title_tag.text))
#     # ^ : 처음부터, 그 외의 것(한글영어 제외)은 공백으로 표시 (.sub~)
#     # 특수문자, 한자는 아스키 코드로 구현 가능
# print(titles)
# print(len(titles))

re_title = re.compile('[^가-힣|a-z|A-Z]')

for i in range(6):
    resp = requests.get('https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i), headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    title_tags = soup.select('.sh_text_headline')
    titles = []
    for title_tag in title_tags:
        titles.append(re.compile('[^가-힣|a-z|A-Z]').sub(' ',title_tag.text))
    # i 번째 카테고리의 헤드라인을 가져옴
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    # i 번째 카테고리의 묶음을 만듦
    df_section_titles['category'] = category[i]
    if category[i] == 'IT':         # IT 카테고리의 이름을 Science로 변경
        df = df.rename(columns={'IT': 'Science'})
    # 카테고리, 헤드라인이 전부 들어있는 묶음을 만듦
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows')

print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())         # 각 카테고리에 있는 헤드라인의 수를 셈
df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)