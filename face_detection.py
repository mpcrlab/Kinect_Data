import cv2
import numpy as np

cascPath = "C:/Users/mpcrl/Desktop/Kinect_Data-master/Kinect_Data-master/haarcascade_frontalface_default.xml"

def face_detection(image):
    image=np.reshape(image, [1080, 1920, 4])
    # Get user supplied values
    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)
    # Read the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )
    print("Found {0} faces!".format(len(faces)))
    return faces

    # Draw a rectangle around the faces
    #for (x, y, w, h) in faces:
     #   cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)