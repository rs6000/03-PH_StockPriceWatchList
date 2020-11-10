'''


'''
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import datetime
from datetime import date, timedelta

default_timer = 180
mytimer = default_timer

def marketopen():
    todayis = date.today()
    week = datetime.datetime.strptime(str(todayis), "%Y-%m-%d").isoweekday()
    Open_time = datetime.datetime.strptime(
        str(datetime.datetime.now().date()) + '9:30', '%Y-%m-%d%H:%M')
    Closed_time = datetime.datetime.strptime(
        str(datetime.datetime.now().date()) + '15:30', '%Y-%m-%d%H:%M')
    Now_time = datetime.datetime.now()
    ot = False
    # print('Open_time={}\nClosed_time={}\nNow_time={}'.format(Open_time,Closed_time,Now_time))
    if week < 6:
        if Now_time > Open_time and Now_time < Closed_time:
            ot = True
        else:
            ot = False
    else:
        ot = False
    return ot

def GetPrice():
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
    url = 'https://www.pesobility.com/stock'
    res = requests.get(url, headers=headers)
    df = pd.read_html(res.text)[0]
    df = df.set_index(['Symbol'])
    df2 = df.drop(columns=['Name', '52-Week High (%)',
                           '52-Week Low', 'PE', '2019 Cash Div (%)'], axis=1)
    df2.rename(columns={'Current Price (%)': 'Current Price'}, inplace=True)
    df2['Current Price'] = df2['Current Price'].apply(
        lambda x: float(re.sub('\(.*\)', '', x)))
    df2['change'] = (
        (df2['Current Price'] - df2['Previous Close'])/df2['Previous Close'])*100

    return df2
# ===================================================================================

all_list = GetPrice()

# flag 用來偵測關注名單是否為初始值
flag = 0

refresh_F5 = 0

default_list = ['BDO', 'JFC', 'MM', 'DITO', 'ALI']
mylist = GetPrice().loc[default_list]


watch_list = []
# ===================================================================================
root = tk.Tk()
root.title('看盤小幫手')
root.geometry('270x300')
root.wm_attributes('-topmost', 1)
root.resizable(False, False)
# ===================================================================================
def Clock():
    global mytimer, refresh_F5
    mytimer -= 1

    localtime = time.strftime('%I:%M', time.localtime())
    lbl_lastupdate.config(text="現在時間:"+localtime,
                          font=("Helvetica", 12), fg="blue")

    lbl_countdown.config(text='更新倒數計時:{}'.format(mytimer),
                         font=("Helvetica", 12), fg="red")
    if mytimer == 0:
        mytimer = default_timer+1
        Clean_WatchList()
        Display_TreeView()
        refresh_F5 = 0
        Clock()
    else:
        root.after(1000, Clock)
# ===================================================================================
def Clean_WatchList():
    tree.delete(*tree.get_children())
# ===================================================================================
def Clean_TxTinput():
    txt_input.delete(0, "end")
# ===================================================================================
def Add_Symbol():
    global mylist, watch_list, flag
    symbol = txt_input.get().upper()
    
    if symbol in watch_list:
        messagebox.showwarning("重覆輸入", "{} 已在關注名單內".format(symbol))
        Clean_TxTinput()
    elif symbol == '':
        messagebox.showwarning("錯誤訊息", "請輸入資料!!!")
    elif symbol not in all_list.index:
        messagebox.showwarning("錯誤訊息", "股票代碼: {} 不在股票名單內".format(symbol))
        Clean_TxTinput()
    elif len(watch_list) >= 10:
        messagebox.showwarning("提示訊息", "關注名單只能10筆以下")
        Clean_TxTinput()
    else:
        if flag == 0:
            watch_list = default_list
            flag += 1
        watch_list.append(str(symbol).upper())
        mylist = all_list.loc[watch_list]
        Clean_WatchList()
        Display_TreeView()
        Clean_TxTinput()
# ===================================================================================
def Del_Symbol():
    global default_list, watch_list, flag
    if flag == 0:
        watch_list = default_list
        flag += 1
    myselect = tree.selection()
    if not myselect:
        messagebox.showwarning("錯誤訊息", "請輸入資料!!!")
    else:
        for item in tree.selection():
            item_text = tree.item(item, "values")[1]
            watch_list.remove(item_text)
            tree.delete(item)
# ===================================================================================
def KeyListener(event):
    global mytimer, refresh_F5
    if event.keycode == 46:
        Del_Symbol()
    elif event.keycode == 116:
        if mytimer >= 90 and refresh_F5 == 1:
            messagebox.showwarning("提示訊息", "禁止快速刷新!!!")
        else:
            mytimer = default_timer+1
            refresh_F5 = 1
    else:
        pass
# ===================================================================================
def TreeView_Sort_Column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(key=lambda t: float(t[0]), reverse=reverse)
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col,
               command=lambda: TreeView_Sort_Column(tv, col, not reverse))
# ===================================================================================
lbl_lastupdate = tk.Label(root)
lbl_lastupdate.grid(row=0, column=0, columnspan=4)
# ===================================================================================
columns = ('0', '1', '2')
tree = ttk.Treeview(root, show='headings', columns=columns)
tree.column('0', width=30, anchor='e')
tree.column('1', width=120, anchor='center')
tree.column('2', width=120, anchor='center')
tree.tag_configure('+', background='red')
tree.tag_configure('-', background='green')
tree.heading('0', text='#')
tree.heading('1', text='Symbol')
tree.heading('2', text='Current Price')
# ===================================================================================
def Display_TreeView():
    global flag, mylist, watch_list
    if flag == 0:
        mylist = GetPrice().loc[default_list]
    else:
        mylist = GetPrice().loc[watch_list]

    n = 1
    for j, k, x in zip(mylist.index, mylist['Current Price'].values, mylist['change']):
        i = [int(n), str(j), str(k)]
        n += 1
        if x < 0:
            tree.insert('', 'end', values=i, tags=('-',))
        elif x == 0:
            tree.insert('', 'end', values=i,)
        else:
            tree.insert('', 'end', values=i, tags=('+',))
# ===================================================================================
tree.grid(row=1, column=0, columnspan=4)
# ===================================================================================
lbl_addsymbol = tk.Label(root, text="增加股票代號:", fg="green")
lbl_addsymbol.grid(row=2, column=0)
txt_input = tk.Entry(root, width=10)
txt_input.grid(row=2, column=1)
btn_confirm = tk.Button(root, text="確認", fg="green", command=Add_Symbol)
btn_confirm.grid(row=2, column=2)
btn_delete = tk.Button(root, text="刪除", fg="red", command=Del_Symbol)
btn_delete.grid(row=2, column=3)
# ===================================================================================
lbl_countdown = tk.Label(root, text="現在不是開盤時間，只提供最後報價資料", fg="red")
lbl_countdown.grid(row=4, column=0, columnspan=4)
# ===================================================================================
for col in columns:
    if col in columns[1]:
        continue
    tree.heading(
        col, command=lambda c=col: TreeView_Sort_Column(tree, c, False))
# ===================================================================================
root.bind('<Return>', lambda event=None: btn_confirm.invoke())
root.bind('<Key>', KeyListener)
# ===================================================================================
check_opt = marketopen()
if check_opt == True:
    Display_TreeView()
    Clock()
else:
    Display_TreeView()
# Run
root.mainloop()