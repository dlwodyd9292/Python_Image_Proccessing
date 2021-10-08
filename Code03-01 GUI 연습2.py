from tkinter import  *
from tkinter import  messagebox
from tkinter.simpledialog import *
from tkinter.filedialog import *
## 함수
def openMenu() :
    #messagebox.showinfo('파일', '열기를 선택함')
    # filename (pet.raw),  fullname(c:/images/pet.raw)
    fullname = askopenfilename(parent=window,
                filetypes= (('로우 파일', '*.raw'),('모든 파일', '*.*')))
    label2.configure(text=fullname)

def addImage() :
    value = askinteger('제목','내용', minvalue=-255, maxvalue=255)
    label1.configure(text=str(value))

## 메인
window = Tk()
window.title("GUI 연습2")
window.geometry('500x300')

mainMenu = Menu(window)  # 메뉴바 (비어 있음)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu) # 상위메뉴
mainMenu.add_cascade(label='파일', menu=fileMenu) # 상위메뉴를 메뉴바에 붙이기
fileMenu.add_command(label="열기", command=openMenu) # 하위 메뉴들
fileMenu.add_command(label="저장", command=None)
fileMenu.add_separator()
fileMenu.add_command(label="종료", command=None)

imageMenu = Menu(mainMenu) # 상위메뉴
mainMenu.add_cascade(label='영상처리', menu=imageMenu) # 상위메뉴를 메뉴바에 붙이기
imageMenu.add_command(label="밝게/어둡게", command=addImage) # 하위 메뉴들
imageMenu.add_command(label="반전", command=None)
imageMenu.add_command(label="흑백", command=None)
imageMenu.add_command(label="미러링", command=None)

label1 = Label(window, text='요기1', font=('궁서체',30) , fg='blue', bg='yellow')
label1.pack()
label2 = Label(window, text='요기요2', font=('궁서체',30) , fg='blue', bg='magenta')
label2.pack()

window.mainloop()