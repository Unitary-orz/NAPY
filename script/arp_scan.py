#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from scapy.all import (
    Ether,
    ARP,
    srp1)
import ipaddress
import time
import threading
import argparse
import os
import sys


def arp_request(ip_dst):
    hwdst = '00:00:00:00:00:00'
    mac_broad = 'FF:FF:FF:FF:FF:FF'  # 广播地址
    pkt = Ether(dst=mac_broad) / ARP(op=1, hwdst=hwdst, pdst=ip_dst)
    arp_rep = srp1(pkt, timeout=3, verbose=False)

    if arp_rep:
        print('[+]' + ip_dst, '-->MAC: ', arp_rep.hwsrc)  # 扫描出的MAC地址


def arp_scan(network):
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
    print('[+]complete scan time cost:%.3fs' % (stop - begin))


def main():
    # Windows下注释掉这段
    # 判断是否为root
    if os.getegid() != 0:
        print('[-]Need root user to run')
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument('network', help='eg: 192.168.1.0/24')
    args = parser.parse_args()

    try:
        network = list(ipaddress.ip_network(args.network))
        arp_scan(network)
    # 捕获输入参数错误
    except ValueError:
        parser.print_help()
    # 捕获Ctrl + C
    except KeyboardInterrupt:
        print('[-]Stop scan')


if __name__ == '__main__':
    main()
