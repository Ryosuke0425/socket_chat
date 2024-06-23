import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter.scrolledtext import ScrolledText
from socket import socket,AF_INET,SOCK_STREAM
import threading
import cv2
import numpy as np
import wave
import sounddevice as sd
import pickle

root = tk.Tk()
root.geometry('400x600')
canvas = tk.Canvas(root)
frame = tk.Frame(canvas)
scrollbar = tk.Scrollbar(
    canvas,orient=tk.VERTICAL,command=canvas.yview
)

canvas.configure(scrollregion=(0,0,0,610))
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
canvas.pack(expand=True,fill=tk.BOTH)
canvas.create_window((0,0),window=frame,anchor=tk.NW,width=400,height=10000)

messages = []
messages_show = []
icons = []
icons_show = []
names = []
count = 0

HOST = 'localhost'
PORT = 51000
MAX_MESSAGE = 1024
NUM_THREAD = 4

def receive():
    global count
    print('receiver ready, NUM_THREAD=' + str(NUM_THREAD))
    while True:
        try:
            sock = socket(AF_INET,SOCK_STREAM)
            sock.bind((HOST,PORT))
            sock.listen(NUM_THREAD)
            conn,addr = sock.accept()
            data_sum = bytes()

            while True:
                data = conn.recv(MAX_MESSAGE)
                if not data:
                    break
                data_sum += data

            data_sum = pickle.loads(data_sum)
            icon = data_sum['icon']
            icon = Image.fromarray(icon)
            icon = ImageTk.PhotoImage(icon)
            icons.append(icon)
            icons_show.append(
                    tk.Label(
                        frame,
                        image=icons[count],
                        width=70,
                        height=70)
            )
            icons_show[count].place(x=15,y= 100*count + 15,anchor=tk.NW)
            name = data_sum['name']
            names.append(tk.Label(
                frame,
                text=name,
            ))
            names[count].place(x=50,y=99 + count * 100,anchor=tk.CENTER)

            if data_sum['message_type'] == 0:
                messages.append(data_sum['message'])
                messages_show.append(ScrolledText(frame))
                messages_show[count].insert(tk.END,messages[count])
                messages_show[count]['state'] = 'disabled'
                messages_show[count].place(x=110,y=100*count+10,width=270,height=80,anchor=tk.NW)
            elif data_sum['message_type'] == 1:
                img = Image.fromarray(data_sum['message'])
                img = ImageTk.PhotoImage(img)
                messages.append(img)
                messages_show.append(
                    tk.Label(
                        frame,
                        image=messages[count],
                        width=70,
                        height=70)
                )
                messages_show[count].place(x=235,y= 100*count + 50,anchor=tk.CENTER)
            elif data_sum['message_type'] == 2:
                messages.append(data_sum['message'])
                messages_show.append(
                    tk.Button(
                        frame,
                        text='音声データが送信されました',
                        command=play(count)
                    )
                )
                messages_show[count].place(x=235,y=100*count+50,anchor=tk.CENTER)
            if count >=  6:
                canvas.configure(scrollregion=(0,0,0,(count+1) * 100 + 10))
                canvas.yview_moveto(1)
            count += 1

        except:
            print('ERROR')
    sock.close()

def receive_start():
    th = threading.Thread(target=receive)
    th.start()


def play(count):
    def x():
        sd.play(messages[count])
        status = sd.wait()
    return x


receive_start()

root.resizable(False,False)
root.mainloop()