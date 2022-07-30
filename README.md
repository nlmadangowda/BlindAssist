# BlindAssist
SetUp: for Raspberry Pi
1. Boot RaspberryPi wit a 64bit OS
2. set the clock speed to 2GHz
sudo apt update
sudo apt upgrade
5. pip install --upgrade google-cloud-vision
6. curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-374.0.0-linux-arm.tar.gz
7. tar -xf google-cloud-sdk-374.0.0-linux-arm.tar.gz
8. ./google-cloud-sdk/install.sh
9. ./google-cloud-sdk/bin/gcloud init
10. copy the json key to rasberry pi location.
11. export GOOGLE_APPLICATION_CREDENTIALS="./blindstick-340706-1d36a9c91daf.json"
12. sudo apt install git
13. git clone https://github.com/nlmadangowda/BlindAssist.git
14. python BlindStick.py

sudo apt-get install espeak

reff:https://www.dexterindustries.com/howto/make-your-raspberry-pi-speak/#:~:text=To%20make%20the%20Raspberry%20Pi,which%20is%20an%20added%20plus.

sudo chmod 666 /dev/ttyAMA0
sudo chmod 777 /dev/ttyAMA0

sudo systemctl stop serial-getty@USB0.service

export GOOGLE_APPLICATION_CREDENTIALS="/home/pi/visionapi-348017-da8a228fd641.json"

Ref:
https://www.youtube.com/watch?v=p7zpfXG15ho
https://cloud.google.com/vision/docs/setup
