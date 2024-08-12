import cv2 as cv
import argparse
import serial

parser = argparse.ArgumentParser()
parser.add_argument('--input', help='Path to image or video. Skip to capture frames from camera')
args = parser.parse_args()

# Load pre-trained face detection model
face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv.VideoCapture(args.input if args.input else 0)
stop_key = ord('q')

# Initialize serial connection with Arduino
ser = serial.Serial('COM3', 9600)  # Replace 'COM3' with the appropriate port

while cv.waitKey(1) < 0:
    hasFrame, frame = cap.read()
    if not hasFrame:
        cv.waitKey()
        break
    
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # If face detected, send signal to Arduino to drive motor
    if len(faces) > 0:
        ser.write(b'1')
    else:
        ser.write(b'0')
    
    for (x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    cv.imshow('Face Detection', frame)
    
    if cv.waitKey(1) & 0xFF == stop_key:
        break

cap.release()
cv.destroyAllWindows()
