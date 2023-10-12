import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split        # pip install scikit-learn
from sklearn.preprocessing import LabelEncoder              # 범주형 변수를 숫자 형식으로 변환
from konlpy.tag import Okt                                  # 한국어 형태소 분석
from tensorflow.keras.preprocessing.text import Tokenizer   # 자연어 처리에서 입력 문장을 일정한 단위로 분할
from tensorflow.keras.preprocessing.sequence import pad_sequences
# 시퀀스 데이터의 길이를 조정하여 동일한 길이를 가지도록 패딩(padding)을 추가하는 기능을 제공
from tensorflow.keras.utils.import to_categorical           # 정수형(integer) 레이블을 원-핫 인코딩(one-hot encoding) 벡터로 변환
import pickle           # 파이썬에서 사용하는 dic, list, class과 같은 자료형을 변환 없이 그대로 파일로 저장하고 이를 불러올 때 사용