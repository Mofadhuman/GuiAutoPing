# -*- coding: UTF-8 -*-
import csv
import os
import struct
import socket
import select
import time
import sys
from sendemail import faultemail
from sendemail import recoveryemail

hostlist=[]    #用于存放专线对象字典数据列表
iplist=[]    #需要进行ping测试的IP，以列表形式保存
error=[]     #经过ping测试后不通的IP，以列表的形式保存
i=1

def gethostlist():
    with open(r"data\bin\host.csv", "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        for line in csv_reader:
            hostlist.append({'name': line[0], 'ip': line[1]})
    return hostlist
    print("本程序将要进行ping测的IP地址{0}".format(hostlist))  # 控制台打印本次程序要ping的地址

def startping(number):
    for zhandian in hostlist:
        for i in range(number):
            stat=getlinestat(zhandian["ip"])

def chesksum(data):
    """
    校验
    """
    n = len(data)
    m = n % 2
    sum = 0
    for i in range(0, n - m, 2):
        sum += (data[i]) + ((data[i + 1]) << 8)  # 传入data以每两个字节（十六进制）通过ord转十进制，第一字节在低位，第二个字节在高位
    if m:
        sum += (data[-1])
    # 将高于16位与低16位相加
    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)  # 如果还有高于16位，将继续与低16位相加
    answer = ~sum & 0xffff
    # 主机字节序转网络字节序列（参考小端序转大端序）
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

    '''
    连接套接字,并将数据发送到套接字
    '''

def raw_socket(dst_addr, imcp_packet):
    rawsocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    send_request_ping_time = time.time()
    # send data to the socket
    rawsocket.sendto(imcp_packet, (dst_addr, 80))
    return send_request_ping_time, rawsocket, dst_addr

    '''
    request ping
    '''

def request_ping(data_type, data_code, data_checksum, data_ID, data_Sequence, payload_body):
    # 把字节打包成二进制数据
    imcp_packet = struct.pack('>BBHHH32s', data_type, data_code, data_checksum, data_ID, data_Sequence, payload_body)
    icmp_chesksum = chesksum(imcp_packet)  # 获取校验和
    imcp_packet = struct.pack('>BBHHH32s', data_type, data_code, icmp_chesksum, data_ID, data_Sequence, payload_body)
    return imcp_packet

    '''
    reply ping
    '''

def reply_ping(send_request_ping_time, rawsocket, data_Sequence, timeout=2):
    while True:
        started_select = time.time()
        what_ready = select.select([rawsocket], [], [], timeout)
        wait_for_time = (time.time() - started_select)
        if what_ready[0] == []:  # Timeout
            return -1
        time_received = time.time()
        received_packet, addr = rawsocket.recvfrom(1024)
        icmpHeader = received_packet[20:28]
        type, code, checksum, packet_id, sequence = struct.unpack(
            ">BBHHH", icmpHeader
        )
        if type == 0 and sequence == data_Sequence:
            return time_received - send_request_ping_time
        timeout = timeout - wait_for_time
        if timeout <= 0:
            return -1

    '''
    实现 ping 主机/ip
    '''

def getlinestat(host):
    data_type = 8  # ICMP Echo Request
    data_code = 0  # must be zero
    data_checksum = 0  # "...with value 0 substituted for this field..."
    data_ID = 0  # Identifier
    data_Sequence = 1  # Sequence number
    payload_body = b'abcdefghijklmnopqrstuvwabcdefghi'  # data
    dst_addr = socket.gethostbyname(host)  # 将主机名转ipv4地址格式，返回以ipv4地址格式的字符串，如果主机名称是ipv4地址，则它将保持不变
    print("正在 Ping {0} [{1}] 具有 32 字节的数据:".format(host, dst_addr))
    for i in range(0, 4):
        icmp_packet = request_ping(data_type, data_code, data_checksum, data_ID, data_Sequence + i, payload_body)
        send_request_ping_time, rawsocket, addr = raw_socket(dst_addr, icmp_packet)
        times = reply_ping(send_request_ping_time, rawsocket, data_Sequence + i)
        if times > 0:
            print("来自 {0} 的回复: 字节=32 时间={1}ms".format(addr, int(times * 1000)))
            time.sleep(0.5)
            return True
        else:
            print("请求超时。")
            return False
