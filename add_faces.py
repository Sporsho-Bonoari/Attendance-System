import cv2
import pickle
import numpy as np
import os


if not os.path.exists('data'):
    os.makedirs('data')
    print("Data directory created!")

video = cv2.VideoCapture(0)
if not video.isOpened():
    print("Error: Could not open webcam!")
    exit()


facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
if facedetect.empty():
    print("Error: Could not load Haar Cascade file!")
    print("Please ensure 'data/haarcascade_frontalface_default.xml' exists")
    video.release()
    exit()

faces_data = []
i = 0

name = input("Enter Your Name: ")
if not name.strip():
    print("Error: Name cannot be empty!")
    video.release()
    exit()

print(f"\nCollecting face data for: {name}")
print("Instructions:")
print("- Look at the camera")
print("- Move your face slightly to capture different angles")
print("- Press 'q' to quit early")
print(f"- {100} samples will be collected\n")

while True:
    ret, frame = video.read()
    if not ret:
        print("Error: Failed to capture frame!")
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Improved face detection - works from farther distance
    faces = facedetect.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4, minSize=(60, 60))
    
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50))
        if len(faces_data) <= 100 and i % 10 == 0:
            faces_data.append(resized_img)
        i = i + 1
        
        cv2.putText(frame, f"Samples: {len(faces_data)}/100", (50, 50), 
                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
    
    cv2.imshow("Face Data Collection - Press 'q' to quit", frame)
    k = cv2.waitKey(1)
    
    if k == ord('q') or len(faces_data) == 100:
        break

video.release()
cv2.destroyAllWindows()

if len(faces_data) == 0:
    print("\nError: No face data collected!")
    print("Please ensure your face is visible to the camera")
    exit()

print(f"\n{len(faces_data)} face samples collected successfully!")

faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape(len(faces_data), -1)



num_samples = len(faces_data)
if 'names.pkl' not in os.listdir('data/'):
    names = [name] * num_samples
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)
else:
    with open('data/names.pkl', 'rb') as f:
        names = pickle.load(f)
    names = names + [name] * num_samples
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)


if 'faces_data.pkl' not in os.listdir('data/'):
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces_data, f)
else:
    with open('data/faces_data.pkl', 'rb') as f:
        faces = pickle.load(f)
    faces = np.append(faces, faces_data, axis=0)
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces, f)

print(f"\nData saved successfully!")
print(f"Total samples for {name}: {num_samples}")
print(f"Data saved in 'data/' directory")