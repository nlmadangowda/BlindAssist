# BlindAssist
SetUp: for Raspberry Pi
1. Boot RaspberryPi wit a 64bit OS
2. set the clock speed to 2GHz
3. sudo apt update
4. sudo apt upgrade
5. pip install --upgrade google-cloud-vision
6. curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-374.0.0-linux-arm.tar.gz
7. tar -xf google-cloud-sdk-374.0.0-linux-arm.tar.gz
8. ./google-cloud-sdk/install.sh
9. ./google-cloud-sdk/bin/gcloud init
10. copy the json key to rasberry pi location.
11. export GOOGLE_APPLICATION_CREDENTIALS="/home/pi/first-geode-340815-476da4a478e6.json"
12. sudo apt install git
13. git clone https://github.com/nlmadangowda/BlindAssist.git
14. python BlindStick.py