import mediapipe as mp 
import cv2
import time
#from activateKeyboard import IKEY, UKEY, OKEY, COMMAKEY, SPACE
#from activateKeyboard import PressKey, ReleaseKey   
# 
print("start Joystick")

import RPi.GPIO as GPIO
import time

UP_PIN = 6
LEFT_PIN = 23
RIGHT_PIN = 22
DOWN_PIN = 27
BUTTON_PIN = 12


GPIO.setmode(GPIO.BCM)
GPIO.setup(UP_PIN,GPIO.OUT)
GPIO.setup(LEFT_PIN,GPIO.OUT)
GPIO.setup(RIGHT_PIN,GPIO.OUT)
GPIO.setup(DOWN_PIN,GPIO.OUT)
GPIO.setup(BUTTON_PIN,GPIO.OUT)

# starting point - all LOW
# ========================
GPIO.output(UP_PIN,GPIO.LOW)
GPIO.output(LEFT_PIN,GPIO.LOW)
GPIO.output(RIGHT_PIN,GPIO.LOW)
GPIO.output(DOWN_PIN,GPIO.LOW)
GPIO.output(BUTTON_PIN,GPIO.LOW)


mp_drwaing = mp.solutions.drawing_utils #drawing uility - Help to render the landmarks
mp_hands = mp.solutions.hands

waitTimePressKey=0.25
pixelsdif = 100
maxHeight = 250
fireHeight = 80
LastMove=''
fireStatus=False


cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080) 

