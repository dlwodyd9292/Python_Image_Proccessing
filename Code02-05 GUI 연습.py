from tkinter import *
from tkinter import messagebox

## 함수 선언부
def clickButton() :
    # messagebox.showinfo("제목", "내용")
    label2.config(text='이름바뀜')
## 메인 코드부
window = Tk()
window.title("윈도우창")
window.geometry('500x700')
window.resizable(width = False, height= False)

## 여기에 화면을 구성하고 처리
label1 = Label(window, text='안녕하세요?')
label1.pack()

label2 = Label(window, text='Hello World', font=('궁서체', 30), fg='blue', bg='yellow')
label2.pack()

button1 = Button(window, text='버튼 클릭', fg='red', command=clickButton)
button1.place(x=5, y=10)

photo = PhotoImage(file='C:\images\lion.png')
label3 = Label(window, image=photo)
label3.pack()


window.mainloop()