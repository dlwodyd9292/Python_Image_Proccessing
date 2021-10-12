## 기 학습된 모델(Pre-Trained Model)을 불러와서 예측하기
import joblib
clf = joblib.load('iris_150_KNN3_96.dmp')

# 산을 산책하다가 우연히 꽃을 하나 발견
myData = [4.8, 3.3, 1.3, 0.2]
result = clf.predict( [myData] )
print('(인공지능 왈) 이 꽃은 %s 입니다.' % (result[0]))