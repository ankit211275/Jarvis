import cv2
import numpy as np

# Load pre-trained DNN face detector
model_path = "engine/auth/deploy.prototxt"
weights_path = "engine/auth/res10_300x300_ssd_iter_140000_fp16.caffemodel"
net = cv2.dnn.readNetFromCaffe(model_path, weights_path)

# Initialize face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('engine/auth/trainer/trainer.yml')

font = cv2.FONT_HERSHEY_SIMPLEX
names = ['Unknown', 'Ankit']  # Ensure names correspond to IDs

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

def start_authentication():
    """Capture video and perform face authentication."""
    # Initialize webcam
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # Set video width
    cam.set(4, 480)  # Set video height

    authenticated = False

    while True:
        ret, img = cam.read()
        if not ret:
            break

        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

        faces = detect_face_dnn(rgb_img)  # Detect faces

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, accuracy = recognizer.predict(gray_img[y:y + h, x:x + w])

            if accuracy < 100:
                id = names[id] if id < len(names) else "Unknown"
                accuracy = "  {0}%".format(round(100 - accuracy))
                if id != "Unknown":
                    authenticated = True
                    break
            else:
                id = "Unknown"
                accuracy = "  {0}%".format(round(100 - accuracy))

            cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(accuracy), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)

        k = cv2.waitKey(10) & 0xff  # Press 'ESC' to exit
        if k == 27 or authenticated:  # Exit if ESC is pressed or authentication is successful
            break

    cam.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    return authenticated

def authenticate():
    """Perform authentication and return result."""
    return start_authentication()
