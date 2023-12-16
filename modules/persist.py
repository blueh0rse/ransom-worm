import subprocess


# run commands inside an opened shell
def run_command(process, command):
    process.stdin.write(command.encode())
    process.stdin.flush()


# job: create service
def run():
    next_action = ""
    data = "data"

    print("privesc module activated...")

    # create shell
    process = subprocess.Popen(
        ["bash"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    run_command(process, "\n")

    return data, next_action
