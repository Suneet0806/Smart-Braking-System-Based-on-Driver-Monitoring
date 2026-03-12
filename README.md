# Drowsiness Detection Car

A system that detects eye closure using a laptop camera and 
controls a Raspberry Pi motor car via socket communication.

## How it works
- server.py runs on the laptop and detects drowsiness using EAR
- client.py runs on the Raspberry Pi and controls the motors

## Setup
1. Download shape_predictor_68_face_landmarks.dat from dlib.net
2. Install requirements: pip install -r requirements.txt
3. Update LAPTOP_IP in client.py with your laptop's IP
4. Run server.py on laptop first, then client.py on Raspberry Pi

## Libraries
- OpenCV, dlib, imutils, scipy, RPi.GPIO