with mp_hands.Hands(min_detection_confidence=0.3, min_tracking_confidence=0.3,max_num_hands=1) as hands:

    while cap.isOpened():


       
        re, frame = cap.read()

        scale = 75
        w = int(frame.shape[1] * scale / 100)
        h   = int(frame.shape[0] * scale / 100)
    
        dim = (w,h)

        resized = cv2.resize(frame , dim , interpolation = cv2.INTER_AREA)

        
        # Start the detection : 
        # =====================
        
        # change it to RGB
        image = cv2.cvtColor(resized,cv2.COLOR_BGR2RGB)
        
        # flip the image
        image = cv2.flip(image, 1)
      
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        if results.multi_hand_landmarks:

            for handLMS in results.multi_hand_landmarks:
                #mp_drwaing.draw_landmarks(image,handLMS) # draw dots - handLMS is the hand index
                mp_drwaing.draw_landmarks(image,handLMS, mp_hands.HAND_CONNECTIONS) # draw connection - handLMS is the hand index
                for id , lm in enumerate(handLMS.landmark):
                    h , w , c = image.shape
                    cx , cy = int(lm.x * w) , int (lm.y * h)
                    #print (id, cx , cy)
                    

                    if id == 4 : # this is the thumb landmark
                        cv2.circle(image, (cx,cy) , 15 , (0,0,255), -1 )
                        thumbTipX = cx
                        thumbTipY = cy

                    if id == 8 : # this is the indexFingerTip landmark
                        cv2.circle(image, (cx,cy) , 15 , (0,0,255), -1 )
                        indexFingerTipX = cx
                        indexFingerTipY = cy
                    
                    if id == 12 : # this is the middleFingerTip landmark
                        cv2.circle(image, (cx,cy) , 15 , (0,0,255), -1 )
                        middleFingerTipX = cx
                        middleFingerTipY = cy

                    if id == 16 : # this is the ringFingerTip landmark
                        cv2.circle(image, (cx,cy) , 15 , (0,0,255), -1 )
                        ringFingerTipX = cx
                        ringFingerTipY = cy

                    if id == 20 : # this is the pinkeyTips landmark
                        cv2.circle(image, (cx,cy) , 15 , (0,0,255), -1 )
                        pinkeyTipX = cx
                        pinkeyTipY = cy

                    if id == 0 : # this is the wrist landmark
                        cv2.circle(image, (cx,cy) , 15 , (0,0,255), -1 )
                        wristX = cx
                        wristY = cy



            fireStatus=False
            GPIO.output(BUTTON_PIN,GPIO.HIGH)

            # check for fire button
            if abs(wristY-middleFingerTipY) < fireHeight and abs(wristX-middleFingerTipX) < fireHeight and abs(pinkeyTipX-thumbTipX) < fireHeight:
                fireStatus=True 
                GPIO.output(UP_PIN,GPIO.HIGH)
                GPIO.output(LEFT_PIN,GPIO.HIGH)
                GPIO.output(RIGHT_PIN,GPIO.HIGH)
                GPIO.output(DOWN_PIN,GPIO.HIGH)
                GPIO.output(BUTTON_PIN,GPIO.LOW)
                #print('FIRE')
                cv2.rectangle(image, (50, 50), (250,150), (255, 255, 255), cv2.FILLED)
                cv2.putText(image,'Fire',(70,120), cv2.FONT_HERSHEY_COMPLEX , 2 , (0,102,0), 5 )

            #Center direction
            if (wristY-middleFingerTipY >  maxHeight and fireStatus==False)  :
                print('Joystick in the center')
                GPIO.output(UP_PIN,GPIO.HIGH)
                GPIO.output(LEFT_PIN,GPIO.HIGH)
                GPIO.output(RIGHT_PIN,GPIO.HIGH)
                GPIO.output(DOWN_PIN,GPIO.HIGH)
                GPIO.output(BUTTON_PIN,GPIO.HIGH)
                LastMove="Joystick in the center"
                cv2.rectangle(image, (50, 50), (850,150), (255, 255, 255), cv2.FILLED)
                cv2.putText(image,'Joystick in the cnter',(70,120), cv2.FONT_HERSHEY_COMPLEX , 2 , (0,102,0), 5 )
                
            else :
                # check the pixele between finger tip and wrist for direction
                ydiff = wristY-indexFingerTipY
                xdiff = wristX-indexFingerTipX

                #print('xdiff:',xdiff,'   ydiff:',ydiff)
                #print(ydiff,'   ',pixelsdif)
                # check if pressed Up or Down
                if abs(ydiff) > pixelsdif :
                    if ydiff > 0 :
                        # up direction
                        GPIO.output(UP_PIN,GPIO.LOW)
                        GPIO.output(LEFT_PIN,GPIO.HIGH)
                        GPIO.output(RIGHT_PIN,GPIO.HIGH)
                        GPIO.output(DOWN_PIN,GPIO.HIGH)
                        GPIO.output(BUTTON_PIN,GPIO.HIGH)
                        LastMove="UP"
                        cv2.rectangle(image, (50, 50), (250,150), (255, 255, 255), cv2.FILLED)
                        cv2.putText(image,'UP',(70,120), cv2.FONT_HERSHEY_COMPLEX , 2 , (0,102,0), 5 )   
                    else :
                        # down direction
                        GPIO.output(UP_PIN,GPIO.HIGH)
                        GPIO.output(LEFT_PIN,GPIO.HIGH)
                        GPIO.output(RIGHT_PIN,GPIO.HIGH)
                        GPIO.output(DOWN_PIN,GPIO.LOW)
                        GPIO.output(BUTTON_PIN,GPIO.HIGH)
                        LastMove="DOWN"
                        cv2.rectangle(image, (50, 50), (270,150), (255, 255, 255), cv2.FILLED)
                        cv2.putText(image,'DOWN',(70,120), cv2.FONT_HERSHEY_COMPLEX , 2 , (0,102,0), 5 )
                    

                # check if pressed Left or Right
                if abs(xdiff) > pixelsdif :
                    if xdiff > 0:
                        # left direction
                        print('LEFT')
                        GPIO.output(UP_PIN,GPIO.HIGH)
                        GPIO.output(LEFT_PIN,GPIO.LOW)
                        GPIO.output(RIGHT_PIN,GPIO.HIGH)
                        GPIO.output(DOWN_PIN,GPIO.HIGH)
                        GPIO.output(BUTTON_PIN,GPIO.HIGH)
                        LastMove="LEFT"
                        cv2.rectangle(image, (50, 50), (270,150), (255, 255, 255), cv2.FILLED)
                        cv2.putText(image,'LEFT',(70,120), cv2.FONT_HERSHEY_COMPLEX , 2 , (0,102,0), 5 )
                    else :
                        # right direction
                        print('RIGHT')
                        GPIO.output(UP_PIN,GPIO.HIGH)
                        GPIO.output(LEFT_PIN,GPIO.HIGH)
                        GPIO.output(RIGHT_PIN,GPIO.LOW)
                        GPIO.output(DOWN_PIN,GPIO.HIGH)
                        GPIO.output(BUTTON_PIN,GPIO.HIGH)
                        LastMove="RIGHT"
                        cv2.rectangle(image, (50, 50), (270,150), (255, 255, 255), cv2.FILLED)
                        cv2.putText(image,'RIGHT',(70,120), cv2.FONT_HERSHEY_COMPLEX , 2 , (0,102,0), 5 )    

            

            




            # check for fire 

            #print("abs(wristY-middleFingerTipY)",abs(wristY-middleFingerTipY))
            #print("abs(wristX-middleFingerTipX)",abs(wristX-middleFingerTipX))
            #print("abs(pinkeyTipX-thumbTipX)",abs(pinkeyTipX-thumbTipX))


            # if abs(wristY-middleFingerTipY) < fireHeight and abs(wristX-middleFingerTipX) < fireHeight and abs(pinkeyTipX-thumbTipX) < fireHeight:
            #     fireStatus=True 
            #     GPIO.output(UP_PIN,GPIO.HIGH)
            #     GPIO.output(LEFT_PIN,GPIO.HIGH)
            #     GPIO.output(RIGHT_PIN,GPIO.HIGH)
            #     GPIO.output(DOWN_PIN,GPIO.HIGH)
            #     GPIO.output(BUTTON_PIN,GPIO.LOW)
            #     #print('FIRE')
            #     cv2.rectangle(image, (50, 50), (250,150), (255, 255, 255), cv2.FILLED)
            #     cv2.putText(image,'Fire',(70,120), cv2.FONT_HERSHEY_COMPLEX , 2 , (0,102,0), 5 )
                
            # Up direction
            # if (wristY-indexFingerTipY > difHeight  and fireStatus==False) : # and wristY-indexFingerTipY < maxHeight
            #     print (wristY-indexFingerTipY , ' ' , difHeight ,' ' , maxHeight) #print('UP')
            #     GPIO.output(UP_PIN,GPIO.LOW)
            #     GPIO.output(LEFT_PIN,GPIO.HIGH)
            #     GPIO.output(RIGHT_PIN,GPIO.HIGH)
            #     GPIO.output(DOWN_PIN,GPIO.HIGH)
            #     GPIO.output(BUTTON_PIN,GPIO.HIGH)
            #     LastMove="UP"
            #     cv2.rectangle(image, (50, 50), (250,150), (255, 255, 255), cv2.FILLED)
            #     cv2.putText(image,'UP',(70,120), cv2.FONT_HERSHEY_COMPLEX , 2 , (0,102,0), 5 )
                
            #     #print(str(wristY-middleFingerTipY))

            # # Stop direction
            # if (wristY-middleFingerTipY >  maxHeight and fireStatus==False)  :
            #     #print('STOP')
            #     GPIO.output(UP_PIN,GPIO.HIGH)
            #     GPIO.output(LEFT_PIN,GPIO.HIGH)
            #     GPIO.output(RIGHT_PIN,GPIO.HIGH)
            #     GPIO.output(DOWN_PIN,GPIO.HIGH)
            #     GPIO.output(BUTTON_PIN,GPIO.HIGH)
            #     LastMove="Joystick in the cnter"
            #     cv2.rectangle(image, (50, 50), (250,150), (255, 255, 255), cv2.FILLED)
            #     cv2.putText(image,'Joystick in the cnter',(70,120), cv2.FONT_HERSHEY_COMPLEX , 2 , (0,102,0), 5 )
                
            #     #print(str(wristY-middleFingerTipY))

            # # down direction
            # if (middleFingerTipY-wristY > difHeight and fireStatus==False)  :
            #     #print('DOWN')
            #     GPIO.output(UP_PIN,GPIO.HIGH)
            #     GPIO.output(LEFT_PIN,GPIO.HIGH)
            #     GPIO.output(RIGHT_PIN,GPIO.HIGH)
            #     GPIO.output(DOWN_PIN,GPIO.LOW)
            #     GPIO.output(BUTTON_PIN,GPIO.HIGH)
            #     LastMove="DOWN"
            #     cv2.rectangle(image, (50, 50), (270,150), (255, 255, 255), cv2.FILLED)
            #     cv2.putText(image,'DOWN',(70,120), cv2.FONT_HERSHEY_COMPLEX , 2 , (0,102,0), 5 )
            #     #print(str(middleFingerTipY-wristY ))
            
            # # left direction
            # if (wristX-middleFingerTipX > difHeight and fireStatus==False)  :
            #     #print('LEFT')
            #     GPIO.output(UP_PIN,GPIO.HIGH)
            #     GPIO.output(LEFT_PIN,GPIO.LOW)
            #     GPIO.output(RIGHT_PIN,GPIO.HIGH)
            #     GPIO.output(DOWN_PIN,GPIO.HIGH)
            #     GPIO.output(BUTTON_PIN,GPIO.HIGH)
            #     LastMove="LEFT"
            #     cv2.rectangle(image, (50, 50), (270,150), (255, 255, 255), cv2.FILLED)
            #     cv2.putText(image,'LEFT',(70,120), cv2.FONT_HERSHEY_COMPLEX , 2 , (0,102,0), 5 )

            # # right direction
            # if (middleFingerTipX-wristX > difHeight and fireStatus==False)  :
            #     #print('RIGHT')
            #     GPIO.output(UP_PIN,GPIO.HIGH)
            #     GPIO.output(LEFT_PIN,GPIO.HIGH)
            #     GPIO.output(RIGHT_PIN,GPIO.LOW)
            #     GPIO.output(DOWN_PIN,GPIO.HIGH)
            #     GPIO.output(BUTTON_PIN,GPIO.HIGH)
            #     LastMove="RIGHT"
            #     cv2.rectangle(image, (50, 50), (270,150), (255, 255, 255), cv2.FILLED)
            #     cv2.putText(image,'RIGHT',(70,120), cv2.FONT_HERSHEY_COMPLEX , 2 , (0,102,0), 5 )


        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        cv2.imshow('image',image)
        cv2.moveWindow('image',40,0)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()