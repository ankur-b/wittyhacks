import cv2
import numpy as np
import copy
import math
import time

def dir():
    cap_region_x_begin=0.6
    cap_region_y_end=0.6
    threshold = 30
    blurValue = 41
    bgSubThreshold = 50
    learningRate = 0

    isBgCaptured = 0
    triggerSwitch = False
    counter = 0
    q = []
    out = []


    def printThreshold(thr):
        print("! Changed threshold to "+str(thr))

    def removeBG(frame):
        fgmask = bgModel.apply(frame,learningRate=learningRate)
        kernel = np.ones((3, 3), np.uint8)
        fgmask = cv2.erode(fgmask, kernel, iterations=1)
        res = cv2.bitwise_and(frame, frame, mask=fgmask)
        return res

    def push(q, x):
        if len(q) < 5:
            q.append(x)
        else:
            for i in range(4):
                q[i] = q[i+1]
                q[4] = x


    camera = cv2.VideoCapture(0)
    camera.set(10,200)
    cv2.namedWindow('trackbar')
    cv2.createTrackbar('trh1', 'trackbar', threshold, 100, printThreshold)

    while camera.isOpened():
        ret, frame = camera.read()
        threshold = cv2.getTrackbarPos('trh1', 'trackbar')
        frame = cv2.bilateralFilter(frame, 5, 50, 100)
        frame = cv2.flip(frame, 1)
        cv2.rectangle(frame, (int(cap_region_x_begin * frame.shape[1]), 0),
                     (frame.shape[1], int(cap_region_y_end * frame.shape[0])), (255, 0, 0), 2)
        cv2.imshow('original', frame)

        if isBgCaptured == 1:
            img = removeBG(frame)
            img = img[0:int(cap_region_y_end * frame.shape[0]),
                        int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
            ret, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)

            thresh1 = copy.deepcopy(thresh)
            _,contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            length = len(contours)
            maxArea = -1
            if length > 0:
                c = max(contours, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                try:
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                except:
                    pass
                push (q, center)
                if len(q)==5:
                    if (q[0][0] - q[-1][0]) < -30:
                        if len(out) < 5:
                            out.append("Right")
                    elif (q[0][0] - q[-1][0]) > 30:
                        if len(out) < 5:
                            out.append("Left")
                    if abs(q[0][1] - q[-1][1]) > 60:
                        if len(out) < 5:
                            out.append("Up")
                print (out)
                if len(out) == 5:
                    return(max(out, key = out.count))
                for i in range(length):
                    temp = contours[i]
                    area = cv2.contourArea(temp)
                    if area > maxArea:
                        maxArea = area
                        ci = i

                res = contours[ci]
                hull = cv2.convexHull(res)
                drawing = np.zeros(img.shape, np.uint8)
                cv2.drawContours(drawing, [res], 0, (0, 255, 0), 2)
                cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)

            cv2.imshow('output', drawing)

        k = cv2.waitKey(10)
        if k == 27:
            break
        elif k == ord('r'):
            bgModel = None
            triggerSwitch = False
            isBgCaptured = 0
            print ('!!!Reset BackGround!!!')

        if isBgCaptured == 0:
            time.sleep(1)
            bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
            isBgCaptured = 1
            print ('Background Captured')

#result = dir()
#print(max(result, key = result.count))
