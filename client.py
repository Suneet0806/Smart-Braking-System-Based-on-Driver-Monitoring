import socket
import RPi.GPIO as GPIO
import time

LAPTOP_IP = "192.168.x.x"  # replace with your laptop's IPv4
PORT = 5005

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

motor1_in1 = 17
motor1_in2 = 18
motor2_in1 = 22
motor2_in2 = 23

GPIO.setup(motor1_in1, GPIO.OUT)
GPIO.setup(motor1_in2, GPIO.OUT)
GPIO.setup(motor2_in1, GPIO.OUT)
GPIO.setup(motor2_in2, GPIO.OUT)


def move_motors_forward():
    GPIO.output(motor1_in1, GPIO.HIGH)
    GPIO.output(motor1_in2, GPIO.LOW)
    GPIO.output(motor2_in1, GPIO.HIGH)
    GPIO.output(motor2_in2, GPIO.LOW)


def stop_motors():
    GPIO.output(motor1_in1, GPIO.LOW)
    GPIO.output(motor1_in2, GPIO.LOW)
    GPIO.output(motor2_in1, GPIO.LOW)
    GPIO.output(motor2_in2, GPIO.LOW)


def connect():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((LAPTOP_IP, PORT))
            print("[CLIENT] Connected to server.")
            return s
        except Exception as e:
            print(f"[CLIENT] Connection failed: {e}. Retrying...")
            time.sleep(2)


def main():
    s = connect()
    buffer = b""
    try:
        while True:
            chunk = s.recv(1024)
            if not chunk:
                raise ConnectionError("Server disconnected")
            buffer += chunk
            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                cmd = line.decode().strip().lower()
                print(f"[CLIENT] Received: {cmd}")
                if cmd == "move":
                    move_motors_forward()
                elif cmd == "stop":
                    stop_motors()
    except KeyboardInterrupt:
        pass
    finally:
        stop_motors()
        GPIO.cleanup()
        s.close()


if __name__ == "__main__":
    main()
