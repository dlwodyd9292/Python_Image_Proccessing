import os.path
from tkinter import  *
from tkinter import  messagebox
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
## 함수 선언부
## --- 공통 함수부 --- ##
def malloc2D(h, w) :
    memory = []
    for i in range(h):
        tmp = []
        for k in range(w):
            tmp.append(0)
        memory.append(tmp)
    return memory
def openImage() :
    global inImage, inH, inW, outImage,outH, outW, window, canvas, paper, filename
    filename = askopenfilename(parent=window,
                filetypes= (('로우 파일', '*.raw'),('모든 파일', '*.*')))
    fsize = os.path.getsize(filename) # 파일의 크기 byte
    ## (중요!)
    inH = inW = int(math.sqrt(fsize))
    inImage = malloc2D(inH, inW)
    ## 파일 --> 메모리
    rawFp = open(filename, 'rb')
    for i in range(inH):
        for k in range(inW):
            pixel = ord(rawFp.read(1))
            inImage[i][k] = pixel
    rawFp.close()
    equalImage()

def displayImage() :
    global inImage, inH, inW, outImage, outH, outW, window, canvas, paper, filename
    if canvas != None :
        canvas.destroy()
    window.geometry(str(outH)+'x'+str(outW))
    canvas = Canvas(window, height=outH, width=outW)
    canvas.pack()
    paper = PhotoImage(height=outH, width=outW)
    canvas.create_image((outH / 2, outW / 2), image=paper, state='normal')

    # for i in range(outH) :
    #     for k in range(outH) :
    #         color = outImage[i][k]
    #         paper.put("#%02x%02x%02x" % (color, color, color), (k, i))
    rgbString = ""
    for i in range(outH) :
        tmpString = ""
        for k in range(outH):
            p = outImage[i][k]
            tmpString += "#%02x%02x%02x " % (p, p, p)
        rgbString += '{' + tmpString + '} '
    paper.put(rgbString)

## -- 영상처리 함수부 -- ##
def equalImage() : # 동일 영상 알고리즘
    global inImage, inH, inW, outImage, outH, outW, window, canvas, paper, filename
    # (중요!) 출력 영상의 크기를 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    outImage = malloc2D(outH, outW)
    ## 진짜 영상처리 알고리즘 ##
    for i in range(inH) :
        for k in range(inW) :

            outImage[i][k] = inImage[i][k]
    ########################
    displayImage()

def addImage() : # 값 더하기 알고리즘
    global inImage, inH, inW, outImage, outH, outW, window, canvas, paper, filename
    # (중요!) 출력 영상의 크기를 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    outImage = malloc2D(outH, outW)
    ## 진짜 영상처리 알고리즘 ##
    addValue = askinteger('제목', '내용', minvalue=-255, maxvalue=255)
    for i in range(inH) :
        for k in range(inW) :
               v = inImage[i][k] + addValue
               if v > 255:
                  v = 255
               if v < 0:
                  v = 0
               outImage[i][k] = v
    ########################
    displayImage()

def negativeImage() : # 영상 반전 알고리즘
    global inImage, inH, inW, outImage, outH, outW, window, canvas, paper, filename
    # (중요!) 출력 영상의 크기를 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    outImage = malloc2D(outH, outW)
    ## 진짜 영상처리 알고리즘 ##
    for i in range(inH) :
        for k in range(inW) :

            outImage[i][k] = 255 - inImage[i][k]
    ########################
    displayImage()

def bwImage() : #입력받은 흑백 값 기준 알고리즘
    global inImage, inH, inW, outImage, outH, outW, window, canvas, paper, filename
    # (중요!) 출력 영상의 크기를 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    outImage = malloc2D(outH, outW)
    bwValue = askinteger('흑백반전', '값 입력', minvalue=-255, maxvalue=255)
    ## 진짜 영상처리 알고리즘 ##
    for i in range(inH) :
        for k in range(inW) :

            v = inImage[i][k]
            if (v < bwValue):
                v = 0
            else:
                v = 255
            outImage[i][k] = v
    ########################
    displayImage()

def upDownImage() : # 상하 반전 알고리즘
    global inImage, inH, inW, outImage, outH, outW, window, canvas, paper, filename
    # (중요!) 출력 영상의 크기를 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    outImage = malloc2D(outH, outW)
    ## 진짜 영상처리 알고리즘 ##
    rgbString = ""
    for i in range(outH):
        tmpString = ""
        for k in range(outH):
            outImage[i][k] = inImage[len(inImage) - 1 - i][k]
    ########################
    displayImage()

def leftRightImage() : # 좌우 반전 알고리즘
    global inImage, inH, inW, outImage, outH, outW, window, canvas, paper, filename
    # (중요!) 출력 영상의 크기를 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    outImage = malloc2D(outH, outW)
    ## 진짜 영상처리 알고리즘 ##
    rgbString = ""
    for i in range(outH):
        tmpString = ""
        for k in range(outH):
            outImage[i][k] = inImage[i][len(inImage) - 1 - k]
    ########################
    displayImage()
