# -*- coding: UTF-8 -*-
import threading
from tkinter import *
from autoping import gethostlist
from autoping import getlinestat
import time
from sendemail import faultemail,recoveryemail
from threading import *

#为了能获得线程函数的返回值，所以要改写线程类（另一个方法是设置一个全局参数接收不推荐该方法）
class MyThread(threading.Thread):
    def __init__(self,func,args=()):       #重新构造函数
        super(MyThread, self).__init__()    #继承父类的构造方法
        self.func=func                      #重写父类的构造方法，将构造参数修改
        self.args=args                      #重写父类的构造方法，省去了线程名称，并且将后面的传参指定为元祖

    def run(self):
        self.result=self.func(*self.args)   #改写run方法，用result属性去接收函数的返回值

    def get_result(self):                   #通过get_result让主进程取得线程函数的返回值
        try:
            return self.result              #返回上面保存的result，如果该函数没有返回值则返回空值
        except Exception as e:
            return None


class Application(Frame):
    def __init__(self,master=None):             #super()代表是父类的定义继承父类的构造方法
        super().__init__(master)
        self.master=master
        self.grid()                             #容器采用Grid布局
        self.creatWidget()                      #采用creaWidet函数初始布局

    def creatWidget(self):
        #定义一个标题行标签，字体为微软雅黑，48号字
        self.nametitle = Label(self, text="服务器监控自动PING测程序",font=("微软雅黑",48))
        #定义一个站点名称的表头，字体为微软雅黑，12号字
        self.namelabel = Label(self,text="站点名称",font=("微软雅黑",12))
        # 定义一个IP地址的表头，字体为微软雅黑，12号字
        self.iplabel = Label(self,text="IP地址",font=("微软雅黑",12))
        # 定义一个PING测状态的表头(打算放入指示灯图片做动态效果)，字体为微软雅黑，12号字
        self.testlabel = Label(self,text="Ping测状态",font=("微软雅黑",12))
        # 定义一个站点名称的表头(打算用于显示ping测完后的状态结果)，字体为微软雅黑，12号字
        self.resultlabel = Label(self,text="状态",font=("微软雅黑",12))
        #将主窗体分割为12行16列，标题行占1行，16列
        self.nametitle.grid(row=0,column=0,columnspan=18)
        # 将主窗体分割为12行16列，站点名称表头标签布局在第二行，第一列，占6列，约窗口宽度的1/3
        self.namelabel.grid(row=1,column=0,columnspan=6)
        #IP地址表头标签布局于第二行，紧接站点名称，在第7列，占用4列
        self.iplabel.grid(row=1,column=6,columnspan=4)
        #ping测表头标签布局于第二行，在第11列，占用4列，每列放一个指示灯图片
        self.testlabel.grid(row=1,column=10,columnspan=4)
        #状态结果头标签布局于第二行，在第15列，占用2列
        self.resultlabel.grid(row=1,column=14,columnspan=4)
        #添加设置按钮，用于以后各种设置项
        self.configbutton=Button(self,text="设        置",font=("微软雅黑",12))
        #添加开始运行按钮，用于启动ping测试
        self.startbutton = Button(self,text="开始Ping测",font=("微软雅黑",12),command=self.startp)
        #将设置按钮布局在第13行，第7列，占用两列
        self.configbutton.grid(row=12,column=6,columnspan=2)
        # 将开始运行按钮布局在第11行，第10列，占用两列
        self.startbutton.grid(row=12,column=9,columnspan=2)
        """
        定义两类全局变量，img类用于存放图片对象，图片对象必须全局变量
        当图片对象使用局部变量时候会因为函数结束后对象销户而不显示
        hostlist以列表保持所有的站点信息（列表内元素为单个站点的信息（单站点以字典形式保存））
        """
        global img,img2,img3
        img = PhotoImage(file="data\\image\\白灯202.png")
        img2 = PhotoImage(file="data\\image\\绿灯202.png")
        img3 = PhotoImage(file="data\\image\\红灯202.png")
        global hostlist
        hostlist=gethostlist()      #使用gethostlist()获取同目录内host.csv里面的站点信息
        global guzhanglist
        guzhanglist=[]
        self.stop=False
        """
        标题和表头布局完毕开始布局具体站点和内容，因站点可能较多，所以使用循环来添加和布局
        规划每个站点用一行来展示，每页显示10个站点（分页功能暂时未做）
        先用len函数取得所以站点数，确定一个要布局多少行（后面分页可以使用除以10的方法来处理）
        """
        for i in range(len(hostlist)):
            """
            因为需要批量创建组件，故使用exec方法
            exec方法可以将字符串变成执行语句
            然后通过使用字符串的格式化str.format函数来批量定义大量组件
            同时组件名变成按循环变量进行更改，便于以后对组件属性的修改
            例如第一次循环时i=0,表示第一层，则其组件名会变成“组件名0”这样的名称
            第二次循环组件名则变成“组件名1”，可达成批量创建大量组件并按规律命名
            """
            exec("self.labelzhandianmingchen%s =Label(self,text=hostlist[i][\"name\"])" % i)
            """
            组件的布局，因为第一行标题，第二行表头，第三行才是内容
            所以布局的行数因为循环数i+2,每次循环将跳到下一行
            """
            exec("self.labelzhandianmingchen%s.grid(row=i+2,column=0,columnspan=6)" % i)
            #与上面相同方法布局IP地址内容，注意在字符串内包括“等特殊字符要用转义符\来进行处理
            exec("self.labelIPdizhi%s = Label(self, text=hostlist[i][\"ip\"],)" % i)
            #IP地址从第三行第7列开始布局
            exec("self.labelIPdizhi%s.grid(row=i + 2, column=6, columnspan=4)" % i)
            """
            因为ping测状态需要放置四个指示灯，所以使用嵌套循环布局
            同时继续沿用exec的方法来进行批量创建布局
            而组件名称也变成了"组件名[i][a]"的模式
            以便日后修改相关位置的组件
            """
            for a in range(4):
                exec("self.labelpingce{0}{1} = Label(self, image=img)".format(i,a) )
                exec("self.labelpingce{0}{1}.grid(row=i+2, column=10+{1})".format(i,a) )
            #最后继续沿用exec的方法创建组后的状态结果组件
            exec("self.labelstat%s = Label(self, text=\"未ping测\")" % i)
            exec("self.labelstat%s.grid(row=i + 2, column=14, columnspan=4)" % i)
    """
    创建一个changetestlabel方法用于改变Ping测状态内的指示灯的变化
    通过改变图片来实现变化(链路正常时转绿灯，链路故障时转红灯，未评测时转白灯)
    该函数需要传递进来一个元祖（函数定义时用*stat来定义）
    传进来的*stat应最少包含三个参数的元祖
    第一个参数stat[0]为number，代表这行的第几个灯需要改变状态
    第二个参数stat[1]为stat布尔型，当链路正常时为True，当链路故障时为False
    第三个参数Stat[2]为一个站点信息（以字典形式保存），用于判断是那个站点应该在那一行
    """

    def changeresultlabel(self,result,hang):
        self.result=result
        self.hang=hang
        if self.result==0:
            exec("self.labelstat{0}[\"text\"]=\"未ping测\"".format(hang))
        elif self.result==1:
            exec("self.labelstat{0}[\"text\"]=\"ping测中\"".format(hang))
        elif self.result==2:
            exec("self.labelstat{0}[\"text\"]=\"正常\"".format(hang))
        elif self.result==3:
            exec("self.labelstat{0}[\"text\"]=\"故障(邮件已经发送)\"".format(hang))
        elif self.result==4:
            exec("self.labelstat{0}[\"text\"]=\"丢包\"".format(hang))

    def changetestlabel(self,*stat):
        self.number=stat[0]
        self.stat=stat[1]
        self.zhandian=stat[2]
        self.changeresultlabel(1,hostlist.index(self.zhandian))
        #当这个站点的链路正常时，将对应的组件"labelpingce[i][a]"的图像修改为绿灯
        if self.stat==True:
            #通过"list.index函数返回站点在全站点的列表的索引得到要修改的那一行i，然后那个灯a等于传进来的number"
            exec("self.labelpingce{0}{1}[\"image\"]=img2".format(hostlist.index(self.zhandian),self.number))
        else:
            #当链路状态故障时，将对应指示灯变成红灯
            exec("self.labelpingce{0}{1}[\"image\"]=img3".format(hostlist.index(self.zhandian), self.number))
        self.master.update()  #更新窗口的显示，必要，不用这个不会更新
    #定义一个用于开启ping测的方法关联到按钮开始运行

    def resettestlabel(self,hang):
        for i in range(4):
            exec("self.labelpingce{0}{1}[\"image\"]=img".format(hang, i))


    def startp(self):
        self.stop=False
        self.startbutton.config(text="停止运行",font=("微软雅黑",12),command=self.stopp)
        #使用循环for去一次ping测每个站点
        while True:
            if self.stop == True:
                break
            for zhandian in hostlist:
                if self.stop == True:
                    break
                a=0  #定义一个计数器a用于计算ping通的包数
                #每个站点需要ping测多次，预订ping测4次后期可改为可设置ping测次数
                for i in range(4):
                    """
                    通过getlinestat函数使用ping去获取该IP链路是否正常
                    getlinestat根据传进去的IP进行ping测试
                    链路正常时返回Ture
                    链路故障时返回False
                    获取链路状态后使用changetestlabel方法调整指示灯
                    """
                    stat=getlinestat(zhandian["ip"])
                    self.changetestlabel(i,stat,zhandian)
                    if stat==True:
                        a=a+1
                if a>3:   #通3个包以上，则认为业务正常
                    if zhandian in guzhanglist:
                        guzhanglist.remove(zhandian)
                        recoveryemail(zhandian["name"],zhandian["ip"])
                    self.changeresultlabel(2,hostlist.index(zhandian))
                    self.master.update()
                elif a>0 and a<3:  #通1-2个包，则认为业务丢包
                    self.changeresultlabel(4,hostlist.index(zhandian))
                    self.master.update()
                else:  #一个包都不通，则认为业务故障
                    if zhandian not in guzhanglist:
                        guzhanglist.append(zhandian)
                        faultemail(zhandian["name"],zhandian["ip"])
                    self.changeresultlabel(3,hostlist.index(zhandian))
                    self.master.update()
                self.resettestlabel(hostlist.index(zhandian))
                time.sleep(0.5)


    def stopp(self):
        self.stop = True
        self.startbutton.config(text="开始Ping测",font=("微软雅黑",12),command=self.startp)

if __name__=="__main__":
    tk=Tk()
    tk.title("服务器监控自动PING测程序v0.5 by魔发")
    app=Application(tk) #将容器类实例化等于初始化窗口
    tk.mainloop()