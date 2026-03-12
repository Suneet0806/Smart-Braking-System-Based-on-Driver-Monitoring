# 🚗 Smart Braking System Based on Driver Monitoring

A real-time drowsiness detection system that uses a laptop camera to monitor
eye activity and automatically controls a Raspberry Pi-powered motor car via
socket communication. If the driver's eyes are detected as closed for too long,
the car stops automatically — before human error causes an accident.

---

## 👥 Team Members

| Name | GitHub Accounts |
|------|-------------|
| S Suneet | https://github.com/Suneet0806 |
| Patchipala Lokesh Sahitya | https://github.com/LokeshSahitya |
| N Trivikram | https://github.com/nakkatrivikram299-prog |
| Mithunraj T | https://github.com/mithunraj777 | 
| Monish Babu V S | https://github.com/Agent1810 |
| Kritin Panda | https://github.com/KritinSynced |

---

## 🎓 Under the Guidance of

**Prof. Lakhan Dev Sharma**
Sr. Assistant Professor, SENSE
VIT-AP University, Amaravati, Andhra Pradesh

---

## 🏫 Institution

**VIT-AP University**
G-30, Inavolu, Beside AP Secretariat,
Amaravati, Andhra Pradesh – 522241

---

## 🚗 How It Works

1. The **laptop** runs `server.py` which:
   - Captures live video from the webcam
   - Detects faces and eyes using dlib
   - Calculates the Eye Aspect Ratio (EAR) and PERCLOS
   - Sends `move` or `stop` commands over WiFi via TCP/IP socket

2. The **Raspberry Pi** runs `client.py` which:
   - Connects to the laptop over a socket connection
   - Receives `move` or `stop` commands
   - Controls the motors via GPIO pins using the L298N Motor Driver

---

## 🛠️ Hardware Required

- Raspberry Pi 3 Model B+
- L298N Motor Driver
- 4x DC Gear Motors (DIY Car Kit)
- LED Light
- Jumper Wires
- Power Bank (for Raspberry Pi)
- AA Battery Pack (for motors — isolated power system)
- Laptop with webcam

---

## 📁 Project Structure
```
smart-braking-system/
│
├── server.py                              # Runs on Laptop — EAR/drowsiness detection
├── client.py                              # Runs on Raspberry Pi — motor control
├── requirements.txt                       # Required Python libraries
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
   - Download: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
   - Extract and place the `.dat` file in the same folder as `server.py`

3. Find your laptop's IPv4 address:
```bash
   ipconfig    # Windows
   ifconfig    # Linux/Mac
```

### On your Raspberry Pi (client):
1. Install dependencies:
```bash
   pip install scipy imutils
```
   > `RPi.GPIO` comes pre-installed on Raspberry Pi OS

2. Open `client.py` and update this line with your laptop's IP:
```python
   LAPTOP_IP = "192.168.x.x"  # replace with your actual IP
```

---

## ▶️ Running the Project

> ⚠️ Both devices must be connected to the same WiFi network

**Step 1 — Run server on laptop first:**
```bash
python server.py
```

**Step 2 — Run client on Raspberry Pi:**
```bash
python client.py
```

---

## 🔌 GPIO Pin Wiring

| Motor | PIN | Mode |
|-------|-----|------|
| Motor 1 - IN1 | GPIO 17 | BCM |
| Motor 1 - IN2 | GPIO 18 | BCM |
| Motor 2 - IN1 | GPIO 22 | BCM |
| Motor 2 - IN2 | GPIO 23 | BCM |

---

## 📊 EAR (Eye Aspect Ratio) Logic
```
EAR = (||p2 - p6|| + ||p3 - p5||) / (2 × ||p1 - p4||)
```

- If **EAR < 0.25** for **5 consecutive frames** → eyes closed → `stop` sent
- Otherwise → eyes open → `move` sent
- **PERCLOS** metric used for robust fatigue detection over a time window

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

