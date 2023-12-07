###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import requests

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

URL = "http://10.0.2.15:8000/"

def get_server_response():
    try:
        response = requests.get(URL)
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