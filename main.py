#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import tkinter as tk
import pandas as pd
from tkinter import *
from sklearn import linear_model

#登記資料
def add():
    sta = []
    sta.append((text1.get('0.0','end').replace(' ','')).strip()) #去除空白和換行
    sta.append((text2.get('0.0','end').replace(' ','')).strip())
    sta.append((text3.get('0.0','end').replace(' ','')).strip())
    mylist = pd.read_excel('./data.xlsx',index_col = 0) #讀出excel
    last_i = mylist.index[-1] # 找最新一筆資料的index
    mylist.loc[last_i+1] = [sta[0],sta[1],sta[2]] #加入新資料
    if(sta[0]=="" or sta[1]=="" or sta[2]==""):
        label_show1['text'] = "登記失敗"
    else:
        df = pd.DataFrame(mylist,columns=['日期','確診','死亡'])
        filePath = r'.\data.xlsx' 
        df.to_excel(filePath,index=True)    #將資料寫入excel
        print('save to',filePath,'successfully') #確認有寫進去
        text1.delete('1.0', 'end')
        text2.delete('1.0','end')
        text3.delete('1.0', 'end') #清空text
        print_data()

# 續add後 印出結果
def print_data():
    data = pd.read_excel("./data.xlsx")
    last_i = data.index[-1]
    print_x = np.array(data[["確診"]])
    print_y = np.array(data[["死亡"]])
    label_show1['text']  = "登記成功，"+"自"+str(data.loc[0][1]) + " 起，至" +         str(data.loc[last_i][1]) +" 累計確診" + str(print_x.sum()) + "人"
    label_show2['text']  = "死亡"+ str(print_y.sum()) + "人，"+'死亡率：' +          str(round(print_y.sum()/print_x.sum()*1000,3))+ "%"

#由線性方程預測人數
def get_y(x,intercept,slope): # 由確診預測死亡
    y = x*slope + intercept
    return y
def get_x(y,intercept,slope): # 由死亡預測確診
    x = (y-intercept)/slope
    return x  


# 訓練資料，預測實際確診
def pri_get():
    train = pd.read_excel("./data.xlsx")
    regr = linear_model.LinearRegression()
    last_i = train.index[-1] # 找最新一筆資料的index
    train_x = np.array(train[["確診"]])
    train_y = np.array(train[["死亡"]])
    train_x = train_x[:-8:]   #平移8格，因為確診8天左右死亡，讓資料對上
    train_y = train_y[8::]
    regr.fit(train_x,train_y) #ML預測
    sta = []
    sta.append((text4.get('0.0','end').replace(' ','')).strip())
    if(sta[0]!=""):   
        y_death = int(sta[0])
        pri_get = get_x(y_death,regr.intercept_[0],regr.coef_[0][0])
        label_show4["text"] = "預測實際確診數:" + str(round(pri_get))
    else:
        label_show4["text"] = "請輸入數字"

# 訓練資料，預測明日死亡數   
def pri_tomo():
    train = pd.read_excel("./data.xlsx")
    regr = linear_model.LinearRegression()
    last_i = train.index[-1]
    train_x = np.array(train[["確診"]])
    train_y = np.array(train[["死亡"]])
    train_x = train_x[:-8:]             
    train_y = train_y[8::]
    regr.fit(train_x,train_y)
    x = (train.loc[last_i-6][2]+train.loc[last_i-7][2]*2+train.loc[last_i-8][2])/4 #加了一些權重
    pri_get = get_y(x,regr.intercept_[0],regr.coef_[0][0])
    label_show4["text"] = "預測死亡人數:" + str(round(pri_get))+ "，死亡率："+    str(round(regr.coef_[0][0]*100,3))+ "%"
  
    
    


# In[2]:


from ttkbootstrap import Style
from tkinter import ttk

win = tk.Tk()
win.title('Covid-19')
win.geometry('420x530')
win.configure(bg="lightsteelblue")

#介面
label_show0 = tk.Label(win,text = '登記系統：',bg = "wheat",font = ('Arial',14))
label_show0.grid(row=0, padx = 5, pady = 5 ,sticky=W)

label1 = tk.Label(win,text = '輸入日期：',bg = "darkblue",fg = "white",font = ('Arial',10))
label1.grid(row=1, padx = 10, pady = 10, sticky=W)

text1 = tk.Text(win, width = 40, height = 1)
text1.grid(row=1, padx = 110, pady = 10)

label2 = tk.Label(win,text = '確診人數：',bg = "darkblue",fg = "white",font = ('Arial',10))
label2.grid(row=2, padx = 10, sticky=W)

text2 = tk.Text(win, width = 40, height = 1)
text2.grid(row=2, padx = 110, pady = 10)

label3 = tk.Label(win,text = '死亡人數：',bg = "darkblue",fg = "white",font = ('Arial',10))
label3.grid(row=3, padx = 10, sticky=W)

text3 = tk.Text(win, width = 40, height = 1)
text3.grid(row=3, padx = 110, pady = 10)

button_send = tk.Button(win,text = '登 記',font = ('Arial',12,'bold'),width = 38,                        height = 2, fg = 'white', bg = 'green', command = add)
button_send.grid(row=4, padx = 10, pady = 5, sticky=W)

label_show1 = tk.Label(win,font = ('Arial',10),bg="lightsteelblue")
label_show1.grid(row=5, padx = 30, pady = 1 ,sticky=W)

label_show2 = tk.Label(win,font = ('Arial',10),bg="lightsteelblue")
label_show2.grid(row=6, padx = 30, pady = 1 ,sticky=W)

label_show3 = tk.Label(win,text = '預測系統：',bg = "wheat",font = ('Arial',14))
label_show3.grid(row=7, padx = 5, pady = 5 ,sticky=W)

label4 = tk.Label(win,text = '死亡人數：',bg = "darkblue",fg = "white",font = ('Arial',10))
label4.grid(row=8, padx = 10, pady = 10 ,sticky=W)

text4 = tk.Text(win, width = 40, height = 1)
text4.grid(row=8, padx = 110, pady = 10)

button_pri = tk.Button(win,text = '預 測 實 際 確 診 人 數',font = ('Arial',12,'bold'),width =38, height = 2,                        fg = 'white', bg = 'green', command = pri_get)
button_pri.grid(row=9, padx = 10, pady = 5, sticky=W)

button_pri = tk.Button(win,text = '預 測 明 日 死 亡 人 數',font = ('Arial',12,'bold'),width =38, height = 2,                        fg = 'white', bg = 'green', command = pri_tomo)
button_pri.grid(row=10, padx = 10, pady = 5, sticky=W)


label_show4 = tk.Label(win,font = ('Arial',10),bg="lightsteelblue")
label_show4.grid(row=11, padx = 30, pady = 1 ,sticky=W)

win.mainloop()

