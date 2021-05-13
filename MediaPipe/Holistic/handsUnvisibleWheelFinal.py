import mediapipe as mp 
import cv2
import time
import math


from activateKeyboard import RIGHT,LEFT,UP,DOWN,SPACE
from activateKeyboard import PressKey, ReleaseKey    


rigthKeyPressed=RIGHT
leftKeyPressed=LEFT
upKeyPressed=UP
downKeyPressed=DOWN
spaceKeyPressed=SPACE

waitTimePressKey=0.8


mp_drwaing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)



with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

    while cap.isOpened():

        re, frame = cap.read()
        
        # set everything to Zero or False
        keyPressed = False
        rightPressed=False
        leftPressed=False
        upPressed=False
        downPressed=False
        spacePressed=False
        
        frame = cv2.flip(frame,1)
                
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = holistic.process(image)
        image.flags.writeable = True
       
        
        if results.pose_landmarks:
            

            h , w , c = image.shape
            
            rightCx = int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_INDEX].x * w)
            rightCy = int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_INDEX].y * h)
            cv2.circle(image, (rightCx,rightCy) , 15 , (255,0,255), -1 )
            
            leftCx = int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_INDEX].x * w)
            leftCy = int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_INDEX].y * h)
            
            cv2.circle(image, (leftCx,leftCy) , 15 , (255,0,255), -1 )
            cv2.line(image,(rightCx,rightCy),(leftCx,leftCy),(0,0,255),7)


            # Find the center points
            middlewheelx = int(abs(rightCx - leftCx) /2) + min(leftCx,rightCx)
            middlewheelY = int(abs(rightCy - leftCy) /2) + min(leftCy,rightCy)

            # find the radius , calculating the distance between the hands
            distRadius = int(math.sqrt((leftCx - rightCx)**2 + (leftCy - rightCy)**2) /2 )
            cv2.circle(image, (middlewheelx,middlewheelY) , distRadius , (0,255,0), 10 )


            # calculate the distance between the hands
            distHands = abs(rightCx - leftCx)
          

            if distHands < 900 :

                if rightCy-leftCy > 100 :
                    print('Left')
                    PressKey(leftKeyPressed) # press the left key
                    time.sleep(waitTimePressKey)
                    ReleaseKey(leftKeyPressed) # press the left key
                    
                elif leftCy-rightCy > 100:
                    print('Right')
                    PressKey(rigthKeyPressed) # press the right key
                    time.sleep(waitTimePressKey)
                    ReleaseKey(rigthKeyPressed)
                else:
                    print('straight -> release right and left ')
                    ReleaseKey(rigthKeyPressed)
                    ReleaseKey(leftKeyPressed)
                    ReleaseKey(spaceKeyPressed)

            else : # if the distance is bigger than 1500 then stop the car
                    print('Stop -> Space')
                    #print('dist',distHands)
                    PressKey(spaceKeyPressed) # press the right key
                    time.sleep(waitTimePressKey)
                    ReleaseKey(spaceKeyPressed)
                


            #cv2.rectangle(image,(rightCx,rightCy), (leftCx,leftCy),(0,255,255),3,lineType=cv2.LINE_4 )
                    

                
        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

       
               
        cv2.imshow('image',image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()