## 정지영상을 위한 컴퓨터 비전 (딥러닝) ##
import cv2
import  numpy as np

## 함수 선언부
def ssdNet(image) :
    CONF_VALUE = 0.5
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
            if idx != 15 :
                ## 경고 메세지 발생 ##
                continue
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            cv2.rectangle(image, (startX, startY), (endX, endY),
                          COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
    return image

## 전역 변수부
filename = "C:/images/images(DL)/example_01.jpg"
cvImage = cv2.imread(filename)

## 메인 코드부
# 이미지에서 다양한 사물을 골라서 표시하기
# --> MobileNetSSD (사물 인식용 Pre_Trained 모델
## 딥러닝 기반의 컴퓨터 비전 ##
resultImage = ssdNet(cvImage)

cv2.imshow('Result', resultImage)
cv2.waitKey(0)
cv2.destroyAllWindows()