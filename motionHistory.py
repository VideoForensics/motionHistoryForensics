#!/usr/bin/env python
import numpy as np
import cv2

MHI_DURATION = 10
DEFAULT_THRESHOLD = 32
def genVideo(start, end, inputDir):
    mhArr = []
    prev_frame = None
    timestamp = 0
    kernel = np.ones((5,5),np.uint8)
    for i in range(start, end):
        frame = cv2.imread("{}/frame{}.jpg".format(inputDir, i))
        h, w = frame.shape[:2]
        motion_history = np.zeros((h, w), np.float32)
        if (prev_frame is not None):
            frame_diff = cv2.absdiff(frame, prev_frame)
            gray_diff = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
            ret, fgmask = cv2.threshold(gray_diff, DEFAULT_THRESHOLD, 1, cv2.THRESH_BINARY)
            timestamp += 1
            # update motion history
            cv2.motempl.updateMotionHistory(fgmask, motion_history, timestamp, MHI_DURATION)
                           
            # normalize motion history
            mh = np.uint8(np.clip((motion_history-(timestamp-MHI_DURATION)) / MHI_DURATION, 0, 1)*255)
            dilation = cv2.dilate(mh,kernel,iterations = 1)
            mhArr.append(dilation)
        prev_frame = frame.copy()
    return mhArr

def makeVideo(inputArr,outputFileName, MakeColorImg=False):
    #height, width, channels = inputArr[0].shape
    height = 1280
    width = 720
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')  # 'x264' doesn't work
    out = cv2.VideoWriter('output/{}.mp4'.format(outputFileName), fourcc, 29.0, (height,width),MakeColorImg)
    for img in inputArr:
        #frame = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        out.write(img)
    out.release()

def concatVideo(inputArr1, inputArr2):
    concatArr = []
    print(len(inputArr1))
    print(len(inputArr2))
    zeroMat = np.zeros_like(cv2.cvtColor(inputArr1[0],cv2.COLOR_GRAY2RGB))
    for i in range(len(inputArr1)):
        #img = cv2.cvtColor(cv2.imread("{}/frame{}.jpg".format(inputDir, i), cv2.IMREAD_GRAYSCALE), cv2.COLOR_GRAY2RGB)
        concatImg = zeroMat.copy()
        concatImg[:,:,0] = inputArr1[i]
        concatImg[:,:,2] = inputArr2[i]
        concatArr.append(concatImg)
    return concatArr


diff1 = genVideo(2682,2787, "frames")
diff2 = genVideo(0,105, "framessarah")
makeVideo(diff1,"output1")
makeVideo(diff2,"output2")
makeVideo(concatVideo(diff1, diff2), "concat",True)
