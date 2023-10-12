import pandas as pd
import numpy as np
import pickle           # 파이썬에서 사용하는 dic, list, class과 같은 자료형을 변환 없이 그대로 파일로 저장하고 이를 불러올 때 사용
from sklearn.model_selection import train_test_split        # pip install scikit-learn
from sklearn.preprocessing import LabelEncoder              # 범주형 변수를 숫자 형식으로 변환
from konlpy.tag import Okt                                  # 한국어 형태소 분석
# tensorflow ver 2.7.0 downgrade
from tensorflow.keras.utils import to_categorical           # 정수형(integer) 레이블을 원-핫 인코딩(one-hot encoding) 벡터로 변환
from tensorflow.keras.preprocessing.text import Tokenizer   # 자연어 처리에서 입력 문장을 일정한 단위로 분할
from tensorflow.keras.preprocessing.sequence import pad_sequences
# 시퀀스 데이터의 길이를 조정하여 동일한 길이를 가지도록 패딩(padding)을 추가하는 기능을 제공


# pd.set_option('display.unicode.east_asian_width', True)             # 제목 열을 맞추기 위한 코드
df = pd.read_csv('./crawling_data/naver_news_titles_20231012.csv')
print(df.head())
df.info()

X = df['titles']
Y = df['category']

# encoder = LabelEncoder()                        # LabelEncoder 함수를 변수에 할당시킴
# labeled_y = encoder.fit_transform(Y)
# print(labeled_y[:3])                            # 카테고리 넘버 출력 (초반 3개)
# label = encoder.classes_
# print(label)                                    # 카테고리 출력
#
# onehot_y = to_categorical(labeled_y)
# print(onehot_y)                                 # 카테고리 onehot-encoding

okt = Okt()

okt_morph_x = okt.morphs(X[0])
print(okt_morph_x)