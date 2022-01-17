#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
from time import sleep
from script import *
import ipaddress
import time
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


def scan():
    name_print("Scan Mode")
    menu = [("ARP Scan", arpScan), ("ICMP Scan", icmpScan), ("Back", main)]
    menu_print(menu)


def attack():
    name_print("Attack Mode")

    menu = [
        ("ARP Spoof", arpSpoof),
        ("STP Attack\DOS", stpAttack),
        ("MAC Flood", main),
        ("Back", main),
    ]
    menu_print(menu)


# Scan Mode


def arpScan():
    name_print("ARP Scan")
    while True:
        print("\nEnter a network you need to scan (e:exit)")
        net = input("Network(192.168.1.0/24):")
        if net == "e" or net == "exit" or net == "q":
            scan()
        try:
            net = list(ipaddress.ip_network(net, False))
            arp_scan(net)
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


def icmpScan():
    name_print("ICMP Scan")
    while True:
        print("Enter a network you need to scan (e:exit)")
        net = input("Network(192.168.1.0/24):")
        if net == "e" or net == "exit" or net == "q":
            scan()
        try:
            net = list(ipaddress.ip_network(net, strict=False))
            icmp_scan(net)
        # 捕获Ctrl + C
        except KeyboardInterrupt:
            print("[-]Stop scan")
        except ValueError:
            print("\nEnter a network!!!!! eg:192.168.1.0/24\n")
            time.sleep(1)


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
        print(host, target, iface, vlan)
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
        if ans == "no":
            break


def stpAttack():
    name_print("STP Attack")


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