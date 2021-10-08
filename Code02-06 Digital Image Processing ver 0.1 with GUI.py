import math
from tkinter import *
from tkinter import messagebox
## 함수 선언부
## 공통 함수부 ##
def malloc2D(h, w) :
    memory = []
    for i in range(h):
        tmp = []
        for k in range(w):
            tmp.append(0)
        memory.append(tmp)
    return memory

def loadImage(fName) :
    global image, height, width, fileName
    rawFp = open(fName, 'rb')
    # 파일의 크기를 알아냄.
    fsize = 65536
    #fsize = 262144
    height = width = int(math.sqrt(fsize))
    # 메모리 할당(빈 배열 준비)
    image = malloc2D(height, width)
    # 파일 --> 배열
    for i in range(height):
        for k in range(width):
            pixel = ord(rawFp.read(1))
            image[i][k] = pixel
    rawFp.close()

def displayImage() :
    global image, height, width, fileName
    for i in range(height) :
        for k in range(width) :
            color = image[i][k] # 원본
            # color = image[i][k] + 100 # 밝게
            # color = image[i][k] - 100 # 어둡게
            # color = 255 - image[i][k] # 반전

            # if color > 255 : #밝게, 어둡게
            #     color = 255
            # if color < 0 :
            #     color = 0

            # if color > 127 : # 흑백
            #     color = 255
            # if color <= 127 :
            #     color = 0
            # color = image[len(image) - 1 - i][k] # 상하 반전
            #color = image[i][len(image) - 1 - k]  # 좌우 반전

            paper.put("#%02x%02x%02x" % (color, color, color), (k, i))

### 영상처리 함수부 ###
def addImage() :
    global image, height, width, fileName
    value = int(input('더할 값 -->'))

    for i in range(height) :
        for k in range(width) :
            v = image[i][k] + value
            if ( v > 255) :
                v = 255
            if ( v < 0) :
                v = 0
            image[i][k] = v

    displayImage()

def bwImage() :
    global image, height, width, fileName
    value = int(input('기준 값 -->'))

    for i in range(height) :
        for k in range(width) :
            v = image[i][k]
            if ( v < value ) :
                v = 0
            else :
                v = 255
            image[i][k] = v

    displayImage()

def bwAvgImage() :
    global image, height, width, fileName
    hap = 0
    for i in range(height) :
        for k in range(width) :
            hap += image[i][k]
    value = hap / (height*width)
    print('평균값-->', value)

    for i in range(height) :
        for k in range(width) :
            v = image[i][k]
            if ( v < value ) :
                v = 0
            else :
                v = 255
            image[i][k] = v

    displayImage()
## 전역 변수부
image = []
height, width = 256, 256
#height, width = 512, 512
fileName = "C:/images/Etc_Raw(squre)/LENA256.RAW"
#fileName = "C:/images/Etc_Raw(squre)/LENNA512.raw"


## 메인 코드부
window = Tk()
window.title("영상처리(Ver 0.1)")
window.geometry('256x256')
#window.geometry('512x512')
window.resizable(width=False, height=False)

canvas = Canvas(window, height=256/2, width=256/2) # 256 X 256 기준 128 X 128로 만들 땐 /2를 해줌
#canvas = Canvas(window, height=512, width=512) # 256 X 256 기준 128 X 128로 만들 땐 /2를 해줌
canvas.pack()

paper = PhotoImage(height=256, width=256)
#paper = PhotoImage(height=512, width=512)
canvas.create_image((256/16, 256/16), image=paper, state='normal')
# # 256 X 256 기준 1/2로 축소할 땐 /16를 해줌
# 256 X 256 기준 2로 확대할 땐 *16를 해줌
#canvas.create_image( (512/2, 512/2), image=paper, state='normal')


# 파일을 열기, 메모리에 로딩
loadImage(fileName)
displayImage()

# 밝게하기 / 어둡게
# addImage()

# 흑백
# bwImage()

# 흑백(평균값)
# bwAvgImage()

# 흑백 (중앙값==중위수)
# bwCenImage() --> 과제


window.mainloop()