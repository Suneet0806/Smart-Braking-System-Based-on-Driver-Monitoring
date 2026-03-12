# 😴 Smart Braking System Based on Driver Monitoring

A real-time drowsiness detection system that uses a laptop camera to monitor
eye activity and controls a Raspberry Pi-powered motor car via socket communication.
If the driver's eyes are detected as closed for too long, the car stops automatically.

---

## 🚗 How It Works

1. The **laptop** runs `server.py` which:
   - Captures live video from the webcam
   - Detects faces and eyes using dlib
   - Calculates the Eye Aspect Ratio (EAR)
   - Sends `move` or `stop` commands over WiFi

2. The **Raspberry Pi** runs `client.py` which:
   - Connects to the laptop over a socket connection
   - Receives `move` or `stop` commands
   - Controls the motors accordingly via GPIO pins

---

## 🛠️ Hardware Required

- Raspberry Pi (any model with GPIO)
- Motor driver module (L298N or similar)
- 2x DC motors
- Laptop or PC with a webcam
- Both devices connected to the same WiFi network

---

## 📁 Project Structure
```
drowsiness-detection/
│
├── server.py                            # Runs on laptop — eye detection
├── client.py                            # Runs on Raspberry Pi — motor control
├── requirements.txt                     # Required Python libraries
└── shape_predictor_68_face_landmarks.dat  # Download separately (see below)
```

---

## ⚙️ Setup & Installation

### On your Laptop (server):
1. Install dependencies:
```bash
   pip install opencv-python dlib numpy scipy imutils
```

2. Download the dlib shape predictor file:
   - Download from: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
   - Extract and place `shape_predictor_68_face_landmarks.dat` in the same folder as `server.py`

3. Find your laptop's IPv4 address:
```bash
   ipconfig   # Windows
   ifconfig   # Linux/Mac
```

### On your Raspberry Pi (client):
1. Install dependencies:
```bash
   pip install imutils scipy
```
   > `RPi.GPIO` comes pre-installed on Raspberry Pi OS

2. Open `client.py` and update this line with your laptop's IP:
```python
   LAPTOP_IP = "192.168.x.x"  # replace with your actual IP
```

---

## ▶️ Running the Project

> ⚠️ Both devices must be on the same WiFi network

**Step 1 — Run the server on your laptop first:**
```bash
python server.py
```

**Step 2 — Run the client on your Raspberry Pi:**
```bash
python client.py
```

---

## 🔌 GPIO Pin Wiring

| Motor | PIN | GPIO |
|-------|-----|------|
| Motor 1 - IN1 | 17 | BCM |
| Motor 1 - IN2 | 18 | BCM |
| Motor 2 - IN1 | 22 | BCM |
| Motor 2 - IN2 | 23 | BCM |

---

## 📊 EAR (Eye Aspect Ratio) Logic
```
EAR = (A + B) / (2 * C)

A = distance between eye landmarks 1 & 5
B = distance between eye landmarks 2 & 4
C = distance between eye landmarks 0 & 3
```

- If **EAR < 0.25** for **5 consecutive frames** → eyes are closed → `stop` command sent
- Otherwise → eyes are open → `move` command sent

---

## 📦 Requirements
```
opencv-python
dlib
numpy
scipy
imutils
RPi.GPIO
```

---

