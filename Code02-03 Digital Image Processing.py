import math


## 함수 선언부
## 공통 함수부 ##
def malloc2D(h, w):
    memory = []
    for i in range(h):
        tmp = []
        for k in range(w):
            tmp.append(0)
        memory.append(tmp)
    return memory


def loadImage(fName):
    global image, height, width, fileName
    rawFp = open(fName, 'rb')
    # 파일의 크기를 알아냄.
    fsize = 262144
    height = width = int(math.sqrt(fsize))
    # 메모리 할당(빈 배열 준비)
    image = malloc2D(height, width)
    # 파일 --> 배열
    for i in range(height):
        for k in range(width):
            pixel = ord(rawFp.read(1))
            image[i][k] = pixel
    rawFp.close()


def displayImage():
    global image, height, width, fileName
    print('---------------------')
    for i in range(5):
        for k in range(5):
            print("%3d" % image[i + 250][k + 250], end=' ')
        print()
    print('---------------------')


### 영상처리 함수부 ###
def addImage():
    global image, height, width, fileName
    value = int(input('더할 값 -->'))

    for i in range(height):
        for k in range(width):
            v = image[i][k] + value
            if (v > 255):
                v = 255
            if (v < 0):
                v = 0
            image[i][k] = v

    displayImage()


def bwImage():
    global image, height, width, fileName
    value = int(input('기준 값 -->'))

    for i in range(height):
        for k in range(width):
            v = image[i][k]
            if (v < value):
                v = 0
            else:
                v = 255
            image[i][k] = v

    displayImage()


def bwAvgImage():
    global image, height, width, fileName
    hap = 0
    for i in range(height):
        for k in range(width):
            hap += image[i][k]
    value = hap / (height * width)
    print('평균값-->', value)

    for i in range(height):
        for k in range(width):
            v = image[i][k]
            if (v < value):
                v = 0
            else:
                v = 255
            image[i][k] = v

    displayImage()


## 전역 변수부
image = []
height, width = 512, 512
fileName = "C:/images/Etc_Raw(squre)/flower512.raw"

## 메인 코드부
# 파일을 열기, 메모리에 로딩
loadImage(fileName)
displayImage()

# 밝게하기 / 어둡게
addImage()

# 흑백
bwImage()

# 흑백(평균값)
bwAvgImage()

# 흑백 (중앙값==중위수)
#bwCenImage() --> 과제