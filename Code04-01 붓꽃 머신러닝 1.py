## [붓꽃 구별하기] 머신러닝 프로젝트 ##
from sklearn.neighbors import KNeighborsClassifier # KNN 알고리즘
from sklearn import metrics,utils # 편리한 함수
import pandas as pd # 판다스 : CSV 파일을 편리하게 사용
import numpy as np # 필수

## 0. 데이터 준비 (iris.csv)
df = pd.read_csv('iris.csv') # 엑셀의 데이터 시트처럼 읽어들이기
df = utils.shuffle(df) # 데이터 섞기(*필수*)

# 0-1. 학습(train)용 80%, 테스트용 20% 분리
dataLen = df.shape[0] # 행 개수(= 데이터 갯수)
trainSize = int(dataLen * 0.8) # 학습용 데이터 개수 (120건) # 80%
testSize = dataLen - trainSize # 테스트용 데이터 개수( 전체 - 학습용) # 20%

# 0-2. 문제(data)와 답(label)을 분리
train_data = df.iloc[ 0:trainSize, 0: -1] # 마지막 열을 제외하고.....80% 행
train_label = df.iloc[ 0:trainSize, [-1]] # 마지막 열만... 20% 행
test_data = df.iloc[ trainSize:, 0: -1] # 마지막 열을 제외하고.....80% 행
test_label = df.iloc[ trainSize:, [-1]] # 마지막 열만... 20% 행

## 1. 학습 방법을 결정 (머신러닝 알고리즘 선택) : KNN, SVN, DeepLearning ....
clf = KNeighborsClassifier(n_neighbors=3) # 모델 == 인공지능 == (알파고)

## 2. 학습 하기 (훈련 하기) --> 오랫 동안 CPU가 작업함 --> 결과 : 모델(Model) : 인공지능 ( ** 무지 오래 걸릴 수 있음 **)
clf.fit(train_data, train_label) # 실제 공부하기....

## 3. 모델의 정답을 구하기 (몇 점짜리 인공지능인지)
result = clf.predict(test_data) # 모의고사 문제(test_data) 풀어서 답안(result) 제출
score = metrics.accuracy_score(result, test_label) # 채점하기 (0.0 ~ 1.0)
print('정답률 --> %5.2f %%' % (score*100))

## (4. 정답을 모로는 데이터를 '예측' 하기)
## 산을 산책하다가 우연히 꽃을 하나 발견
myData = [4.8, 3.3, 1.3, 0.2]
result = clf.predict( [myData] )
print('(인공지능 왈) 이 꽃은 %s 입니다. 단, %5.2f %% 보장함' % (result[0], score*100))