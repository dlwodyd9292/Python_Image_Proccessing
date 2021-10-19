import os.path
from tkinter import  *
from tkinter import  messagebox
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import cv2

## 함수 선언부
## --- 공통 함수부 --- ##
import numpy as np


def malloc2D(h, w) :
    memory = []
    for i in range(h):
        tmp = []
        for k in range(w):
            tmp.append(0)
        memory.append(tmp)
    return memory

def openImage() :
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage
    filename = askopenfilename(parent=window,
                filetypes= (('이미지 파일', '*.jpg;*.jpeg;*.png;*.bmp;*.tif;*.tiff'),('모든 파일', '*.*')))
    ## 파일 --> OpenCV 개체
    inCvImage = cv2.imread(filename)
    ## (중요!) 입력 이미지의 폭, 높이 알아내기
    inH = inCvImage.shape[0]
    inW = inCvImage.shape[1]
    ## 메모리 할당
    inImageR = malloc2D(inH, inW)
    inImageG = malloc2D(inH, inW)
    inImageB = malloc2D(inH, inW)
    ## OpenCV --> 메모리
    for i in range(inH):
        for k in range(inW):
            inImageR[i][k] = inCvImage.item(i, k, 2)
            inImageG[i][k] = inCvImage.item(i, k, 1)
            inImageB[i][k] = inCvImage.item(i, k, 0)

    equalImage()

def saveImage() :
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage
    # 빈 OpenCV 개체 준비
    saveCvImage = np.zeros((outH, outW, 3), np.uint8)  # 3차원 배열. 모두 0으로 채움 (OpenCV 개체)
    # 출력 이미지 --> 넘파이 배열(OpenCV 개체)
    for i in range(outH) :
        for k in range(outW) :
            # 파이썬의 튜플  (( [37, 240, 55] ))
            saveCvImage[i,k] = tuple( ( [outImageB[i][k],outImageG[i][k], outImageR[i][k] ]  ))

    savename = asksaveasfile(parent=window, mode='wb', defaultextension='.',
            filetypes=(('이미지 파일', '*.jpg;*.jpeg;*.png;*.bmp;*.tif;*.tiff'), ('모든 파일', '*.*')))
    cv2.imwrite(savename.name, saveCvImage)
    messagebox.showinfo("저장 성공",savename.name+'가 저장됨' )

def displayImage() :
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage
    if canvas != None :
        canvas.destroy()
    window.geometry(str(outW)+'x'+str(outH))
    canvas = Canvas(window, height=outH, width=outW)
    canvas.pack()
    paper = PhotoImage(height=outH, width=outW)
    canvas.create_image((outW / 2, outH / 2), image=paper, state='normal')

    rgbString = "" # 메모리로 임시로 그리는 공간
    for i in range(outH) :
        tmpString = ""  # 한줄짜리
        for k in range(outW) :
            r = outImageR[i][k]
            g = outImageG[i][k]
            b = outImageB[i][k]
            tmpString += "#%02x%02x%02x  " % (r, g, b)
        rgbString += '{' + tmpString + '}  '
    paper.put(rgbString)

## -- 영상처리 함수부 -- ##
def equalImage() : # 동일 영상 알고리즘
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB
    global outH, outW, window, canvas, paper, filename, inCVImage, outCVImage
    # (중요!) 출력 영상의 크기를 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    outImageR = malloc2D(outH, outW)
    outImageG = malloc2D(outH, outW)
    outImageB = malloc2D(outH, outW)
    ## 진짜 영상처리 알고리즘 ##
    for i in range(inH) :
        for k in range(inW) :
            outImageR[i][k] = inImageR[i][k]
            outImageG[i][k] = inImageG[i][k]
            outImageB[i][k] = inImageB[i][k]
    ########################
    displayImage()

def grayScaleImage() : # 그레이스케일 알고리즘
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB
    global outH, outW, window, canvas, paper, filename, inCVImage, outCVImage
    # (중요!) 출력 영상의 크기를 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    outImageR = malloc2D(outH, outW)
    outImageG = malloc2D(outH, outW)
    outImageB = malloc2D(outH, outW)

    R,G,B = 0,0,0
    ## 진짜 영상처리 알고리즘 ##
    for i in range(inH) :
        for k in range(inW) :
            R = inImageR[i][k]
            G = inImageG[i][k]
            B = inImageB[i][k]

            Gray = int((R + G + B) / 3)

            outImageR[i][k] = Gray
            outImageG[i][k] = Gray
            outImageB[i][k] = Gray
    ########################
    displayImage()

