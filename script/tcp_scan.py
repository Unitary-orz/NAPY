#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from scapy.all import sr, IP, TCP
import time
import threading
import ipaddress


def tcp_request(ip_dst):
    ip_port = 80
    ans, unans = sr(IP(dst=ip_dst) / TCP(dport=ip_port, flags="S"), timeout=2)
    for s, r in ans:
        print("[+]" + r.sprintf("%IP.src% is alive"))


def tcp_scan(network):
    begin = time.time()
    threads = []
    length = len(network)

    for ip in network:
        scan = threading.Thread(target=arp_request, args=(str(ip),))
        threads.append(scan)

    for i in range(length):
        threads[i].start()

    for i in range(length):
        threads[i].join()

    # 计算运行时间
    stop = time.time()
    print("[+]complete scan time cost:%.3fs" % (stop - begin))
