import socket
import cv2
import dlib
import numpy as np
from scipy.spatial import distance as dist
from imutils import face_utils
import time

HOST = "0.0.0.0"  # listen on all interfaces
PORT = 5005
EAR_THRESHOLD = 0.25
EAR_CONSEC_FRAMES = 5
PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"


def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C + 1e-8)


def draw_eye_overlay(frame, eye_pts, color=(0, 255, 0)):
    for i in range(len(eye_pts)):
        pt1 = tuple(eye_pts[i])
        pt2 = tuple(eye_pts[(i + 1) % len(eye_pts)])
        cv2.line(frame, pt1, pt2, color, 2)
    x, y, w, h = cv2.boundingRect(eye_pts)
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 1)


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"[SERVER] Listening on {HOST}:{PORT} ...")

    conn, addr = server.accept()
    print(f"[SERVER] Client connected from {addr}")

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(PREDICTOR_PATH)

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    cap = cv2.VideoCapture(0)
    time.sleep(1.0)

    closed_counter = 0
    last_state = None

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray, 0)

            if len(faces) > 0:
                shape = predictor(gray, faces[0])
                shape = face_utils.shape_to_np(shape)

                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]

                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)
                ear = (leftEAR + rightEAR) / 2.0

                draw_eye_overlay(frame, leftEye)
                draw_eye_overlay(frame, rightEye)

                cv2.putText(frame, f"EAR: {ear:.3f}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                if ear < EAR_THRESHOLD:
                    closed_counter += 1
                else:
                    closed_counter = 0

                if closed_counter >= EAR_CONSEC_FRAMES:
                    state = "stop"
                    cv2.putText(frame, "EYES CLOSED", (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                else:
                    state = "move"
                    cv2.putText(frame, "EYES OPEN", (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            else:
                state = "stop"
                cv2.putText(frame, "NO FACE", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            if state != last_state:
                conn.sendall((state + "\n").encode("utf-8"))
                print(f"[SERVER] Sent: {state}")
                last_state = state

            cv2.imshow("EAR Drowsiness Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        cv2.destroyAllWindows()
        conn.close()
        server.close()


if __name__ == "__main__":
    main()