def addMinusImage() : # 값 더하기 빼기 알고리즘
    global inImage, inH, inW, outImage, outH, outW, window, canvas, paper, filename
    # (중요!) 출력 영상의 크기를 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    outImage = malloc2D(outH, outW)
    ## 진짜 영상처리 알고리즘 ##
    addValue = askinteger('제목', '내용', minvalue=-255, maxvalue=255)
    for i in range(inH) :
        for k in range(inW) :
               R = inImageR[i][k] + addValue
               G = inImageG[i][k] + addValue
               B = inImageB[i][k] + addValue
               if R > 255:
                  R = 255
               if R < 0:
                  R = 0
               if G > 255:
                   G = 255
               if G < 0:
                   G = 0
               if B > 255:
                   B = 255
               if B < 0:
                   B = 0
               outImageR[i][k] = R
               outImageG[i][k] = G
               outImageB[i][k] = B
    ########################
    displayImage()

def negativeImage() : # 영상 반전 알고리즘
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB
    global outH, outW, window, canvas, paper, filename, inCVImage, outCVImage
    # (중요!) 출력 영상의 크기를 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    outImageR = malloc2D(outH, outW)
    outImageG = malloc2D(outH, outW)
    outImageB = malloc2D(outH, outW)
    ## 진짜 영상처리 알고리즘 ##
    for i in range(inH) :
        for k in range(inW) :

            outImageR[i][k] = 255 - inImageR[i][k]
            outImageG[i][k] = 255 - inImageG[i][k]
            outImageB[i][k] = 255 - inImageB[i][k]

    ########################
    displayImage()

def bwImage() : #입력받은 흑백 값 기준 알고리즘
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB
    global outH, outW, window, canvas, paper, filename, inCVImage, outCVImage
    # (중요!) 출력 영상의 크기를 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    outImageR = malloc2D(outH, outW)
    outImageG = malloc2D(outH, outW)
    outImageB = malloc2D(outH, outW)

    bwValue = askinteger('흑백반전', '값 입력', minvalue=-255, maxvalue=255)
    ## 진짜 영상처리 알고리즘 ##
    for i in range(inH) :
        for k in range(inW) :

            R = inImageR[i][k]
            G = inImageR[i][k]
            B = inImageR[i][k]

            if (R < bwValue):
                R = 0
            else:
                R = 255

            if (G < bwValue):
                G = 0
            else:
                G = 255

            if (B < bwValue):
                B = 0
            else:
                B = 255
            outImageR[i][k] = R
            outImageG[i][k] = G
            outImageB[i][k] = B
    ########################
    displayImage()

def bwAvgImage():     # 흑백 처리(평균값) 알고리즘
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage

    outH = inH
    outW = inW

    outImageR = malloc2D(outH, outW)
    outImageG = malloc2D(outH, outW)
    outImageB = malloc2D(outH, outW)

    hapR = 0
    hapG = 0
    hapB = 0
    for i in range(outH):
        for k in range(outW):
            hapR += inImageR[i][k]
            hapG += inImageG[i][k]
            hapB += inImageB[i][k]
    hap = hapR + hapB + hapG
    avg = int(hap / (outW*outH*3))

    for i in range(outH):
        for k in range(outW):
            if (inImageR[i][k] + inImageG[i][k] + inImageB[i][k])/3 > avg:
                outImageR[i][k] = 255
                outImageG[i][k] = 255
                outImageB[i][k] = 255
            else:
                outImageR[i][k] = 0
                outImageG[i][k] = 0
                outImageB[i][k] = 0

    displayImage()

def gammaImage() : # 감마 알고리즘
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB
    global outH, outW, window, canvas, paper, filename, inCVImage, outCVImage
    # (중요!) 출력 영상의 크기를 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW

    outImageR = malloc2D(outH, outW)
    outImageG = malloc2D(outH, outW)
    outImageB = malloc2D(outH, outW)

    ## 진짜 영상처리 알고리즘 ##
    for i in range(inH) :
        for k in range(inW) :
            outImageR[i][k] = int(255 * ((inImageR[i][k] / 255) ** 2.5))
            outImageG[i][k] = int(255 * ((inImageG[i][k] / 255) ** 2.5))
            outImageB[i][k] = int(255 * ((inImageB[i][k] / 255) ** 2.5))
    ########################
    displayImage()