def zoomOutImage() : # 동일 영상 알고리즘
    global inImage, inH, inW, outImage, outH, outW, window, canvas, paper, filename
    # (중요!) 출력 영상의 크기를 결정 --> 알고리즘에 의존
    scale = askinteger('이미지 축소', '축소 값 입력(2,4,6,8)', minvalue= 2, maxvalue= 8)
    outH = inH // scale
    outW = inW // scale
    outImage = malloc2D(outH, outW)
    ## 진짜 영상처리 알고리즘 ##
    for i in range(inH) :
        for k in range(inW) :
            outImage[i//scale][k//scale] = inImage[i][k]
    ########################
    displayImage()

def zoomInNormalImage() : # 영상 확대 기본 알고리즘
    global inImage, inH, inW, outImage, outH, outW, window, canvas, paper, filename
    # (중요!) 출력 영상의 크기를 결정 --> 알고리즘에 의존
    scale = askinteger('이미지 확대', '확대 값 입력(2,4,6,8)', minvalue=2, maxvalue=8)
    outH = inH * scale
    outW = inW * scale
    outImage = malloc2D(outH, outW)
    ## 진짜 영상처리 알고리즘 ##
    for i in range(inH) :
        for k in range(inW) :
            outImage[i*scale][k*scale] = inImage[i][k]
    ########################
    displayImage()

def zoomInneighborImage() : # 영상 확대 기본 알고리즘
    global inImage, inH, inW, outImage, outH, outW, window, canvas, paper, filename
    # (중요!) 출력 영상의 크기를 결정 --> 알고리즘에 의존
    nescale = askinteger('이미지 확대', '확대 값 입력(2,4,6,8)', minvalue=2, maxvalue=8)
    outH = inH * nescale
    outW = inW * nescale

    tempImage = malloc2D(inH, inW)
    tempAry = malloc2D(outH, outW)

    outImage = malloc2D(outH, outW)

    ## 진짜 영상처리 알고리즘 ##
    for i in range(inH) :
        for k in range(inW) :
            tempImage[i][k] = inImage[i*inW + k]

    for i in range(outH) :
        for k in range(outW) :
            tempAry[i][k] = tempImage[i//nescale][k//nescale]

    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = tempAry[i][k]

    ########################
    displayImage()

def gammaImage() : # 감마 알고리즘
    global inImage, inH, inW, outImage, outH, outW, window, canvas, paper, filename
    # (중요!) 출력 영상의 크기를 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    outImage = malloc2D(outH, outW)
    ## 진짜 영상처리 알고리즘 ##
    for i in range(inH) :
        for k in range(inW) :

            outImage[i][k] = int(255 * ((inImage[i][k] / 255) ** 2.5))
    ########################
    displayImage()

def parabolaImage() : # 동일 영상 알고리즘
    global inImage, inH, inW, outImage, outH, outW, window, canvas, paper, filename
    # (중요!) 출력 영상의 크기를 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    outImage = malloc2D(outH, outW)
    ## 진짜 영상처리 알고리즘 ##
    for i in range(inH) :
        for k in range(inW) :

            outImage[i][k] = int(255*((inImage[i][k]/128 -1)**2))
    ########################
    displayImage()

def bwAvgImage() : # 흑백 영상 평균값 알고리즘
    global inImage, inH, inW, outImage, outH, outW, window, canvas, paper, filename
    # (중요!) 출력 영상의 크기를 결정 --> 알고리즘에 의존

    hap = 0
    for i in range(inH) :
        for k in range(inW) :
            hap += inImage[i][k]
    avg = hap / (inH*inW)

    outH = inH
    outW = inW
    outImage = malloc2D(outH, outW)
    ## 진짜 영상처리 알고리즘 ##
    for i in range(inH) :
        for k in range(inW) :
            v = inImage[i][k]
            if ( v > avg ) :
                v = 255
            if (v < avg):
                v = 0
            outImage[i][k] = v
    ########################
    displayImage()

def moveImage() : # 영상 이동 알고리즘
    global inImage, inH, inW, outImage, outH, outW, window, canvas, paper, filename
    # (중요!) 출력 영상의 크기를 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    outImage = malloc2D(outH, outW)
    mv = askinteger('이미지 이동', '이동 값 입력(-255 ~ 255)', minvalue= -255, maxvalue= 255)
    ## 진짜 영상처리 알고리즘 ##
    for i in range(inH - 1, -1, -1):
        for k in range(inW - 1, -1, -1):
            if (i + mv) > 255 or (k + mv) > 255:
                pass
            else:
                outImage[i+mv][k+mv] = inImage[i][k]
    ########################
    displayImage()
## 전역 변수부
inImage, inH, inW  = None, 0, 0
outImage,outH, outW  = None, 0, 0
window, canvas, paper = None, None, None
filename = ""

## 메인 코드부
window = Tk()
window.title("영상처리 Ver 0.3")
window.geometry('500x300')

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label='파일', menu=fileMenu)
fileMenu.add_command(label="열기", command=openImage)
fileMenu.add_command(label="저장", command=None)
fileMenu.add_separator()
fileMenu.add_command(label="종료", command=None)

imageMenu = Menu(mainMenu)
mainMenu.add_cascade(label='화소점처리', menu=imageMenu)
imageMenu.add_command(label="밝게/어둡게", command=addImage)
imageMenu.add_command(label="반전", command=negativeImage)
imageMenu.add_command(label="흑백(입력)", command=bwImage)
imageMenu.add_command(label="흑백(평균)", command=bwAvgImage)
imageMenu.add_command(label="감마", command=gammaImage)
imageMenu.add_command(label="프라볼라", command=parabolaImage)

image2Menu = Menu(mainMenu)
mainMenu.add_cascade(label='기하학처리', menu=image2Menu)
image2Menu.add_command(label="미러링(상하)", command=upDownImage)
image2Menu.add_command(label="미러링(좌우)", command=leftRightImage)
image2Menu.add_command(label="축소", command=zoomOutImage)
image2Menu.add_command(label="이동", command=moveImage)
image2Menu.add_command(label="확대(기본)", command=zoomInNormalImage)

window.mainloop()
