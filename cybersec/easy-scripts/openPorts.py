import sys
from scapy.all import *
ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]


def openPorts(ip):
    ans, unans = sr(IP(dst=ip)/TCP(dport=ports, flags="S"), timeout=1)
    for s, r in ans:
        if r[TCP].flags == "SA":
            print(s[TCP].dport, "is open")
        else:
            print(s[TCP].dport, "is closed")

# usage: python openPorts.py <ip>
ip = sys.argv[1]

