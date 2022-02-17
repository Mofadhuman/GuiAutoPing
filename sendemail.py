import smtplib
import email
config={}                      #定义一个用于存放配置参数的字典，配置项为key，配置内容为value
with open(r"data\bin\config.txt","r")as f:      #读取同文件夹下的config.txt配置文件
    list1=f.read().splitlines()         #读取配置文件并且用splitlines去换行符后将每行内容作为元素保存到列表中

for i in list1:                                 #循环列表的每一行进行转换成字典
    #使用split方法会将行字符串通过分隔符转换一个列表,列表[0]就是分隔符左边部分也就是配置项,列表[1]就是配置内容
    config[i.split("=")[0]]=i.split("=")[1]

def faultemail(name,ip):
    name=name
    ip=ip
    msg = email.message.EmailMessage() #创建一个邮件对象msg
    msg["From"] = config["From"]  #邮件的发送人
    msg["To"] = config["To"]    #邮件的接收人
    msg["Subject"] = "[故障]{0}IP:{1}故障，请处理".format(name,ip)     #邮件的标题
    msg.set_content("[故障]{0}IP:{1}故障,请处理".format(name,ip)) #邮件的内容

    #创建邮箱服务器对象，括号内为服务器地址和端口
    server = smtplib.SMTP_SSL(config['server'], config['port'])
    #创建服务器账号密码，账号就是邮箱地址，密码并非邮箱密码，第三方客户端登陆的授权码，且服务器需开启SMTP服务器
    server.login(config['From'], config['Password'])
    server.send_message(msg)  #发送邮件，括号内为邮件实例
    server.close()   #发送完后关闭服务
    print("已邮件发送到"+config["To"])

def recoveryemail(name,ip):
    ip = ip
    name = name
    msg = email.message.EmailMessage()  # 创建一个邮件对象msg
    msg["From"] = config["From"]  # 邮件的发送人
    msg["To"] = config["To"]  # 邮件的接收人
    msg["Subject"] = "[恢复]{0}IP:{1}故障已恢复".format(name,ip) # 邮件的标题
    msg.set_content("[恢复]{0}IP:{1}故障已恢复".format(name, ip))  # 邮件的内容

    # 创建邮箱服务器对象，括号内为服务器地址和端口
    server = smtplib.SMTP_SSL(config['server'], config['port'])
    # 创建服务器账号密码，账号就是邮箱地址，密码并非邮箱密码，第三方客户端登陆的授权码，且服务器需开启SMTP服务器
    server.login(config['From'], config['Password'])
    server.send_message(msg)  # 发送邮件，括号内为邮件实例
    server.close()  # 发送完后关闭服务
    print("已邮件发送到"+config["To"])