def parabolaImage() : # 파라볼라 영상 알고리즘
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB
    global outH, outW, window, canvas, paper, filename, inCVImage, outCVImage
    # (중요!) 출력 영상의 크기를 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW

    outImageR = malloc2D(outH, outW)
    outImageG = malloc2D(outH, outW)
    outImageB = malloc2D(outH, outW)
    ## 진짜 영상처리 알고리즘 ##
    for i in range(inH) :
        for k in range(inW) :
            outImageR[i][k] = int(255 * ((inImageR[i][k] / 128 - 1) ** 2))
            outImageG[i][k] = int(255 * ((inImageG[i][k] / 128 - 1) ** 2))
            outImageB[i][k] = int(255 * ((inImageB[i][k] / 128 - 1) ** 2))
    ########################
    displayImage()

def upDownImage() : # 상하 반전 알고리즘
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB
    global outH, outW, window, canvas, paper, filename, inCVImage, outCVImage
    # (중요!) 출력 영상의 크기를 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    outImageR = malloc2D(outH, outW)
    outImageG = malloc2D(outH, outW)
    outImageB = malloc2D(outH, outW)
    ## 진짜 영상처리 알고리즘 ##
    rgbString = ""
    for i in range(outH):
        tmpString = ""
        for k in range(outW):
            outImageR[i][k] = inImageR[len(inImageR) - 1 - i][k]
            outImageG[i][k] = inImageG[len(inImageG) - 1 - i][k]
            outImageB[i][k] = inImageB[len(inImageB) - 1 - i][k]
    ########################
    displayImage()

def leftRightImage() : # 좌우 반전 알고리즘
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage
    ### 중요! ###
    outH = inH
    outW = inW

    outImageR = malloc2D(outH, outW)
    outImageG = malloc2D(outH, outW)
    outImageB = malloc2D(outH, outW)

    for i in range(outH):
        for k in range(outW):
            outImageR[i][k] = inImageR[i][(outW-1) - k]
            outImageB[i][k] = inImageB[i][(outW - 1) - k]
            outImageG[i][k] = inImageG[i][(outW - 1) - k]

    displayImage()

def moveImage():    #이동 알고리즘
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage
    moveValue = askinteger("이동 거리", "")
    ### 중요! ###
    outH = inH
    outW = inW

    outImageR = malloc2D(outH, outW)
    outImageG = malloc2D(outH, outW)
    outImageB = malloc2D(outH, outW)

    for i in range(outH):
        for k in range(outW):
            if  (i + moveValue > outH - 1) or (k + moveValue > outW - 1):
                pass
            else:
                outImageR[i + moveValue][k + moveValue] = inImageR[i][k]
                outImageB[i + moveValue][k + moveValue] = inImageB[i][k]
                outImageG[i + moveValue][k + moveValue] = inImageG[i][k]
    displayImage()

