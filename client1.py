import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import cv2
from PIL import Image,ImageTk
import wave
import numpy as np
import socket
import threading
import os
import pickle


def limit_char(string):
    return len(string) <= 8

HOST = 'localhost'
POST = 51000
file_path = ''

icon = None
icon_tk = None

def send(message_type,mess):
    data = {'icon':None,'name':'','message_type':message_type,'message':mess}
    data['name'] = entry_name.get()
    data['icon'] = icon
    data = pickle.dumps(data)
    while True:
        try:
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.connect((HOST,POST))
            sock.send(data)
            sock.close()
            break
        except:
            messagebox.showerror('error','送信に失敗しました。')
            break


def send_start(message_type,mess):
    th = threading.Thread(target=lambda:send(message_type,mess))
    th.start()


def file_choice():
    global file_path
    idir = 'C:\\'
    path = tk.filedialog.askopenfilename(initialdir=idir)
    if os.path.splitext(path)[1] in ['.png','.wav']:
        label_image['text'] = path.split('/')[-1]
        file_path = path
    else:
        messagebox.showerror('error','pngファイルかwavファイルを入力してください。')
        file_path = ''
        

def file_send():
    global file_path
    if os.path.splitext(file_path)[1] in ['.wav']:
        wf = wave.open(file_path)
        audio = wf.readframes(-1)
        mess = np.frombuffer(audio,dtype='int32')
        send(2,mess)
    elif os.path.splitext(file_path)[1] in ['.png']:
        try:
            mess = cv2.imread(file_path)
            mess = cv2.resize(mess,dsize=(70,70))
            mess = cv2.cvtColor(mess,cv2.COLOR_BGR2RGB)
            send(1,mess)
        except:
            messagebox.showerror('error','送信に失敗しました。\nパスに日本語は含めないでください。')
    else:
        messagebox.showerror('error','pngファイルかwavファイルを入力してください。')


def icon_change():
    global icon,icon_tk
    idir = 'C:\\'
    path = tk.filedialog.askopenfilename(initialdir=idir)
    if os.path.splitext(path)[1] in ['.png']:
        try:
            icon_cv = cv2.imread(path)
            icon_tk = cv2.resize(icon_cv,(200,200))
            icon_tk = cv2.cvtColor(icon_tk,cv2.COLOR_BGR2RGB)
            icon_tk = Image.fromarray(icon_tk)
            icon_tk = ImageTk.PhotoImage(icon_tk)
            icon = cv2.resize(icon_cv,dsize=(70,70))
            icon = cv2.cvtColor(icon,cv2.COLOR_BGR2RGB)
            icon_canvas.create_image(0,0,anchor=tk.NW,image=icon_tk)
        except:
            messagebox.showerror('error','アイコンの読み込みに失敗しました。\nパスに日本語は含めないでください。')
    else:
        messagebox.showerror('error','pngファイルを入力してください。')

root = tk.Tk()
root.geometry('400x600')

icon = cv2.imread('./icon.png')
icon_tk = cv2.resize(icon,(200,200))
icon_tk = cv2.cvtColor(icon_tk,cv2.COLOR_BGR2RGB)

icon = cv2.resize(icon,(70,70))
icon = cv2.cvtColor(icon,cv2.COLOR_BGR2RGB)


icon_tk = Image.fromarray(icon_tk)
icon_tk = ImageTk.PhotoImage(icon_tk)

icon_canvas = tk.Canvas(root,bg="white")
icon_canvas.place(x=100,y=10,width=200,height=200)
icon_canvas.create_image(0,0,anchor=tk.NW,image=icon_tk)

button_icon = tk.Button(
    root,
    text="アイコン変更",
    command=icon_change
)
button_icon.place(x=200,y=220,anchor=tk.CENTER)


vc = root.register(limit_char)
entry_name = tk.Entry(root,width=20,validate="key",validatecommand=(vc,"%P"))
entry_name.place(x=200,y=260,anchor=tk.CENTER)
entry_name.insert(0,'user1')


entry_message = ScrolledText(root)
entry_message.place(x=200,y=350,width=200,height=100,anchor=tk.CENTER)

button_message = tk.Button(
    root,
    text="テキストを送信",
    command=lambda:send_start(0,entry_message.get("1.0","end-1c"))
)
button_message.place(x=200,y=420,anchor=tk.CENTER)


button_image_choice = tk.Button(
    root,
    text="画像,音声を選択",
    command=file_choice
)
button_image_choice.place(x=200,y=500,anchor=tk.CENTER)

label_image = tk.Label(
    root,
    text='画像,音声が選択されていません'
)
label_image.place(x=200,y=530,anchor=tk.CENTER)

button_image_send = tk.Button(
    root,
    text="画像,音声を送信",
    command=file_send
)
button_image_send.place(x=200,y=560,anchor=tk.CENTER)

root.resizable(False,False)
root.mainloop()