#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from scapy.all import IP, ICMP, srp1, Ether
import threading
import argparse
import ipaddress
import os
import sys


# 发送ICMP请求,判断是否存活
def icmp_requset(ip_dst, iface=None):
    pkt = Ether() / IP(dst=ip_dst) / ICMP(type=8)
    req = srp1(pkt, timeout=3, verbose=False)

    if req:
        print('[+]', ip_dst, '    Host is up')


# 进行子网的多线程扫描
def icmp_scan(network):
    threads = []
    length = len(network)
    for ip in network:
        t = threading.Thread(target=icmp_requset, args=(str(ip),))
        threads.append(t)

    for i in range(length):
        threads[i].start()

    for i in range(length):
        threads[i].join()


# 参数选项
def main():
    # Windows下注释掉这段
    # 判断是否为root
    if os.getuid() != 0:
        print('[-]Need root user to run')
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument('network', help='eg:192.168.1.0/24')
    args = parser.parse_args()
    network = list(ipaddress.ip_network(args.network,strict=False))

    icmp_scan(network)


if __name__ == '__main__':
    main()
