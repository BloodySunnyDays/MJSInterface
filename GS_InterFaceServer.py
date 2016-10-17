# -*- coding:utf-8 -*-
__author__ = 'Djj'

import sys
import os
import ConfigParser
import json
import DbIntf
import oracle_db
import datetime
import urllib2
import urllib
import time
import threading
from Tkinter import  Frame,Label,Tk,Entry,Button,StringVar,W,N
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
sSleepTime = config.get('conn', 'sleeptime')
sFormatJson= config.get('conn', 'formatjson')

def GetinfoCode():
    DcinfoCode = config.options("infoCode")
    return DcinfoCode



def WriteConfig(IP,DateBase,User,Paswd,WebSerIp,DBType,ParkCode,SleepTime):
    config.set("conn", "IP",IP)
    config.set('conn', 'DateBase',DateBase)
    config.set('conn', 'User',User)
    config.set('conn', 'Paswd',Paswd)
    config.set('conn', 'WebSerIp',WebSerIp)
    config.set('conn', 'DBType',DBType)
    config.set('conn', 'ParkCode',ParkCode)
    config.set('conn', 'SleepTime',SleepTime)
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

    Label7 = Label(Frame1, text='(V5)类型说明:')
    Label7.grid(row=nRow,column=0,)
    Label7 = Label(Frame1, text='(0:oracle  / 1:SQL)')
    Label7.grid(row=nRow,column=1,)
    nRow +=1
    Label7 = Label(Frame1, text='数据库类型:')
    Label7.grid(row=nRow,column=0,)
    Dbtype = Entry(Frame1,textvariable=varDBType)
    Dbtype.grid(row=nRow,column=1)
    nRow +=1

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

    Label12 = Label(Frame1, text='        上传间隔:')
    Label12.grid(row=nRow,column=0)
    Input3 = Entry(Frame1,textvariable=varSleeptime)
    Input3.bind('<KeyRelease>', keyPress)
    Input3.grid(row=nRow,column=1)
    nRow +=1


    Frame2=Frame(Frame1,height = 50,width = 200)
    Frame2.grid(sticky=W,row=nRow,column=1)


    nRow =0
    BtnConnet = Button(Frame2, text='写入配置', command=Connet)
    BtnConnet.grid(row=nRow,column=0)


    Frame3=Frame(root,height = 50,width = 300)
    Frame3.grid(sticky=N)

    LabMess = Label(Frame3,text = '等待连接。。',font = 13,fg ='red')
    LabMess.grid(row=0,column=0)

    TestBtn = Button(Frame3,text='数据库连接',command=lambda:TestDBConnet(LabMess))
    TestBtn.grid(row=1,column=0)

    Btn1 = Button(Frame3,text='接口测试',command=lambda:IntfConnetTest(LabMess))
    Btn1.grid(row=1,column=2,padx=10)

    Btn2 = Button(Frame3,text='开始上传',command=lambda:Thread_SaveLoad(LabMess))
    Btn2.grid(row=1,column=4,padx=10)

    quitButton = Button(Frame3, text='关闭', command=Quit)
    quitButton.grid(row=1,column=5,padx=10)

    #接口部分
    nRow = 0
    Label8 = Label(Frame1, text='        接口参数： ')
    Label8.grid(row=nRow,column=2,columnspan=2)
    nRow +=1

    Label9 = Label(Frame1, text='        景区编码:')
    Label9.grid(row=nRow,column=2)
    IPInput = Entry(Frame1,textvariable=varParkCode)
    IPInput.grid(row=nRow,column=3)
    nRow +=1

    Label10 = Label(Frame1, text='        业务编码:')
    Label10.grid(row=nRow,column=2)
    combox1 = Combobox(Frame1,textvariable=varinfoCode,values=GetinfoCode(),width=18,)
    combox1.bind("<<ComboboxSelected>>", comboxChanged,)
    combox1.grid(row=nRow,column=3,)
    nRow +=1

    Label11 = Label(Frame1, text='        存储过程:')
    Label11.grid(row=nRow,column=2)
    Input3 = Entry(Frame1,textvariable=varProc)
    Input3.grid(row=nRow,column=3)
    nRow +=2

    SaveBtn = Button(Frame1,text='保存存储过程',command=SaveProc)
    SaveBtn.grid(row=nRow,column=3)

