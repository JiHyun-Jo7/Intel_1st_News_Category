from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100#&date=%2000:00:00&page=1'
options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
options.add_argument('user-agent=' + user_agent)
options.add_argument('lang=ko_KR')          # 언어 설정
# options.add_argument('headless')
# # 리눅스 환경에서 사용
# driver = webdriver.Chrome('./chromedriver', options=options)
# options.add_argument('window-size=1980x1080')
# options.add_argument('disable-gpu')
# options.add_argument('--no-sandbox')


# 크롬 드라이버 최신 버전 설정
service = ChromeService(executble_path=ChromeDriverManager().install())
# 크롬 드라이버
driver = webdriver.Chrome(service=service, options=options)

# //*[@id="section_body"]/ul[1]/li[1]/dl/dt[2]/a  : X path 복사
# //*[@id="section_body"]/ul[1]/li[2]/dl/dt[2]/a : 2번째 기사
# //*[@id="section_body"]/ul[2]/li[1]/dl/dt[2]/a : 6번째 기사
# //*[@id="section_body"]/ul[4]/li[5]/dl/dt[2]/a : 20번째 기사
# //*[@id="section_body"]/ul[1]/li[1]/dl/dt[2]/a : 2페이지 1번째 기사
# 다중 for문을 사용하여 전체 기사 제목 출력

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
# pages = [146, 328, 461, 75, 117, 72]  # 각 카테고리 별 총 페이지 수
pages = [110, 110, 110, 75, 110, 72]    # 학습을 위해 최대 페이지를 중간 지점인 110 페이지로 제한함
df_titles = pd.DataFrame()

for i in range(6):
    # 카테고리 변경
    section_url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i)
    titles = []                 # titles 초기화
    for j in range(1, 3):       # pages[i]+1 (시간 문제 상 3으로 축소)
        url = section_url + '#&date=%2000:00:00&page={}'.format(j)        # 페이지 변경
        driver.get(url)
        time.sleep(0.5)           # 페이지가 바뀔 수 있도록 대기 시간을 줌 (1초 미만 권장)
        for k in range(1, 5):
            for m in range(1, 6):
                try:
                    title = driver.find_element('xpath', '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(k, m)).text
                    title = re.compile('[^가-힣]').sub(' ', title)
                    titles.append(title)
                except:
                    print('error {} {} {} {}'.format(i, j, k, m))
        if j % 10 == 0:
            df_section_title = pd.DataFrame(titles,columns=['titles'])
            df_section_title['category']=category[i]
            df_titles = pd.concat([df_titles, df_section_title], ignore_index=True)
            df_titles.to_csv('./crawling_data/naver_news_{}_{}.csv'.format(i, j), index=False)
            titles = []
    df_section_title = pd.DataFrame(titles, columns=['titles'])
    df_section_title['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_title], ignore_index=True)
    df_titles.to_csv('./crawling_data/crawling_data_last.csv', index=False)

print(df_titles.head(20))       # 상위 제목 20개 출력
df_titles.info()
print(df_titles['category'].value_counts())