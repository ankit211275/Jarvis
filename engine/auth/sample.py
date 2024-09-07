import cv2
import numpy as np  # Ensure numpy is imported
import os

# Load pre-trained DNN face detector
model_path = "/Users/ankit/Desktop/Jarvis/engine/auth/deploy.prototxt"
weights_path = "/Users/ankit/Desktop/Jarvis/engine/auth/res10_300x300_ssd_iter_140000_fp16.caffemodel"

net = cv2.dnn.readNetFromCaffe(model_path, weights_path)

cam = cv2.VideoCapture(0)
cam.set(3, 640)  # Set video width
cam.set(4, 480)  # Set video height

face_id = input("Enter a Numeric user ID here: ")
print("Taking samples, look at the camera...")

def detect_face_dnn(image):
    """Detect faces using DNN-based face detection."""
    h, w = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    faces = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:  # Threshold for face detection
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            faces.append((startX, startY, endX - startX, endY - startY))
    return faces

count = 0
while True:
    ret, img = cam.read()
    if not ret:
        print("Failed to capture image from webcam")
        break

    faces = detect_face_dnn(img)  # Detect faces

    for (x, y, w, h) in faces:
        count += 1
        cv2.imwrite(f"engine/auth/samples/face.{face_id}.{count}.jpg", img[y:y + h, x:x + w])
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow('image', img)
    k = cv2.waitKey(100) & 0xff
    if k == 27 or count >= 100:  # Stop when 'ESC' is pressed or 100 samples are collected
        break

cam.release()
cv2.destroyAllWindows()

print("Samples taken successfully.")
