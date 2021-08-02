from PIL import Image,ImageDraw
import tkinter
from tkinter import ttk
import pickle
import numpy as np
import os
press=False
formura=""
im = Image.new('RGB', (300, 300), (0,0,0))
draw = ImageDraw.Draw(im)

#絵を描く部分

def Move_func(event):
    global canvas
    x = event.x
    y = event.y
    if press:
        canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill = "black", width=0)
        draw.ellipse((x - 10, y - 10, x + 10, y + 10), fill="white")

def Click_func(event):
    global press
    press = True

def Release_func(event):
    global press
    press = False

#消去と予測

def Delete_and_pred_num(event):
    canvas.delete("all")
    img = im.resize((28, 28))
    img.save('pillow_imagedraw.jpg')
    img=img.convert("L")   #RGB->grayscale
    img=np.asarray(img)
    img = img.reshape((28 * 28)) #flatten
    img=img.astype(np.float32)
    img=img/255            #normalize
    network=init__network()
    y=Predict(network,img)
    p=np.argmax(y)
    print(p) #debug
    draw.rectangle((0,0,300,300),fill="black")
    return str(p)

#DeepLeaning部分

def init__network():
    path=os.path.dirname(__file__)
    path1=os.path.join(path,"weight.pkl")
    with open(path1,"rb") as f:
        network=pickle.load(f)
    return network
def sigmoid(x):
    return 1/(1+np.exp(-x))

def softmax(x):
    c=np.max(x)
    exp_a=np.exp(x  -c)
    sum_exp_a=np.sum(exp_a)
    y=exp_a/sum_exp_a
    return y

def Predict(network,x):
    W1,W2,W3=network["W1"],network["W2"],network["W3"]
    b1,b2,b3=network["b1"],network["b2"],network["b3"]

    a1=np.dot(x,W1)+b1
    z1=sigmoid(a1)
    a2=np.dot(z1,W2)+b2
    z2=sigmoid(a2)
    a3=np.dot(z2,W3)+b3
    y=softmax(a3)
    return y


#電卓機能部分

def Clear_func(event):
    global formura
    num=Delete_and_pred_num(event)
    formura=""
    result["text"]=formura
    print(formura)
def Plus_func(event):
    global formura
    num=Delete_and_pred_num(event)
    formura+=num+"+"
    print(formura) #debug
    result["text"]=formura
def Minus_func(event):
    global formura
    num=Delete_and_pred_num(event)
    formura+=num+"-"
    print(formura) #debug
    result["text"]=formura
def Mul_func(event):
    global formura
    num=Delete_and_pred_num(event)
    formura+=num+"*"
    print(formura) #debug
    result["text"]=formura
def Div_func(event):
    global formura
    num=Delete_and_pred_num(event)
    formura+=num+"/"
    print(formura) #debug
    result["text"]=formura
def Power_func(event):
    global formura
    num=Delete_and_pred_num(event)
    formura+=num+"**"
    print(formura) #debug
    result["text"]=formura
def Root_func(event):
    global formura
    num=Delete_and_pred_num(event)
    formura+=num+"**1/"
    print(formura) #debug
    result["text"]=formura
def Rank_func(event):
    global formura
    num=Delete_and_pred_num(event)
    formura+=num
    print(formura) #debug
    result["text"]=formura
def Equal_func(event):
    global formura
    num=Delete_and_pred_num(event)
    formura+=num
    print(formura,"=",eval(formura)) #debug
    result["text"]=formura+"="+str(eval(formura))
    formura=""
#GUI  
win = tkinter.Tk()
win.geometry("750x500")
win.configure(background='#BDC0C2')
reset_button=tkinter.Button(text="DELETE",width=5,height=2,highlightbackground="#891616")
reset_button.bind("<Button-1>",Delete_and_pred_num)
reset_button.place(x=165,y=370)
win.title("おっちょこちょいな手書き電卓")
win.resizable(width=False, height=False) 
canvas=tkinter.Canvas(win,width=300,height=300,bg="#7BAA17")
canvas.place(x=50,y=50)
clear_button=tkinter.Button(text="C",width=5,height=4,highlightbackground="#1F1FFF")
clear_button.bind("<Button-1>",Clear_func)
clear_button.place(x=363,y=50)
plus_button=tkinter.Button(text="＋",width=5,height=4,highlightbackground="#1F1FFF")
plus_button.bind("<Button-1>",Plus_func)
plus_button.place(x=450,y=50)
minus_button=tkinter.Button(text="−",width=5,height=4,highlightbackground="#1F1FFF")
minus_button.bind("<Button-1>",Minus_func)
minus_button.place(x=537,y=50)
mul_button=tkinter.Button(text="×",width=5,height=4,highlightbackground="#1F1FFF")
mul_button.bind("<Button-1>",Mul_func)
mul_button.place(x=363,y=131)
div_button=tkinter.Button(text="÷",width=5,height=4,highlightbackground="#1F1FFF")
div_button.bind("<Button-1>",Div_func)
div_button.place(x=450,y=131)
power_button=tkinter.Button(text="^",width=5,height=4,highlightbackground="#1F1FFF")
power_button.bind("<Button-1>",Power_func)
power_button.place(x=537,y=131)
rank_button=tkinter.Button(text="位",width=5,height=4,highlightbackground="#1F1FFF")
rank_button.bind("<Button-1>",Rank_func)
rank_button.place(x=363,y=212)
equal_button=tkinter.Button(text="=",width=5,height=4,highlightbackground="#1F1FFF")
equal_button.bind("<Button-1>",Equal_func)
equal_button.place(x=450,y=212)
sub_title=tkinter.Label(text="result",font=("",30),bg="#BDC0C2",fg="#000000")
sub_title.place(x=366,y=300)
frame=tkinter.Frame(win,width="300",height="100",bg="white",bd="5",relief=tkinter.SUNKEN)
frame.place(x=370,y=345)
result=tkinter.Label(text="",font=("",30),bg="white",fg="#000000")
result.place(x=375,y=370)
win.bind("<Motion>",Move_func)
win.bind("<ButtonPress>",Click_func)
win.bind("<ButtonRelease>",Release_func)
win.mainloop()