import cv2
import pickle
import cvzone
import numpy as np

# Video feed
cap = cv2.VideoCapture('ls_desk.mp4')

with open('emptyDesk', 'rb') as f:
    posList = pickle.load(f)   
    
width, height = 150, 450

def checkParkingSpace(imgPro):
    spaceCounter = 0
    
    for pos in posList:
        x, y = pos
        imgCrop = imgPro[y:y + height, x:x + width]
        # cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        
        if count < 6000:
            color = (0, 0, 255)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 255, 0)
            thickness = 5
        
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color , thickness)
        cvzone.putTextRect(img,str(count),(x,y+height-10),scale=2,thickness=3,offset=0) 
    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
            thickness=5, offset=20, colorR=(0,0,0))
    

while True:
    
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
    
    checkParkingSpace(imgDilate)
    # for pos in posList:
    #      cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 5)

    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    # cv2.namedWindow('ImageBlur', cv2.WINDOW_NORMAL)
    # cv2.namedWindow('Imagethres', cv2.WINDOW_NORMAL)
    # cv2.imshow("ImageBlur", imgBlur)
    # cv2.imshow("Imagethres",imgMedian )
    cv2.imshow("Image", img )
    cv2.waitKey(1)