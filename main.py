#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
from time import sleep
from script import *
import ipaddress
import time
import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *


def name_print(name):
    print("\n{:-^40}\n".format(name))
    time.sleep(0.5)


def menu_print(selection):
    menu = {}

    # Add id + selection
    for i in range(len(selection)):
        id = str(i + 1)
        menu.update({id: selection[i]})

    # Add “Quit” selection
    menu.update({str(i + 2): ("Quit", quit)})

    # print(menu)
    for key in sorted(menu.keys()):
        print(key + "." + menu[key][0])

    ans = input("\nMake A Choice: ")
    menu.get(ans, [None, invalid])[1]()


def quit():
    raise KeyboardInterrupt


def invalid():
    print("INVALID CHOICE!!!!!")
    time.sleep(1)
    main()


def ip_check(address):
    try:
        network = ipaddress.ip_address(address)
    except ValueError:
        print("[-]Error:This address/netmask is invalid for IPv4:", address)
        return False
    return True


# function init


def scan():
    name_print("Scan Mode")
    menu = [
        ("ARP Scan", arpScan),
        ("ICMP Scan", icmpScan),
        ("TCP Scan", tcpScan),
        ("Back", main),
    ]
    menu_print(menu)


def attack():
    name_print("Attack Mode")

    menu = [
        ("ARP Spoof", arpSpoof),
        ("STP Spoof", stpSpoof),
        ("STP Dos", stpDos),
        ("MAC Flood", macFlood),
        ("Back", main),
    ]
    menu_print(menu)


# Scan Mode


def scan_input(mode):
    while True:
        print("\nEnter a network you need to scan (e:exit)")
        net = input("Network(192.168.1.0/24):")
        if net == "e" or net == "exit" or net == "q" or net == "quit":
            scan()
        try:
            net = list(ipaddress.ip_network(net, False))
            mode(net)
        # 捕获Ctrl + C
        except KeyboardInterrupt:
            time.sleep(1)
            print("[-]Stop scan")
        except ValueError:
            print("\nEnter a network!!!!! eg:192.168.1.0/24\n")
            time.sleep(1)
        # ans = input("Continue(y/n)?")
        # if ans == "y":
        #     continue
        # if ans == "no":
        #     break


def arpScan():
    name_print("ARP Scan")
    scan_input(arp_scan)


def icmpScan():
    name_print("ICMP Scan")
    scan_input(icmp_scan)


def tcpScan():
    name_print("TCP Scan")
    scan_input(arp_scan)


# Attack Mode


def arpSpoof():
    name_print("ARP Spoof")

    # default value
    iface_working = get_working_if().name
    router = conf.route.route("0.0.0.0")[2]

    while True:
        host = (
            input("Enter a host you need impersonate(Default:{}):".format(router))
            or router
        )
        if not ip_check(host):
            continue
        target = input("Enter a target to ARP poison(Default:None):")
        while True:
            iface = (
                input(
                    "Enter a network interface of use(Default:{}):".format(
                        iface_working
                    )
                )
                or iface_working
            )
            # print(iface, iface_working)
            if iface in get_if_list():
                break
            print("[-]Error: {} does not exist,Now interface:".format(iface))
            show_interfaces()
        vlan = input("Enter vlan hopping of use(Default:None):").split(" ")
        # print(host, target, iface, vlan)
        if vlan != [""]:
            arp_spoof(
                iface,
                target,
                host,
                vlan_own=vlan[0],
                vlan_target=vlan[1],
            )
        else:
            arp_spoof(iface, target, host)

        ans = input("Continue(y/n)?")
        if ans == "y":
            continue
        if ans == "n":
            attack()


def stpDos():
    name_print("STP DOS")

    iface_working = get_working_if().name

    while True:
        iface = (
            input("Enter a network interface of use(Default:{}):".format(iface_working))
            or iface_working
        )
        # print(iface, iface_working)
        if iface in get_if_list():
            break
        print("[-]Error: {} does not exist,Now interface:".format(iface))
        show_interfaces()
    try:
        bpdu_dos(iface)
    except KeyboardInterrupt:
        print("[+]Stop dos")
        ans = input("Continue(y/n)?")
        if ans == "y":
            stpDos()
        if ans == "n":
            attack()


def stpSpoof():
    name_print("STP Spoof")
    iface_working = get_working_if().name

    while True:
        iface = (
            input("Enter a network interface of use(Default:{}):".format(iface_working))
            or iface_working
        )
        print(iface, iface_working)
        if iface in get_if_list():
            break
        print("[-]Error: {} does not exist,Now interface:".format(iface))
        show_interfaces()
    try:
        bpdu_spoof(iface)
    except KeyboardInterrupt:
        print("\n[+]Stop spoof")
        ans = input("Continue(y/n)?")
        if ans == "y":
            stpSpoof()
        if ans == "n":
            attack()


def macFlood():
    name_print("MAC Flood")
    iface_working = get_working_if().name

    while True:
        iface = (
            input("Enter a network interface of use(Default:{}):".format(iface_working))
            or iface_working
        )
        # print(iface, iface_working)
        if iface in get_if_list():
            break
        print("[-]Error: {} does not exist,Now interface:".format(iface))
        show_interfaces()
    try:
        bpdu_dos(iface)
    except KeyboardInterrupt:
        print("[+]Stop flood")
        ans = input("Continue(y/n)?")
        if ans == "y":
            stpDos()
        if ans == "n":
            attack()


def main():
    the_logo = [
        " __  __  __  ___ ___  _____    __ ",
        "/\ \/\ \/\  _  \/\  _`\ /\ \  /\ \\",
        "\ \ `\\\\ \ \ \L\ \ \ \L\ \ `\`\\/' /",
        " \ \ , ` \ \  __ \ \ ,__/`\ `\  /'",
        "  \ \ \`\ \ \ \/\ \ \ \/   `\ \ \ ",
        "   \ \_\ \_\ \_\ \_\ \_\     \ \_\\",
        "    \/_/\/_/\/_/\/_/\/_/      \/_/",
    ]
    the_banner = [
        "   |",
        "   | Welcome to Napy",
        "   |",
        "   | https://github.com/Unitary-orz/NAPY",
        "   |",
        "   | Have fun!",
        "   |",
    ]
    for log, banner in zip(the_logo, the_banner):
        print(log + banner)

    name_print("Home")
    menu = [("Scan Mode", scan), ("Attack Mode", attack)]
    menu_print(menu)


if __name__ == "__main__":
    # menu = {"1": ("Scan", scan), "2": ("Attack", attack), "3": ("Quit", quit)}
    # while True:
    #     menu = [("Scan Mode", scan), ("Attack Mode", attack)]
    #     menu_print(menu)
    if os.geteuid() != 0:
        print("[-]Need root user to run")
        # sys.exit(1)
    try:
        main()
    except KeyboardInterrupt:
        print("\nThank you,Bye~~~~~")