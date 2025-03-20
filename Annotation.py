import cv2
import pickle

img = cv2.imread('custom.png')

width, height = 150, 450

try:
    with open('emptyDesk', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    with open('emptyDesk', 'wb') as f:
        pickle.dump(posList, f)

while True:
    # cv2.rectangle(img,(350,600),(200,150), (255,0,255),2)
    
    img = cv2.imread('custom.png')
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 5)

    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)             #used to fit image into display size
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)