def keyPress(a):
    try:
        textcheck = ''.join(i for i in varSleeptime.get() if i in '0123456789')
        varSleeptime.set(int(textcheck))
    except ValueError:
        varSleeptime.set('')


def Quit():
    global Fconnet
    Fconnet = False
    root.quit()

def SaveProc():
    config.set('infoCode',str(varinfoCode.get()),str(varProc.get()))
    config.write(open(sDir, "w"))



def comboxChanged(event=None):
    if varinfoCode.get()[1:3]== '00':
        procName = config.get('infoCode',str(varinfoCode.get()))
        varProc.set(procName)




def Connet():
    WriteConfig(varIP.get(),varDateBase.get(),varUser.get(),varPaswd.get(),varWebSerIp.get(),varDBType.get(),varParkCode.get(),varSleeptime.get())


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

def IntfConnetTest(LabMess):

    Xdetail = [{"count":"1"}]
    option = varinfoCode.get()
    #{"infoCode":str(option),"scenicCode" :str(varParkCode.get()),"content":Xdetail}
    values = eval(sFormatJson)
    data = urllib.urlencode(values)
    request = urllib2.Request(varWebSerIp.get(),data) #构造Requset
    response = urllib2.urlopen(request)

    data_string = response.read()
    obj_json =  json.loads(data_string)
    Amsg = obj_json['msg']
    Asucc = obj_json['success']
    if (Amsg == varinfoCode.get()[:3]+'2') and (Asucc == True):
        LabMess['text'] = '接口正常连接。'
    else:
        LabMess['text'] = '接口连接失败。'

