import cv2
import time

import mediapipe
import pyautogui
capture_hands = mediapipe.solutions.hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

drawing_option=mediapipe.solutions.drawing_utils
screen_width,screen_height=pyautogui.size()  #get screen size
x1=y1=x2=y2=0
camera=cv2.VideoCapture(0)    #camera Capture front
while True:
    _,image=camera.read() #read camera
    image_height,image_width,_=image.shape  #getting image height and width
    image=cv2.flip(image,1)  #flip camera
    rgb_image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)  #convert to rgb
    output_hands=capture_hands.process(rgb_image)  #process rgb image of hands
    all_hands=output_hands.multi_hand_landmarks  #get all hands captures
    if all_hands:
        for hand in all_hands:
            drawing_option.draw_landmarks(image,hand,mediapipe.solutions.hands.HAND_CONNECTIONS)   # capturing one by one hand and draw landmarks
            for id,landmark in enumerate(hand.landmark):
                x= int(landmark.x*image_width)  #get x coordinate
                y=int (landmark.y*image_height)
                print(x,y) #print x and y coordinates
                if id==8:
                    mouse_x=int(screen_width/image_width*x) #get mouse x and y coordinates
                    mouse_y=int(screen_height/image_height*y)
                    cv2.circle(image,(x,y),3,(0,255,255))
                    pyautogui.moveTo(mouse_x,mouse_y,duration=0)
                    x1=x
                    y1=y
                if id==4:
                    x2=x
                    y2=y
                    cv2.circle(image,(x,y),3,(0,255,255))
        dist=y2-y1  #get distance between two fingers
        print(dist)
        if dist<20:
            pyautogui.click()

    cv2.imshow("Image",image)  #show camera
    key=cv2.waitKey(10) #waitkey  for single frame
    if key==27:  #if key is esc then break
        break
camera.release()  #release camera
cv2.destroyAllWindows()  #exit all windows

