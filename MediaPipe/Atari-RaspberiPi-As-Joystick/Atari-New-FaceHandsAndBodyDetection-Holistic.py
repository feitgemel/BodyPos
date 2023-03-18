import mediapipe as mp 
import cv2
import time
import RPi.GPIO as GPIO


print("start Joystick")

mp_drwaing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

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

waitTimePressKey=0.3  
LastMove=''
fireStatus=False


cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

    while cap.isOpened():

        re, frame = cap.read()


        #scale = 75
        #w = int(frame.shape[1] * scale / 100)
        #h   = int(frame.shape[0] * scale / 100)
    
        #dim = (w,h)

        #resized = cv2.resize(frame , dim , interpolation = cv2.INTER_AREA)
        

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
            #cv2.line(image,(rightCx,rightCy),(leftCx,leftCy),(0,0,255),7)


            # Find the Nose points
            NoseCx = int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x * w)
            NoseCy = int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y * h)
            cv2.circle(image, (NoseCx,NoseCy) , 15 , (255,0,255), -1 )
            
            # find position of right hand
            K = 150

            # create rectangel zone 
            NoseX1 = NoseCx - K
            NoseY1 = NoseCy - K 
            NoseX2 = NoseCx + K
            NoseY2 = NoseCy + K

            cv2.rectangle(image,(NoseX1,NoseY1), (NoseX2,NoseY2),(0,0,255),3,lineType=cv2.LINE_4 )

            
            gapXaxis = leftCx - NoseCx
            gapYaxis = leftCy - NoseCy

            # clear the fire button
            fireStatus=False
            GPIO.output(BUTTON_PIN,GPIO.HIGH)


            # check if the hand are close == fire
            #####################################

            if rightCx > NoseX1 and rightCx < NoseX2 and leftCx>NoseX1 and leftCx< NoseX2 and rightCy>NoseY1 and rightCy<NoseY2 and leftCy>NoseY1 and leftCy<NoseY2 : 
                print("Fire")
                fireStatus=True 
                GPIO.output(UP_PIN,GPIO.HIGH)
                GPIO.output(LEFT_PIN,GPIO.HIGH)
                GPIO.output(RIGHT_PIN,GPIO.HIGH)
                GPIO.output(DOWN_PIN,GPIO.HIGH)
                GPIO.output(BUTTON_PIN,GPIO.LOW)
                cv2.rectangle(image, (50, 50), (250,150), (255, 255, 255), cv2.FILLED)
                cv2.putText(image,'Fire',(70,120), cv2.FONT_HERSHEY_COMPLEX , 2 , (0,102,0), 5 )

                

            else :

                # left / right is dominant
                if abs(gapXaxis) > abs(gapYaxis) :

                    if leftCx < NoseX1 :
                        print("go left")
                        GPIO.output(UP_PIN,GPIO.HIGH)
                        GPIO.output(LEFT_PIN,GPIO.LOW)
                        GPIO.output(RIGHT_PIN,GPIO.HIGH)
                        GPIO.output(DOWN_PIN,GPIO.HIGH)
                        GPIO.output(BUTTON_PIN,GPIO.HIGH)
                        LastMove="LEFT"
                        cv2.rectangle(image, (50, 50), (270,150), (255, 255, 255), cv2.FILLED)
                        cv2.putText(image,'LEFT',(70,120), cv2.FONT_HERSHEY_COMPLEX , 2 , (0,102,0), 5 )

                    
                    elif leftCx > NoseX2 :
                        print("go right")
                        GPIO.output(UP_PIN,GPIO.HIGH)
                        GPIO.output(LEFT_PIN,GPIO.HIGH)
                        GPIO.output(RIGHT_PIN,GPIO.LOW)
                        GPIO.output(DOWN_PIN,GPIO.HIGH)
                        GPIO.output(BUTTON_PIN,GPIO.HIGH)
                        LastMove="RIGHT"
                        cv2.rectangle(image, (50, 50), (270,150), (255, 255, 255), cv2.FILLED)
                        cv2.putText(image,'RIGHT',(70,120), cv2.FONT_HERSHEY_COMPLEX , 2 , (0,102,0), 5 )


                    else :
                        print("stop")
                        GPIO.output(UP_PIN,GPIO.HIGH)
                        GPIO.output(LEFT_PIN,GPIO.HIGH)
                        GPIO.output(RIGHT_PIN,GPIO.HIGH)
                        GPIO.output(DOWN_PIN,GPIO.HIGH)
                        GPIO.output(BUTTON_PIN,GPIO.HIGH)
                        LastMove="STOP"
                        cv2.rectangle(image, (50, 50), (250,150), (255, 255, 255), cv2.FILLED)
                        cv2.putText(image,'STOP',(70,120), cv2.FONT_HERSHEY_COMPLEX , 2 , (0,102,0), 5 )
                    

            
                # up / down is dominant               
                else :
                    if leftCy < NoseY1 :
                        print("go up")
                        GPIO.output(UP_PIN,GPIO.LOW)
                        GPIO.output(LEFT_PIN,GPIO.HIGH)
                        GPIO.output(RIGHT_PIN,GPIO.HIGH)
                        GPIO.output(DOWN_PIN,GPIO.HIGH)
                        GPIO.output(BUTTON_PIN,GPIO.HIGH)
                        LastMove="UP"
                        cv2.rectangle(image, (50, 50), (250,150), (255, 255, 255), cv2.FILLED)
                        cv2.putText(image,'UP',(70,120), cv2.FONT_HERSHEY_COMPLEX , 2 , (0,102,0), 5 )
                
                    
                    elif leftCy > NoseY2 :
                        print("go down")
                        GPIO.output(UP_PIN,GPIO.HIGH)
                        GPIO.output(LEFT_PIN,GPIO.HIGH)
                        GPIO.output(RIGHT_PIN,GPIO.HIGH)
                        GPIO.output(DOWN_PIN,GPIO.LOW)
                        GPIO.output(BUTTON_PIN,GPIO.HIGH)
                        LastMove="DOWN"
                        cv2.rectangle(image, (50, 50), (270,150), (255, 255, 255), cv2.FILLED)
                        cv2.putText(image,'DOWN',(70,120), cv2.FONT_HERSHEY_COMPLEX , 2 , (0,102,0), 5 )
                

                    else :
                        print("stop")


                    

                
        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

       
               
        cv2.imshow('image',image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()