def zoomOutImage() : # 동일 영상 알고리즘
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB
    global outH, outW, window, canvas, paper, filename, inCVImage, outCVImage
    # (중요!) 출력 영상의 크기를 결정 --> 알고리즘에 의존
    scale = askinteger('이미지 축소', '축소 값 입력(2,4,6,8)', minvalue= 2, maxvalue= 8)
    outH = inH // scale
    outW = inW // scale

    outImageR = malloc2D(outH, outW)
    outImageG = malloc2D(outH, outW)
    outImageB = malloc2D(outH, outW)
    ## 진짜 영상처리 알고리즘 ##
    for i in range(inH) :
        for k in range(inW) :
            outImageR[i // scale][k // scale] = inImageR[i][k]
            outImageG[i // scale][k // scale] = inImageG[i][k]
            outImageB[i // scale][k // scale] = inImageB[i][k]
    ########################
    displayImage()

def zoomInNormalImage() : # 영상 확대 기본 알고리즘
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB
    global outH, outW, window, canvas, paper, filename, inCVImage, outCVImage
    # (중요!) 출력 영상의 크기를 결정 --> 알고리즘에 의존
    scale = askinteger('이미지 확대', '확대 값 입력(2,4,6,8)', minvalue=2, maxvalue=8)
    outH = inH * scale
    outW = inW * scale

    outImageR = malloc2D(outH, outW)
    outImageG = malloc2D(outH, outW)
    outImageB = malloc2D(outH, outW)
    ## 진짜 영상처리 알고리즘 ##
    for i in range(inH) :
        for k in range(inW) :
            outImageR[i * scale][k * scale] = inImageR[i][k]
            outImageG[i * scale][k * scale] = inImageG[i][k]
            outImageB[i * scale][k * scale] = inImageB[i][k]
    ########################
    displayImage()

def zoomIncloserImage() : #보간 확대
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB
    global outH, outW, window, canvas, paper, filename, inCVImage, outCVImage
    scale = askfloat("제목","최소 1.0이상",minvalue = 1.0)

    outH = int(inH * scale)
    outW = int(inW * scale)
    outImageR = malloc2D(outH, outW)
    outImageG = malloc2D(outH, outW)
    outImageB = malloc2D(outH, outW)

    for i in range(inH) :
        for k in range(inW) :
            outImageR[int(i * scale)][int(k * scale)] = inImageR[i][k]
            outImageG[int(i * scale)][int(k * scale)] = inImageG[i][k]
            outImageB[int(i * scale)][int(k * scale)] = inImageB[i][k]

    prepixelR, prepixelG, prepixelB = 0,0,0
    for i in range(outH) :
        for k in range(outW) :
            if outImageR[i][k] == 0 and prepixelR != 0:
                outImageR[i][k] = prepixelR ##가로축 보간 R
            prepixelR = outImageR[i][k]

            if outImageG[i][k] == 0 and prepixelG != 0:
                outImageG[i][k] = prepixelG ##가로축 보간 G
            prepixelG = outImageG[i][k]

            if outImageB[i][k] == 0 and prepixelB != 0:
                outImageB[i][k] = prepixelR ##가로축 보간 B
            prepixelB = outImageB[i][k]
        prepixelR, prepixelG, prepixelB = 0, 0 ,0

    for k in range(outW) :
        for i in range(outH) :
            if outImageR[i][k] == 0 and prepixelR != 0:
                outImageR[i][k] = prepixelR ##세로축 보간 R
            prepixelR = outImageR[i][k]

            if outImageG[i][k] == 0 and prepixelG != 0:
                outImageG[i][k] = prepixelG ##세로축 보간 G
            prepixelG = outImageG[i][k]

            if outImageB[i][k] == 0 and prepixelB != 0:
                outImageB[i][k] = prepixelB ##세로축 보간 B
            prepixelB = outImageB[i][k]
        prepixelR, prepixelG, prepixelB = 0, 0 ,0
    displayImage()

def rotateImage() :
    global inImageR, inImageG,inImageB,inH, inW, outImageR, outImageG, outImageB,outH, outW
    outH = inH
    outW = inW
    outImageR = malloc2D(outH, outW)
    outImageG = malloc2D(outH, outW)
    outImageB = malloc2D(outH, outW)

    degree360 = askfloat("제목", "몇 도? (ex.30)")
    center_x = int(inW / 2)
    center_y = int(inH / 2)
    seta = math.radians(degree360)
    new_x, new_y = 0,0

    for i in range(inH) :
        for k in range(inW) :
            new_x = int((i-center_y) * math.sin(seta) + (k-center_x) * math.cos(seta) + center_x)
            new_y = int((i-center_y) * math.cos(seta) - (k-center_x) * math.sin(seta) + center_y)

            if new_x < 0 :
                continue
            if new_x >= inH :
                continue
            if new_y < 0 :
                continue
            if new_y >= inW :
                continue

            outImageR[new_x][new_y] = inImageR[i][k]  ##회전된 좌표에 값 옮기기
            outImageG[new_x][new_y] = inImageG[i][k]  ##회전된 좌표에 값 옮기기
            outImageB[new_x][new_y] = inImageB[i][k]  ##회전된 좌표에 값 옮기기

    # return
    left_pixelR, right_pixelR = 0, 0
    left_pixelG, right_pixelG = 0, 0
    left_pixelB, right_pixelB = 0, 0

    ############## 오버랩과 홀 보간 ###################
    for i in range(outH) :
        for k in range(outW) :
            if k == 0 :
                right_pixelR = outImageR[i][k+1]
                left_pixelR = right_pixelR
            elif k == outW - 1 :
                left_pixelR = outImageR[i][k-1]
                right_pixelR = left_pixelR
            else :
                left_pixelR = outImageR[i][k-1]
                right_pixelR = outImageR[i][k+1]
            if outImageR[i][k] == 0 and left_pixelR != 0 and right_pixelR != 0 :
                outImageR[i][k] = int((left_pixelR + right_pixelR) / 2)

            if k == 0 :
                right_pixelG = outImageG[i][k+1]
                left_pixelG = right_pixelG
            elif k == outW - 1 :
                left_pixelG = outImageG[i][k-1]
                right_pixelG = left_pixelG
            else :
                left_pixelG = outImageG[i][k-1]
                right_pixelG = outImageG[i][k+1]
            if outImageG[i][k] == 0 and left_pixelG != 0 and right_pixelG != 0 :
                outImageG[i][k] = int((left_pixelG + right_pixelG) / 2)

            if k == 0 :
                right_pixelB = outImageB[i][k+1]
                left_pixelB = right_pixelB
            elif k == outW - 1 :
                left_pixelB = outImageB[i][k-1]
                right_pixelB = left_pixelB
            else :
                left_pixelB = outImageB[i][k-1]
                right_pixelB = outImageB[i][k+1]
            if outImageB[i][k] == 0 and left_pixelB != 0 and right_pixelB != 0 :
                outImageB[i][k] = int((left_pixelB + right_pixelB) / 2)

    displayImage()

def blurImage():   # 블러링 영상 알고리즘 3x3
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage
    blurValue = askinteger("블러링", "")
    ### 중요! ###
    outH = inH
    outW = inW

    outImageR = malloc2D(outH, outW)
    outImageG = malloc2D(outH, outW)
    outImageB = malloc2D(outH, outW)

    for i in range(outH):
        for k in range(outW):
            x = y = hapR = hapG = hapB = 0

            for a in range(blurValue**2):
                if a % blurValue == 0:
                    y = 0
                    x += 1
                y += 1
                if i + x >= outH  or k + y >= outW :
                    continue
                # print("outW ; outH ==> ",outW, outH)
                # print("i+x ; k+y ==> ",i+x,k+y)
                hapR += inImageR[i + x][k + y]
                hapG += inImageG[i + x][k + y]
                hapB += inImageB[i + x][k + y]

            avgR = int(hapR / blurValue ** 2)
            avgG = int(hapG / blurValue ** 2)
            avgB = int(hapB / blurValue ** 2)

            outImageR[i][k] = avgR
            outImageG[i][k] = avgG
            outImageB[i][k] = avgB
    displayImage()

def embossingImage():   # 엠보싱 영상 알고리즘
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage
    ### 중요! ###
    outH = inH
    outW = inW

    outImageR = malloc2D(outH, outW)
    outImageG = malloc2D(outH, outW)
    outImageB = malloc2D(outH, outW)

    emboMask = [[1, 1, 1], [1, -8, 1], [1, 1, 1]]
    s = 0
    for i in range(outH):
        for k in range(outW):
            sR = 0
            sG = 0
            sB = 0
            for n in range(3):
                for m in range(3):
                    if i + n >= outH - 1 or k + m >= outW - 1 :
                        continue
                    sR = sR + emboMask[n][m] * inImageR[i + n][k + m]
                    sG = sG + emboMask[n][m] * inImageG[i + n][k + m]
                    sB = sB + emboMask[n][m] * inImageB[i + n][k + m]

            if sR > 255:
                sR = 255
            if sR < 0:
                sR = 0

            if sG > 255:
                sG = 255
            if sG < 0:
                sG = 0

            if sB > 255:
                sB = 255
            if sB < 0:
                sB = 0

            outImageR[i][k] = sR
            outImageG[i][k] = sG
            outImageB[i][k] = sB


    displayImage()

def sharpImage():   # 샤프닝 영상 알고리즘
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage
    ### 중요! ###
    outH = inH
    outW = inW

    outImageR = malloc2D(outH, outW)
    outImageG = malloc2D(outH, outW)
    outImageB = malloc2D(outH, outW)

    sharpMask = [[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]
    s = 0
    for i in range(outH):
        for k in range(outW):

            sR = 0
            sG = 0
            sB = 0
            for n in range(3):
                for m in range(3):
                    if i + n >= outH - 1 or k + m >= outW - 1:
                        continue
                    sR = sR + sharpMask[n][m] * inImageR[i + n][k + m]
                    sG = sG + sharpMask[n][m] * inImageG[i + n][k + m]
                    sB = sB + sharpMask[n][m] * inImageB[i + n][k + m]

            if sR > 255:
                sR = 255
            if sR < 0:
                sR = 0

            if sG > 255:
                sG = 255
            if sG < 0:
                sG = 0

            if sB > 255:
                sB = 255
            if sB < 0:
                sB = 0

            outImageR[i][k] = sR
            outImageG[i][k] = sG
            outImageB[i][k] = sB

    displayImage()

def boundaryDetection():   # 경계선 검출 영상 알고리즘
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage
    ### 중요! ###
    outH = inH
    outW = inW

    outImageR = malloc2D(outH, outW)
    outImageG = malloc2D(outH, outW)
    outImageB = malloc2D(outH, outW)

    detectionMask = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    s = 0
    for i in range(outH):
        for k in range(outW):
            sR = 0
            sG = 0
            sB = 0
            for n in range(3):
                for m in range(3):
                    if i + n >= outH - 1 or k + m >= outW - 1:
                        continue
                    sR = sR + detectionMask[n][m] * inImageR[i + n][k + m]
                    sG = sG + detectionMask[n][m] * inImageG[i + n][k + m]
                    sB = sB + detectionMask[n][m] * inImageB[i + n][k + m]

            if sR > 255:
                sR = 255
            if sR < 0:
                sR = 0

            if sG > 255:
                sG = 255
            if sG < 0:
                sG = 0

            if sB > 255:
                sB = 255
            if sB < 0:
                sB = 0

            outImageR[i][k] = sR
            outImageG[i][k] = sG
            outImageB[i][k] = sB


    displayImage()

## OpenCV 전용 함수부 ##
def cv2output() :
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage

    outH = outCvImage.shape[0]
    outW = outCvImage.shape[1]
    ## 메모리 할당
    outImageR = malloc2D(outH, outW)
    outImageG = malloc2D(outH, outW)
    outImageB = malloc2D(outH, outW)
    ## OpenCV --> 메모리
    for i in range(outH):
        for k in range(outW):
            ## outCVImage가 2,3차원인지 체크후 대입
            if(outCvImage.ndim == 3) :
                outImageR[i][k] = outCvImage.item(i, k, 2)
                outImageG[i][k] = outCvImage.item(i, k, 1)
                outImageB[i][k] = outCvImage.item(i, k, 0)
            else :
                outImageR[i][k] = outCvImage.item(i, k)
                outImageG[i][k] = outCvImage.item(i, k)
                outImageB[i][k] = outCvImage.item(i, k)


def grayScale_cv() :
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage

    #####실제 영상처리########################################
    outCvImage = cv2.cvtColor(inCvImage, cv2.COLOR_BGR2GRAY)
    #########################################################
    ## OpenCV --> outImage 영상처리
    ## (중요!) 입력 이미지의 폭, 높이 알아내기
    cv2output()
    displayImage()

def bw1_cv() : # 이진화(칼라)
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage

    #####실제 영상처리########################################
    #outCvImage = cv2.cvtColor(inCvImage, cv2.COLOR_BGR2GRAY)
    _, outCvImage = cv2.threshold(inCvImage, 127, 255, cv2.THRESH_BINARY)
    #########################################################
    ## OpenCV --> outImage 영상처리
    ## (중요!) 입력 이미지의 폭, 높이 알아내기
    cv2output()
    displayImage()


def bw2_cv() : # 이진화(흑백)
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage

    #####실제 영상처리########################################
    outCvImage = cv2.cvtColor(inCvImage, cv2.COLOR_BGR2GRAY)
    _, outCvImage = cv2.threshold(outCvImage, 127, 255, cv2.THRESH_BINARY)
    #########################################################
    ## OpenCV --> outImage 영상처리
    ## (중요!) 입력 이미지의 폭, 높이 알아내기
    cv2output()
    displayImage()

def bw3_cv() : # 이진화(적응형)
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage

    #####실제 영상처리########################################
    outCvImage = cv2.cvtColor(inCvImage, cv2.COLOR_BGR2GRAY)
    outCvImage = cv2.adaptiveThreshold(outCvImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 33, -5)
    #########################################################
    ## OpenCV --> outImage 영상처리
    ## (중요!) 입력 이미지의 폭, 높이 알아내기
    cv2output()
    displayImage()

def zoomIn_cv() : # 확대
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage

    #####실제 영상처리########################################
    scale = askinteger('확대', '배율', maxvalue=8)
    outCvImage = cv2.resize(inCvImage, dsize=(inW*scale,inH*scale), interpolation=cv2.INTER_NEAREST)
    ########################################################
    ## OpenCV --> outImage 영상처리
    ## (중요!) 입력 이미지의 폭, 높이 알아내기
    cv2output()
    displayImage()

def emboss_cv() : # 엠보싱
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage

    #####실제 영상처리########################################
    mask = np.zeros((3,3), np.float32)
    mask[0][0] = -1.0
    mask[2][2] = 1.0
    outCvImage = cv2.filter2D(inCvImage, -1, mask)
    outCvImage += 127
    #########################################################
    ## OpenCV --> outImage 영상처리
    ## (중요!) 입력 이미지의 폭, 높이 알아내기
    cv2output()
    displayImage()

def zoomOut_cv() : # 축소
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage

    #####실제 영상처리########################################
    outCvImage = cv2.pyrDown(inCvImage, dstsize= None, borderType= None)
    #########################################################
    ## OpenCV --> outImage 영상처리
    ## (중요!) 입력 이미지의 폭, 높이 알아내기
    cv2output()
    displayImage()

def updownleRi_cv() : # 상하 대칭
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage

    #####실제 영상처리########################################
    outCvImage = cv2.flip(inCvImage, flipCode= -1)
    #########################################################
    ## OpenCV --> outImage 영상처리
    ## (중요!) 입력 이미지의 폭, 높이 알아내기
    cv2output()
    displayImage()

def canny_cv() : # 상하 대칭
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage

    #####실제 영상처리########################################
    outCvImage = cv2.Canny(inCvImage, 100, 200, apertureSize=3, L2gradient=True)
    #########################################################
    ## OpenCV --> outImage 영상처리
    ## (중요!) 입력 이미지의 폭, 높이 알아내기
    cv2output()
    displayImage()

def colorExt_cv() : # 상하 대칭
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage

    #####실제 영상처리########################################
    hsv = cv2.cvtColor(inCvImage, cv2.COLOR_BGR2HSV)  # RGB --> HSV
    h, s, v = cv2.split(hsv)
    h_orange = cv2.inRange(h, 8, 20) # 주황 Hue : 8~20

    outCvImage = cv2.bitwise_and(hsv, hsv, mask = h_orange)
    outCvImage = cv2.cvtColor(outCvImage, cv2.COLOR_HSV2BGR) # HSV --> RGB
    #########################################################
    ## OpenCV --> outImage 영상처리
    ## (중요!) 입력 이미지의 폭, 높이 알아내기
    cv2output()
    displayImage()

def frontFace_cv() :
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage

    #####실제 영상처리########################################
    ##모델(*인공지능) 불러오기. Classfire --> Pre_Trained Model
    face_clf = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    #얼굴 찾기
    gray = cv2.cvtColor(inCvImage, cv2.COLOR_BGR2GRAY) #그레이 스케일로 전환해야
    face_rects = face_clf.detectMultiScale(gray, 1.1, 5) # 파라미터 조절 가능
    outCvImage = inCvImage[:] # 원본을 복사, 출력 이미지에 네모를 씌워야하기 때문

    for (x, y, w, h) in face_rects :
        cv2.rectangle(outCvImage, (x,y), (x+w, y+h), (255, 0, 0), 3)

    #########################################################
    ## OpenCV --> outImage 영상처리
    ## (중요!) 입력 이미지의 폭, 높이 알아내기
    cv2output()
    displayImage()

def ssdNet(image) :
    CONF_VALUE = 0.8
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
            cv2.putText(image, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
    return image

def eyeDetect_cv() :
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage

    #####실제 영상처리########################################
    cvImage = cv2.imread(inCvImage)
    outCvImageImage = ssdNet(cvImage)

    #########################################################
    ## OpenCV --> outImage 영상처리
    ## (중요!) 입력 이미지의 폭, 높이 알아내기
    cv2output()
    displayImage()

def deepStillcut_cv() :
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage

    #####실제 영상처리########################################
    ##모델(*인공지능) 불러오기. Classfire --> Pre_Trained Model
    eye_clf = cv2.CascadeClassifier("haarcascade_eye.xml")
    # 얼굴 찾기
    gray = cv2.cvtColor(inCvImage, cv2.COLOR_BGR2GRAY)  # 그레이 스케일로 전환해야
    eye_rects = eye_clf.detectMultiScale(gray, 1.1, 5)  # 파라미터 조절 가능
    outCvImage = inCvImage[:]  # 원본을 복사, 출력 이미지에 네모를 씌워야하기 때문

    for (x, y, w, h) in eye_rects:
        cv2.rectangle(outCvImage, (x, y), (x + w, y + h), (0, 255, 0), 3)

    #########################################################
    ## OpenCV --> outImage 영상처리
    ## (중요!) 입력 이미지의 폭, 높이 알아내기
    cv2output()
    displayImage()

def deepMoive_cv() :
    global inImageR, inImageG, inImageB, inH, inW, outImageR, outImageG, outImageB, outH, outW
    global window, canvas, paper, filename, inCvImage, outCvImage

    #####실제 영상처리########################################
    ##모델(*인공지능) 불러오기. Classfire --> Pre_Trained Model
    eye_clf = cv2.CascadeClassifier("haarcascade_eye.xml")
    # 얼굴 찾기
    gray = cv2.cvtColor(inCvImage, cv2.COLOR_BGR2GRAY)  # 그레이 스케일로 전환해야
    eye_rects = eye_clf.detectMultiScale(gray, 1.1, 5)  # 파라미터 조절 가능
    outCvImage = inCvImage[:]  # 원본을 복사, 출력 이미지에 네모를 씌워야하기 때문

    for (x, y, w, h) in eye_rects:
        cv2.rectangle(outCvImage, (x, y), (x + w, y + h), (0, 255, 0), 3)

    #########################################################
    ## OpenCV --> outImage 영상처리
    ## (중요!) 입력 이미지의 폭, 높이 알아내기
    cv2output()
    displayImage()

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

def deepL_Movie () :

    import random
    def snapshot(image) :
        cv2.imwrite('c:/temp/save' + str(random.randint(11111,99999)) + '.png', image)


    ## 전역 변수부
    filename = "C:/images/traffic.mp4"
    #movie = cv2.VideoCapture(filename) # 영상파일
    movie = cv2.VideoCapture(0) # 카메라 연결

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

## 전역 변수부
inImageR, inImageG, inImageB, inH, inW  = None, None, None, 0, 0
outImageR, outImageG, outImageB, outH, outW  = None, None, None, 0, 0
inCVImage, outCVImage = None, None
window, canvas, paper = None, None, None
filename = ""

## 메인 코드부
window = Tk()
window.title("Computer Vision with AI (Ver 0.5)")
window.geometry('500x300')

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label='파일', menu=fileMenu)
fileMenu.add_command(label="열기", command=openImage)
fileMenu.add_command(label="저장", command=saveImage)
fileMenu.add_separator()
fileMenu.add_command(label="종료", command=None)

imageMenu = Menu(mainMenu)
mainMenu.add_cascade(label='화소점처리', menu=imageMenu)
imageMenu.add_command(label="그레이스케일", command=grayScaleImage)
imageMenu.add_command(label="밝게/어둡게", command=addMinusImage)
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
image2Menu.add_command(label="확대(이웃화소보간)", command=zoomIncloserImage)
image2Menu.add_command(label="회전", command=rotateImage)

image3Menu = Menu(mainMenu)
mainMenu.add_cascade(label='화소점영역', menu=image3Menu)
image3Menu.add_command(label="블러", command=blurImage)
image3Menu.add_command(label="엠보싱", command=embossingImage)
image3Menu.add_command(label="샤프", command=sharpImage)
image3Menu.add_command(label="경계선", command=boundaryDetection)

openCVMenu = Menu(mainMenu)
mainMenu.add_cascade(label='OpenCV(영상처리)', menu=openCVMenu)
openCVMenu.add_command(label="그레이스케일_CV", command=grayScale_cv)
openCVMenu.add_command(label="이진화(칼라)_CV", command=bw1_cv)
openCVMenu.add_command(label="이진화(흑백)_CV", command=bw2_cv)
openCVMenu.add_command(label="이진화(적응형)_CV", command=bw3_cv)
openCVMenu.add_command(label="확대_CV", command=zoomIn_cv)
openCVMenu.add_command(label="측소_CV", command=zoomOut_cv)
openCVMenu.add_command(label="엠보싱_CV", command=emboss_cv)
openCVMenu.add_command(label="대칭(상하좌우)_CV", command=updownleRi_cv)
openCVMenu.add_command(label="캐니 엣지_CV", command=canny_cv)

openCVMenu2 = Menu(mainMenu)
mainMenu.add_cascade(label='OpenCV(컴퓨터 비전)', menu=openCVMenu2)
openCVMenu2.add_command(label="색상수출", command=colorExt_cv)
openCVMenu2.add_command(label="머신러닝(얼굴인식)", command=frontFace_cv)
openCVMenu2.add_command(label="딥러닝(동영상)", command=deepL_Movie)

window.mainloop()