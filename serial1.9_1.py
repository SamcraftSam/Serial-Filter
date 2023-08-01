import serial
import sys
import threading

import tkinter as tk
from tkinter.ttk import Style
from tkinter import *

color = "grey20"
color2 = "grey25"
fontC = "grey90"
fontc2 = "green3"
ins = "white"
sizex = '300'
sizey = '50'
port = input("Port: ")
if not 'COM' in port:
        port ='COM'+port
byte = ['[0;32m', '[0m', '[0;33m']
with open('dict.txt') as f:
        filt = f.readlines()
ser = serial.Serial(port=port, baudrate=115200, timeout=0)
sys.setrecursionlimit(10**5) 
threading.stack_size(2**25)  
e = threading.Event()
file = b''
sr = []

def main():
        global file
        global sr
        c = 0
        s = ser.read(1)
        sr.append(s)
        file = b''.join(sr)
        if s == '\n'.encode():
                file = file.replace(byte[0].encode(), ''.encode())
                file = file.replace(byte[1].encode(), ''.encode())
                file = file.replace(byte[2].encode(), ''.encode())
                file = file.replace('\n'.encode(), ''.encode())
                file = file.decode(errors='ignore')
                while c <= len(filt)-1:
                        if not filt[c].strip() in file and c  == len(filt)-1 and file != '':
                                print(file)
                        elif filt[c].strip() in file:
                                break
                        c +=1
                c = 0
                file = ''
                sr = []

def main_cycle():
        while True:
                try:
                        main()
                except KeyboardInterrupt:
                        a = 1
                        print("Ctrl+C pressed...")
                        thread1.join(1)
                        thread2.join(1)
                        sys.exit(1)
                        return a
def gui():
        root = Tk()
        root.title(port + " insert window")
        root.geometry(sizex + "x" + sizey + "+300+300")
        root.configure(bg=color2)
        root.resizable(width=False, height=False)

        def send():
                out = e1.get() + '\n'
                ser.write(out.encode())
                #print(out)
                e1.delete(0, 'end')
                root.update()
        
        f2 = Frame(root)
        f2.pack(side=TOP, fill=BOTH,expand=True)
        b1 = Button(master=f2, text="Send", command=send, font=("Courier", 11), background=color, foreground=fontC)
        b1.pack(side=RIGHT,fill=BOTH, expand=True)
        e1 = Entry(master=f2, width=100, font=("Courier", 11))
        e1.pack(side=TOP, fill=BOTH, expand=True)
        e1.configure(foreground=fontC)
        e1.configure(background=color2, insertbackground=ins)
        e1.pack(fill=BOTH, expand=True)
        root.mainloop()
#if __name__ == "__main__":
thread1 = threading.Thread(target=main_cycle)
thread1.daemon = True
thread2 = threading.Thread(target=gui)
thread2.daemon = True
thread1.start()
thread2.start()
import time
while True:
        time.sleep(0.00001)
