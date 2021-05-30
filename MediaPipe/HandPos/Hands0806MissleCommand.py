import mediapipe as mp 
import cv2
import time
import win32gui
import numpy as np
from PIL import ImageGrab

from activateKeyboard import UP, DOWN, LEFT, RIGHT, SPACE 
from activateKeyboard import PressKey, ReleaseKey   

def getWindowsRect(windowHandle):
    
    if windowHandle > 0 :
        rect = win32gui.GetWindowRect(windowHandle)
        x1 = rect[0]
        y1 = rect[1]  
        x2 = rect[2] 
        y2 = rect[3] 
        return x1,y1,x2,y2 

mp_drwaing = mp.solutions.drawing_utils #drawing uility - Help to render the landmarks
mp_hands = mp.solutions.hands

waitTimePressKey=0.1

verticalMax = 19
horizontalMax = 9

CursurPosVertical = 8 
CursurPosHorizontal = 4

indexFingerX = 0
indexFingerY = 0
thumbTipX = 0
thumbTipY = 0


cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480) 

handle =  win32gui.FindWindow(None, 'Stella 6.5.2: "Missile Command (1981) (Atari) (Prototype)"')
                                    
#print(handle) check if the game windows was detected 

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5,max_num_hands=1) as hands:

    while cap.isOpened() and handle>0 : # if the camera is working and got the Missle command handle windows
        

        # =====================================   
        # The curser can move 19 X 10 positions
        # =====================================


        # get the position of the Missle command windows
        xPos1, yPos1 , xPos2, yPos2 = getWindowsRect(handle)
        # get the game frame from the full desktop frame
        grabImage = ImageGrab.grab()
        screen = np.array(grabImage)
        screen = cv2.cvtColor(screen,cv2.COLOR_RGB2BGR)
        gameFrame = screen[yPos1:yPos2 , xPos1:xPos2]

        hGame , wGame , cGame = gameFrame.shape
 
        re, frame = cap.read()

        
        # Start the detecion  i 
         
        # change it to RGB
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        
        # flip the image
        image = cv2.flip(image, 1)
      
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        h , w , c = image.shape

        #hProposinal = hGame / h
        #wProposinal = wGame / w

        if results.multi_hand_landmarks:

            for handLMS in results.multi_hand_landmarks:
                #mp_drwaing.draw_landmarks(image,handLMS) # draw dots - handLMS is the hand index
                #mp_drwaing.draw_landmarks(image,handLMS, mp_hands.HAND_CONNECTIONS) # draw connection - handLMS is the hand index
                for id , lm in enumerate(handLMS.landmark):
                    cx , cy = int(lm.x * w) , int (lm.y * h)
                    cxGame , cyGame = int(lm.x * wGame) , int (lm.y * hGame)
                    
                    if id == 8 : # this is the index finger tip
                        
                        cv2.circle(image, (cx,cy) , 15 , (255,0,255), -1 )
                        # put the finger tip on the game image
                        #cxGame = int(cx*wProposinal)
                        #cyGame = int(cy*hProposinal)
                        #cxGame , cyGamey = int(lm.x * wGame) , int (lm.y * hGame)
                        
                        NewVerticalPosition = int(cxGame /  wGame * 20)
                        NewHorizontalPosition = int(cyGame /  hGame * 12)

                        if NewVerticalPosition>verticalMax:
                            NewVerticalPosition=verticalMax
                        if NewVerticalPosition<1:
                            NewVerticalPosition=1
                        if NewHorizontalPosition<1:
                            NewHorizontalPosition=1
                        if NewHorizontalPosition>horizontalMax:
                            NewHorizontalPosition=horizontalMax
                                

                        
                        #print('CursurPosVertical = ',CursurPosVertical )
                        #print('NewVerticalPosition :',NewVerticalPosition)
                        
                        difvertical = NewVerticalPosition - CursurPosVertical
                        difHorizontal = NewHorizontalPosition- CursurPosHorizontal

                        #print('NewHorizontalPosition = ',NewHorizontalPosition , ' CursurPosHorizontal = ',CursurPosHorizontal)
                        #print('NewVerticalPosition = ',NewVerticalPosition , ' CursurPosVertical = ',CursurPosVertical)
                        
                        if difvertical > 0 :
                            PressKey(RIGHT)
                            time.sleep(waitTimePressKey)
                            ReleaseKey(RIGHT)
                            CursurPosVertical = CursurPosVertical + 1

                        if difvertical < 0 :
                            PressKey(LEFT)
                            time.sleep(waitTimePressKey)
                            ReleaseKey(LEFT)
                            CursurPosVertical = CursurPosVertical - 1

                        if difHorizontal < 0 :
                            PressKey(UP)
                            time.sleep(waitTimePressKey)
                            ReleaseKey(UP)
                            CursurPosHorizontal = CursurPosHorizontal - 1

                        if difHorizontal > 0 :
                            PressKey(DOWN)
                            time.sleep(waitTimePressKey)
                            ReleaseKey(DOWN)
                            CursurPosHorizontal = CursurPosHorizontal + 1
                            

                        #print(cxGame,' ',cyGame)
                        cv2.circle(gameFrame, (cxGame,cyGame) , 10 , (255,0,255), -1 )

                        indexFingerX = cxGame
                        indexFingerY = cyGame
                        
                    if id == 4 : # this is the thunmb Tip landmark
                        cv2.circle(image, (cx,cy) , 15 , (255,0,255), -1 )
                        thumbTipX = cxGame
                        thumbTipY = cyGame

                        # put the thumb tip on the game image
                        #cxGame = int(cx*wProposinal)
                        #cyGame = int(cy*hProposinal)
                        #print(cxGame,' ',cyGame)
                        cv2.circle(gameFrame, (cxGame,cyGame) , 10 , (255,0,255), -1 )


                    if abs(indexFingerX-thumbTipX) < 30 and abs(thumbTipY-indexFingerY)<30  : # trigger fire
                        PressKey(SPACE)
                        time.sleep(0.1)
                        ReleaseKey(SPACE)
                    
                    
        #if results.multi_hand_landmarks:
        #    for num, hand in enumerate(results.multi_hand_landmarks):
        #        mp_drwaing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)

        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        cv2.imshow('image',image)
        cv2.imshow('gameFrame', gameFrame)
        cv2.moveWindow('gameFrame',1200,0)
    
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()