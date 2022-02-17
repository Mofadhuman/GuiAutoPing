# GuiAutoPing
一个基于python tkinter实现的服务器ping测程序<br/>
GuiAutoPing模块用于实现GUI窗口的展示<br/>
autoping模块用来实现ping服务功能以及hostlist列表的获取<br/>
sendemail模块用于实现邮件发送<br/>
data\bin目录内保存的是程序的配置文件，主要包含所有需要ping测得host信息得host.csv文件和和邮箱配置相关的config.txt文件<br/>
data\image目录保存指示灯图片<br/>
运行程序前需对config.txt中的配置项进行配置，要不会因为无法获取邮箱信息而出错<br/>
邮箱服务器以163邮箱为例
server=smtp.163.com  <br/> 
邮箱服务器端口
port=465<br/>
发送邮箱账号
From=<br/>
发送邮箱鉴权码（非邮箱密码），需发送邮箱开启IMAP/SMTP服务才可以获得
Password=<br/>
接收者邮箱
To=<br/>

