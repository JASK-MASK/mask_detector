from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np 
import imutils
import time
import cv2
import os

from datetime import datetime

def predice_mascarilla(frame, faceNet, maskNet):


    (h,w) = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(frame, 1.0, (224,224),(104.0, 177.0, 123.0))


    faceNet.setInput(blob)
    detections = faceNet.forward()
    


    faces = []
    locs = []
    preds = []

    for i in range(0, detections.shape[2]):


        confidence = detections[0,0,i,2]

        if confidence > 0.5:

            box = detections[0,0,i,3:7]*np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            (startX,startY)=(max(0, startX), max(0, startY))
            (endX, endY) = (min(w-1,endX), min(h-1,endY))

            face = frame[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224,224))
            face = img_to_array(face)
            face = preprocess_input(face)


            faces.append(face)
            locs.append((startX,startY,endX,endY))

    if len(faces) > 0:

        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)
    return(locs,preds)
prototxPath = "/home/alejandro/Escritorio/gui_app/face_detector/deploy.prototxt.txt"
weightsPath = "/home/alejandro/Escritorio/gui_app/face_detector/res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxPath, weightsPath)

maskNet = load_model("model-012.model")


print("Empezando stream de video")

vs = VideoStream(src=0).start()


while True:

    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    cv2.putText(frame,str(datetime.now()),(140,280), cv2.FONT_HERSHEY_PLAIN, 1,(255,255,255),2,cv2.LINE_AA)

    (locs, preds) = predice_mascarilla(frame, faceNet, maskNet)

    for(box, pred) in zip(locs, preds):

        (startX, startY, endX, endY) = box
        (mask, withoutMask) = pred

        label = "Mascarilla" if mask > withoutMask else "Sin Mascarilla"
        color = (0,255,0) if label == "Mascarilla" else (0,0,255)

        

        cv2.putText(frame, label, (startX, startY-5), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
        cv2.rectangle(frame, (startX, startY),(endX,endY), color, 2)
    
    cv2.imshow("Detector", frame)
    key = cv2.waitKey(1)

    if key == 27:
        break

vs.stream.release()
cv2.destroyAllWindows()