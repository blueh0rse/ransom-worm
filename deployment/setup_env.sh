#!/bin/bash

VM_NAME="MyUbuntuVM"
ISO_PATH="/path/to/ubuntu.iso" # Replace with your actual Ubuntu ISO path
HDD_PATH="$HOME/VirtualBox VMs/$VM_NAME/$VM_NAME.vdi"
HDD_SIZE=10000 # Size in MB

# Create VM
VBoxManage createvm --name "$VM_NAME" --ostype Ubuntu_64 --register

# Set memory and network
VBoxManage modifyvm "$VM_NAME" --ioapic on
VBoxManage modifyvm "$VM_NAME" --memory 1024 --vram 128
VBoxManage modifyvm "$VM_NAME" --nic1 nat

# Create a virtual hard disk
VBoxManage createhd --filename "$HDD_PATH" --size $HDD_SIZE

# Add storage controllers
VBoxManage storagectl "$VM_NAME" --name "SATA Controller" --add sata --controller IntelAhci
VBoxManage storageattach "$VM_NAME" --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium "$HDD_PATH"
VBoxManage storagectl "$VM_NAME" --name "IDE Controller" --add ide --controller PIIX4
VBoxManage storageattach "$VM_NAME" --storagectl "IDE Controller" --port 1 --device 0 --type dvddrive --medium "$ISO_PATH"

# Start the VM
VBoxManage startvm "$VM_NAME"
