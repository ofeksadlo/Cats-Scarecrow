import cv2
import numpy as np
from time import sleep
import sys
import os
import datetime


# Enter what class the object you're detecting will be labeled as.
classesNames = []
with open('coco.names','rt') as f:
    classesNames = f.read().rstrip('\n').split('\n')

# Change the modelConfig.cfg and modelWeights.weights to your own custom model config and weights path.
net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


    

def findObjects(outputs, img):
    global borderRect
    hT, wT, cT = img.shape
    bbox = []
    classIds = []
    confs = []

    borderX, borderY, borderW, borderH = borderRect
    x1 = borderX
    x2 = borderX + borderW
    y1 = borderY
    y2 = borderY + borderH

    predictions = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > 0.5:
                w, h = int(detection[2] * wT), int(detection[3] * hT)
                x, y = int((detection[0]*wT) - (w / 2)), int((detection[1] * hT) - (h / 2))
                bbox.append([x,y,w,h])
                classIds.append(classId)
                confs.append(float(confidence))

    indices = cv2.dnn.NMSBoxes(bbox, confs, 0.5, 0.3)
    for i in indices:
        i = i[0]
        if classesNames[classIds[i]] == 'cat':
            box = bbox[i]
            x, y, w, h = box[0], box[1], box[2], box[3]
            centerX = int(x + (w / 2))
            centerY = int(y + (h / 2))
            if centerX > x1 and centerX < x2 and centerY > y1 and centerY < y2:
                print('Cat detected on couch at: ' + datetime.datetime.now().strftime('%c'))
                cv2.putText(img, 'Cat On Couch!', (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
                cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (0,0,255), thickness=2)
                os.system('vlc --play-and-exit Sound.mp3')
            else:
                cv2.putText(img, 'Cat', (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
                cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (0,255,0), thickness=2)
            cv2.circle(img, (centerX, centerY), 7, (0,0,0), 1)
        

cap = cv2.VideoCapture(0)
ret, img = cap.read()

borderRect = cv2.selectROI('', img)

# print(borderRect)

detectedFlag = False
while True:
    
    ret, img = cap.read()

    cv2.rectangle(img, borderRect[:2], (borderRect[0] + borderRect[2], borderRect[1] + borderRect[3]), (255,0,0),2)

    blob = cv2.dnn.blobFromImage(img, 1/255, (608,608), [0,0,0],crop=False)
    net.setInput(blob)

    layerNames = net.getLayerNames()
    outputNames = []
    for i in net.getUnconnectedOutLayers():
        outputNames.append(layerNames[i[0] - 1])
    outputs = net.forward(outputNames)
    
    findObjects(outputs, img)
    cv2.rectangle(img, borderRect[:2], (borderRect[0] + borderRect[2], borderRect[1] + borderRect[3]), (255,0,0),2)
    cv2.imshow('', img)

    cv2.waitKey(1)