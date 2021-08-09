import cv2
import numpy as np

color_explore = np.zeros((100,200, 3), np.uint8)
color_selected = np.zeros((100,200, 3), np.uint8)


mycolorvalues=[0,0,0]

points =  []
draw=False
erase=False
################################################################################################
# Mouse Callback function
def show_color(event, x, y, flags, param):
    global mycolorvalues
    B = img[y, x][0]
    G = img[y, x][1]
    R = img[y, x][2]

    color_explore[:] = (B,G,R)

    if event == cv2.EVENT_RBUTTONDOWN:
        mycolorvalues = [B, G, R]
        color_selected[:] = mycolorvalues
        # print('show color = ', mycolorvalues)

def draw_event(event,x,y,flags,param):
    global draw,mycolorvalues,erase

    b=int(mycolorvalues[0])
    g =int(mycolorvalues[1])
    r =int(mycolorvalues[2])


    if event== cv2.EVENT_LBUTTONDOWN:
        if draw==True:
            draw=False
        else:
            draw=True

    if draw==True:
        points.append((x, y))
        if len(points) >= 2:
            cv2.line(boardimg, points[-1], points[-2], (b, g, r),pos1)
        # cv2.imshow('image', img)

    if erase == True:
        # cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
        points.append((x, y))
        if len(points) >= 2:
            cv2.line(boardimg, points[-1], points[-2], (255, 255, 255),pos2+15)

    # elif event == cv2.EVENT_MOUSEMOVE:
    #     if draw==True:
    #         cv2.circle(boardimg, (x, y), 3,(0,0,255) , -1)
    #         points.append((x, y))
    #         if len(points) >= 2:
    #             cv2.line(boardimg, points[-1], points[-2], (b,g,r), 5)
    #         cv2.imshow('Board',boardimg)
    #         # print('draw_event = ',mycolorvalues)
    if event == cv2.EVENT_RBUTTONDOWN:
        erase = True
    if event == cv2.EVENT_RBUTTONUP:
        erase = False
    else:
        points.append((x, y))
        cv2.imshow('Board', boardimg)
##############################################################################################

def empty(a):
    pass

trackimg=np.zeros((1,400,3),np.uint8)
cv2.namedWindow('COLOR PICKER')

cv2.createTrackbar("Pen Size",'COLOR PICKER',9,15,empty)
# cv2.createTrackbar("Eraser 0FF/0N","TrackBar",0,1,empty)
cv2.createTrackbar("Eraser",'COLOR PICKER',7,15,empty)


#############################################################################################
# image window for sample image
cv2.namedWindow('COLOR PICKER')

img = cv2.imread('colortable.png')
img=cv2.resize(img,(400,600))

# mouse call back function declaration
cv2.setMouseCallback('COLOR PICKER', show_color)

boardimg = np.zeros((800,1100,3),np.uint8)
boardimg[:]= (255,255,255)
cv2.namedWindow('Board')
cv2.setMouseCallback('Board', draw_event)
#################################################################################################
#
# manualimg=cv2.imread("manual.png")
# manualimg=cv2.putText(manualimg,"PRESS ENTER KEY TO CONTINUE",(20,40),cv2.FONT_HERSHEY_PLAIN, 2,(0,0,255),1)
# cv2.imshow("Manual",manualimg)



# while loop to live update
while (1):

    cv2.putText(color_explore, "EXPLORE", (5, 15), cv2.FONT_HERSHEY_COMPLEX, .5, (255, 255, 255), 1)
    cv2.putText(color_selected, "SELECTED", (5, 15), cv2.FONT_HERSHEY_COMPLEX, .5, (255, 255, 255), 1)
    imgcolstack=np.hstack((color_explore, color_selected))
    imgstack = np.vstack((img,imgcolstack,trackimg))
    cv2.imshow('COLOR PICKER', imgstack)

    cv2.imshow('Board',boardimg)


    pos1 = cv2.getTrackbarPos("Pen Size",'COLOR PICKER' )
    pos2 = cv2.getTrackbarPos("Eraser", 'COLOR PICKER')

    k = cv2.waitKey(1) & 0xFF
    if k ==ord('q') or k ==ord('Q') :
        break

cv2.destroyAllWindows()

