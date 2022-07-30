#!/bin/sh

export GOOGLE_APPLICATION_CREDENTIALS="./blindstick-340706-1d36a9c91daf.json"
sudo chmod 666 /dev/ttyAMA0
python BlindStick.py