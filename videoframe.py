import cv2

def saveFramestoImages(videopath,outdirName):
  vidcap = cv2.VideoCapture('assets/sarah.mp4')
  success,image = vidcap.read()
  count = 0
  success = True
  while success:
    cv2.imwrite("{}/frame{}.jpg".format(outdirName, count), image)     # save frame as JPEG file
    success,image = vidcap.read()
    print 'Read a new frame: ', success
    count += 1
saveFramestoImages('assets/cspan.mp4','frames')
saveFramestoImages('assets/sarah.mp4','framessarah')