from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from attendance_db import AttendanceDatabase

from win32com.client import Dispatch

def speak(str1):
    try:
        speak_engine=Dispatch("SAPI.SpVoice")
        speak_engine.Speak(str1)
    except Exception as e:
        print(f"Voice: {str1}")  # If speech fails, print instead

video=cv2.VideoCapture(0)
facedetect=cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

with open('data/names.pkl', 'rb') as w:
    LABELS=pickle.load(w)
with open('data/faces_data.pkl', 'rb') as f:
    FACES=pickle.load(f)

print('Shape of Faces matrix --> ', FACES.shape)

knn=KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

# Initialize attendance database
db = AttendanceDatabase()

imgBackground=cv2.imread("background.png")

COL_NAMES = ['NAME', 'TIME']

# Create Attendance directory if it doesn't exist
if not os.path.exists('Attendance'):
    os.makedirs('Attendance')

while True:
    ret,frame=video.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Improved face detection - works from farther distance
    faces=facedetect.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4, minSize=(60, 60))
    
    attendance = []  # Initialize attendance variable
    
    for (x,y,w,h) in faces:
        crop_img=frame[y:y+h, x:x+w, :]
        resized_img=cv2.resize(crop_img, (50,50)).flatten().reshape(1,-1)
        output=knn.predict(resized_img)
        ts=time.time()
        date=datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp=datetime.fromtimestamp(ts).strftime("%H:%M-%S")
        exist=os.path.isfile("Attendance/Attendance_" + date + ".csv")
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 1)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),2)
        cv2.rectangle(frame,(x,y-40),(x+w,y),(50,50,255),-1)
        cv2.putText(frame, str(output[0]), (x,y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 1)
        attendance=[str(output[0]), str(timestamp)]
    
    imgBackground[162:162 + 480, 55:55 + 640] = frame
    cv2.imshow("Frame",imgBackground)
    k=cv2.waitKey(1)
    
    if k==ord('o'):
        if len(attendance) > 0:  # Check if face was detected
            speak("Attendance Taken..")
            
            # Save to database
            db.add_attendance(attendance[0], date, attendance[1])
            
            # Also save to CSV (for backup)
            if exist:
                with open("Attendance/Attendance_" + date + ".csv", "a") as csvfile:
                    writer=csv.writer(csvfile)
                    writer.writerow(attendance)
            else:
                with open("Attendance/Attendance_" + date + ".csv", "a") as csvfile:
                    writer=csv.writer(csvfile)
                    writer.writerow(COL_NAMES)
                    writer.writerow(attendance)
            
            time.sleep(5)
        else:
            speak("No face detected")
    
    if k==ord('q'):
        break
video.release()
cv2.destroyAllWindows()
