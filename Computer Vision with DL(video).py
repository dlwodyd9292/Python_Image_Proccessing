## 동영상을 위한 컴퓨터 비전 (딥러닝) ##
import cv2
import  numpy as np

## 함수 선언부
def ssdNet(image) :
    CONF_VALUE = 0.5 # 사물을 50% 이상 인식하면 표시
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
    net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > CONF_VALUE:
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100) # 비행기 67.5%
            #label = "{}".format(CLASSES[idx]) # 비행기
            cv2.rectangle(image, (startX, startY), (endX, endY),
                          COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
    return image

import random
def snapshot(image) :
    cv2.imwrite('c:/temp/save' + str(random.randint(11111,99999)) + '.png', image)


## 전역 변수부
filename = "C:/images/traffic.mp4"
#movie = cv2.VideoCapture(0) # 카메라 연결
movie = cv2.VideoCapture(filename) # 영상파일

s_factor = 0.5 # 화면 크기 비율, 조절 가능
imageCount = 0 # 프레임을 꼐속 카운트
hop = 5 # 프레임(=이미지)를 건너 뛰는 폭

## 메인 코드부

while True :
    ret, image = movie.read() # 한 장면 읽기, 성공하면 ret가 True, image는 한 장면
    if not ret :
        break;

    ## 동영상 딥러닝 기반의 컴퓨터 비전 ##
    imageCount += 1 # 일반적으로 1초에 30씩 증가
    if imageCount % hop == 0 : #건너뛰다가 hop마다 처리하기
        cvImage = cv2.resize(image, None, fx=s_factor, fy=s_factor, interpolation=cv2.INTER_AREA)
        resultImage = ssdNet(cvImage)
        cv2.imshow('Vedeo', resultImage)
    ###################################
    key = cv2.waitKey(20)
    if key == 27 : # Esc 키
        break
    if key == ord('c') or key == ord('C') :
        snapshot(image)

movie.release()
cv2.destroyAllWindows()
