# -*- coding:utf-8 -*-
__author__ = 'Djj'

import sys
import os
import ConfigParser
import json
import DbIntf
import oracle_db
import datetime

from Tkinter import  Frame,Label,Tk,Entry,Button,StringVar,W,N,E,S
from ttk     import  Combobox

# 准备数据

def cur_file_dir():
     path = sys.path[0]
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

sDir = cur_file_dir() + '\\Config.ini'
config = ConfigParser.ConfigParser()
config.read(sDir)

sIP        = config.get("conn", "IP")
sDateBase  = config.get('conn', 'DateBase')
sUser      = config.get('conn', 'User')
sPassw     = config.get('conn', 'Paswd')
sWebSerIp  = config.get('conn', 'WebSerIp')
sDBType    = config.get('conn', 'DBType')
sParkCode  = config.get('conn', 'ParkCode')

def GetinfoCode():
    DcinfoCode = config.options("infoCode")
    return DcinfoCode



def WriteConfig(IP,DateBase,User,Paswd,WebSerIp,DBType,ParkCode):
    config.set("conn", "IP",IP)
    config.set('conn', 'DateBase',DateBase)
    config.set('conn', 'User',User)
    config.set('conn', 'Paswd',Paswd)
    config.set('conn', 'WebSerIp',WebSerIp)
    config.set('conn', 'DBType',DBType)
    config.set('conn', 'ParkCode',ParkCode)
    config.write(open(sDir, "w"))

Fconnet = False

root = Tk()
#居中
def center_window(w=600, h=200):
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

def createWidgets():
    nRow = 0
    Frame1=Frame(root,height = 200,width = 200)
    Frame1.grid(sticky=W)

    Label7 = Label(Frame1, text='类型说明:')
    Label7.grid(row=nRow,column=0,)
    Label7 = Label(Frame1, text='(0:oracle  / 1:SQL)')
    Label7.grid(row=nRow,column=1,)
    nRow +=1
    Label7 = Label(Frame1, text='数据库类型:')
    Label7.grid(row=nRow,column=0,)
    Dbtype = Entry(Frame1,textvariable=varDBType)
    Dbtype.grid(row=nRow,column=1)

    Label1 = Label(Frame1, text='数据库地址:')
    # Label1.pack(anchor=W)
    Label1.grid(row=nRow,column=0)
    IPInput = Entry(Frame1,textvariable=varIP)
    IPInput.grid(row=nRow,column=1)
    nRow +=1
    #
    Label2 = Label(Frame1, text='数据库名称:')
    Label2.grid(row=nRow,column=0,)
    ServerName = Entry(Frame1,textvariable=varDateBase)
    ServerName.grid(row=nRow,column=1)
    nRow +=1

    Label3 = Label(Frame1, text='用户名:')
    Label3.grid(row=nRow,column=0,)
    User = Entry(Frame1,textvariable=varUser)
    User.grid(row=nRow,column=1)
    nRow +=1

    Label4 = Label(Frame1, text='数据库密码:')
    Label4.grid(row=nRow,column=0,)
    DBPass = Entry(Frame1,show='*',textvariable=varPaswd)
    DBPass.grid(row=nRow,column=1)
    nRow +=1

    Label5 = Label(Frame1, text='接口地址:')
    Label5.grid(row=nRow,column=0,)
    WebSerIp = Entry(Frame1,textvariable=varWebSerIp)
    WebSerIp.grid(row=nRow,column=1)
    nRow +=1


    Frame2=Frame(Frame1,height = 50,width = 200)
    Frame2.grid(sticky=W,row=nRow,column=1)

    nRow =0
    BtnConnet = Button(Frame2, text='写入配置', command=Connet)
    BtnConnet.grid(row=nRow,column=0)

    quitButton = Button(Frame2, text='关闭', command=root.quit)
    quitButton.grid(row=nRow,column=1)

    Frame3=Frame(root,height = 50,width = 300)
    Frame3.grid(sticky=N)

    LabMess = Label(Frame3,text = '等待连接。。',font = 13,fg ='red')
    LabMess.grid(row=0,column=0)

    TestBtn = Button(Frame3,text='数据库连接',command=lambda:TestDBConnet(LabMess))
    TestBtn.grid(row=1,column=0)

    #接口部分




def Connet():
    WriteConfig(varIP.get(),varDateBase.get(),varUser.get(),varPaswd.get(),varWebSerIp.get(),varDBType.get(),varParkCode.get())

        # thread.start_new_thread(TestConnet,(root.Frame3.LabMess))

# http://192.168.0.44:8092/SOAP/?wsdl
def TestConnet(LabMess):
    from suds.client import Client
    try:
        WebIP = varWebSerIp.get()
        test=Client('http://'+ WebIP +':8092/SOAP/?wsdl')

        LabMess['text'] = '连接成功。'
        root.update()
    except ImportError:
        LabMess['text'] = '连接失败。'
        root.update()

def TestDBConnet(LabMess,isconnet=False):
    global Fconnet
    Fconnet = False
    if varDBType.get() == '0':
        oracle_db.engine = None
        sSQL = 'select 1 as Count from dual '
        oracle_db.create_engine(user=varUser.get(), password=varPaswd.get(), database=varDateBase.get(), host=varIP.get())
        try:
            LabMess['text'] = '数据库连接失败。'
            user =  oracle_db.select(sSQL)
            if user[0]['COUNT'] == 1:
                LabMess['text'] = '数据库连接成功。'
                Fconnet =True
            else:
                LabMess['text'] = '数据库连接失败。'
        except ImportError:
            root.update()
    if varDBType.get() == '1':
        DbIntf.engine = None
        sSQL = 'select 1 as Count  '
        DbIntf.create_engine(user=varUser.get(), password=varPaswd.get(), database=varDateBase.get(), host=varIP.get())
        try:
            LabMess['text'] = '数据库连接失败。'
            user =  DbIntf.select(sSQL)
            if user[0]['COUNT'] == 1:
                LabMess['text'] = '数据库连接成功。'
                Fconnet =True
            else:
                LabMess['text'] = '数据库连接失败。'
        except ImportError:
            root.update()



center_window(600, 300)

varIP = StringVar()
varDateBase = StringVar()
varUser = StringVar()
varPaswd = StringVar()
varWebSerIp = StringVar()
varDBType   = StringVar()
varParkCode =StringVar()
varinfoCode = StringVar()
varProc     =StringVar()

varIP.set(sIP)
varDateBase.set(sDateBase)
varUser.set(sUser)
varPaswd.set(sPassw)
varWebSerIp.set(sWebSerIp)
varDBType.set(sDBType)
varParkCode.set(sParkCode)
varinfoCode.set('')
varProc.set('')

createWidgets()

# 设置窗口标题:
root.title('MJSService')
root.resizable(False, False)
# 主消息循环:


root.mainloop()