def StartUpLoad(LabMess):
    global  Fconnet
    if Fconnet ==False:
        LabMess['text'] = '请先连接数据库。。'

    fname = 'log'+str(datetime.date.today()) + '.txt'
    sDir = cur_file_dir() + '\\log\\'+fname

    while Fconnet==True:
        LabMess['text'] = '等待'+str(sSleepTime)+'秒..'
        time.sleep(int(sSleepTime))
        LabMess['text'] = '开始上传..'
        try:
            for option,value in config.items('infoCode'):
                if (option <> '1001') and (option[3:4]=='1') and(value <> ''):

                    if varDBType.get() == '0':
                        with open(sDir, 'a') as f:
                            f.write('select '+value+' from dual '
                                     +'\n')
                    else:
                        with open(sDir, 'a') as f:
                            f.write('DECLARE @RetMess varchar '
                                       'exec '+value+' '
                                       '@RetMess OUTPUT '
                                       'SELECT @RetMess ' +'\n')


                    if varDBType.get() == '0':
                        RES = oracle_db.select('select '+value+' as SQL from dual  ')
                        SQL = RES[0]['SQL']
                        with open(sDir, 'a') as f:
                            f.write('SQL: '+SQL +'\n')
                        SQL = SQL.replace("\n"," ")
                        RES = oracle_db.select(SQL)
                    else:
                        RES = DbIntf.exec_sp('DECLARE @RetMess varchar '
                                       'exec '+value+' '
                                       '@RetMess OUTPUT '
                                       'SELECT @RetMess ')
                        SQL = RES[0]['SQL']
                        with open(sDir, 'a') as f:
                            f.write('SQL: '+SQL +'\n')
                        SQL = SQL.replace("\n"," ")
                        RES = DbIntf.select(SQL)

                    if len(RES) > 0:
                        Tradeid = RES[0]['TRADEID']

                        Xdetail = RES

                        # {"infoCode":str(option),"scenicCode" :str(varParkCode.get()),"content":Xdetail}
                        vjson = eval(sFormatJson)

                        values = json.dumps(vjson, ensure_ascii=False,encoding='gbk')

                        if varDBType.get() == '0':
                            vjson = json.dumps(vjson, ensure_ascii=True,encoding='gbk')
                            with open(sDir, 'a') as f:
                                f.write('UpJosn:' + str(values.encode('gbk')) +'\n')
                        else:
                            vjson = values.encode('raw_unicode_escape')
                            vjson = eval(json.dumps(vjson, ensure_ascii=True,encoding='gbk'))
                            with open(sDir, 'a') as f:
                                f.write('UpJosn:' + str(values.encode('raw_unicode_escape')) +'\n')


                        LabMess['text'] = '正在上传:' +str(option) +'...'
                        time.sleep(0.5)

                        vjson = eval(vjson)
                        data = urllib.urlencode(vjson)

                        request = urllib2.Request(varWebSerIp.get(),data) #构造Requset
                        response = urllib2.urlopen(request)

                        data_string = response.read()
                        obj_json =  json.loads(data_string)
                        Amsg = obj_json['msg']
                        Asucc = obj_json['success']
                        #记录返回
                        with open(sDir, 'a') as f:
                            f.write('BackTrans:'+str(option)+':'+str(obj_json)+'\n')

                        if (Amsg == option[:3]+'2') and (Asucc == True):
                            #成功后更新
                            if config.has_option('infoCode', str(Amsg)) == True:
                                ProcName = config.get('infoCode',str(Amsg))
                                if varDBType.get() == '0':
                                    with open(sDir, 'a') as f:
                                        f.write('select '+ProcName+'('+str(Tradeid)+') from dual '+'\n')
                                else:
                                    with open(sDir, 'a') as f:
                                        f.write('DECLARE @RetMess varchar '
                                                   'exec '+ProcName+' "'+str(Tradeid)+'" '
                                                   '@RetMess OUTPUT '
                                                   'SELECT @RetMess ' +'\n')

                                if varDBType.get() == '0':
                                    RES = oracle_db.select('select '+ProcName+'('+repr(Tradeid)+') as SQL from dual  ')
                                    SQL = RES[0]['SQL']
                                    with open(sDir, 'a') as f:
                                        f.write('SQL: '+SQL +'\n')
                                    SQL = SQL.replace("\n"," ")
                                    RES = oracle_db.update(SQL)
                                else:
                                    RES = DbIntf.exec_sp('DECLARE @RetMess varchar '
                                                   'exec '+ProcName+' "'+str(Tradeid)+'",'
                                                   '@RetMess OUTPUT '
                                                   'SELECT @RetMess ')
                                    SQL = RES[0]['SQL']
                                    with open(sDir, 'a') as f:
                                        f.write('SQL: '+SQL +'\n')
                                    SQL = SQL.replace("\n"," ")
                                    RES = DbIntf.update(SQL)

                                if RES >= 1:
                                    LabMess['text'] = str(Tradeid) + '：更新成功。'
                                    time.sleep(0.5)
                                    with open(sDir, 'a') as f:
                                        f.write(str(Tradeid) + u'：更新成功。'.encode('gbk')+'\n')
                                else:
                                    LabMess['text'] = str(Tradeid) + '：更新失败。'
                                    time.sleep(0.5)
                                    with open(sDir, 'a') as f:
                                        f.write(str(Tradeid) + u'更新失败'.encode('gbk')+'\n')


                        else:
                            LabMess['text'] = option + '：传输失败。'
                            time.sleep(0.5)
                            Fconnet = False
                            with open(sDir, 'a') as f:
                                    f.write(str(option) + u'：传输失败。交易号：'.encode('gbk')+ str(Tradeid) +'\n')
                    else:
                        LabMess['text'] = option + '：没有数据需要更新。'
                        time.sleep(0.3)

        except:
            continue
            # Fconnet = False
            # return '数据提交失败'

def Thread_SaveLoad(LabMess):
    t = threading.Thread(target=StartUpLoad,args=(LabMess,))
    t.start()





center_window(600, 400)

varIP = StringVar()
varDateBase = StringVar()
varUser = StringVar()
varPaswd = StringVar()
varWebSerIp = StringVar()
varDBType   = StringVar()
varParkCode =StringVar()
varinfoCode = StringVar()
varProc     =StringVar()
varSleeptime =StringVar()

varIP.set(sIP)
varDateBase.set(sDateBase)
varUser.set(sUser)
varPaswd.set(sPassw)
varWebSerIp.set(sWebSerIp)
varDBType.set(sDBType)
varParkCode.set(sParkCode)
varinfoCode.set('')
varProc.set('')
varSleeptime.set(sSleepTime)

createWidgets()

# 设置窗口标题:
root.title('GSPostDate')
root.resizable(False, False)
# 主消息循环:


root.mainloop()