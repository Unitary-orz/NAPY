#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from scapy.all import RandMAC, RandIP, Ether, IP, sendp  # 针对性的导入函数,避免加载慢
import sys

iface = 'eth0'
if len(sys.argv) >= 2:
    iface = sys.argv[1]

packet = Ether(src=RandMAC(), dst=RandMAC()) / IP(src=RandIP(), dst=RandIP())
# loop参数循环发包
sendp(packet, loop=1)
