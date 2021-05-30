import mediapipe as mp 
import cv2
import time
from activateKeyboard import IKEY, UKEY, OKEY, COMMAKEY, SPACE
from activateKeyboard import PressKey, ReleaseKey   


mp_drwaing = mp.solutions.drawing_utils #drawing uility - Help to render the landmarks
mp_hands = mp.solutions.hands

waitTimePressKey=0.3  
difHeight = 100


cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720) 

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5,max_num_hands=1) as hands:

    while cap.isOpened():

        re, frame = cap.read()

        
        # Start the detecion  i 
         
        # change it to RGB
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        
        # flip the image
        image = cv2.flip(image, 1)
      
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        if results.multi_hand_landmarks:

            for handLMS in results.multi_hand_landmarks:
                mp_drwaing.draw_landmarks(image,handLMS) # draw dots - handLMS is the hand index
                #mp_drwaing.draw_landmarks(image,handLMS, mp_hands.HAND_CONNECTIONS) # draw connection - handLMS is the hand index
                for id , lm in enumerate(handLMS.landmark):
                    h , w , c = image.shape
                    cx , cy = int(lm.x * w) , int (lm.y * h)
                    #print (id, cx , cy)
                    

                    if id == 4 : # this is the thumb landmark
                        cv2.circle(image, (cx,cy) , 15 , (255,0,255), -1 )
                        thumbTipX = cx
                        thumbTipY = cy
                        
                    if id == 20 : # this is the pinkeyTips landmark
                        cv2.circle(image, (cx,cy) , 15 , (255,0,255), -1 )
                        pinkeyTipX = cx
                        pinkeyTipY = cy

                    if id == 0 : # this is the wrist landmark
                        cv2.circle(image, (cx,cy) , 15 , (255,0,255), -1 )
                        wristX = cx
                        wristY = cy
                    
                    if id == 12 : # this is the middleFingerTip landmark
                        cv2.circle(image, (cx,cy) , 15 , (255,0,255), -1 )
                        middleFingerTipX = cx
                        middleFingerTipY = cy


            firePressed=False
            
            if abs(thumbTipX-pinkeyTipX) < 80 and abs(pinkeyTipX-wristX) <80 and abs(wristX-middleFingerTipX) < 80 :
                print('Fire')
                firePressed = True
                PressKey(SPACE) # press the U key
                time.sleep(waitTimePressKey)
                ReleaseKey(SPACE) # press the U key

                        
            if (wristY - middleFingerTipY) > 370 and not firePressed:
                print('Stop and Back '  )
                cv2.rectangle(image, (20, 300), (500, 425), (255, 255, 0), cv2.FILLED)
                cv2.putText(image, "Stop and Back", (20,400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                PressKey(COMMAKEY) # press the U key
                time.sleep(waitTimePressKey)
                ReleaseKey(COMMAKEY) # press the U key

            else :
                
                if (pinkeyTipY- thumbTipY) > difHeight and not firePressed:
                    print('Forward right', str(pinkeyTipY- thumbTipY) )
                    cv2.rectangle(image, (20, 300), (500, 425), (255, 255, 0), cv2.FILLED)
                    cv2.putText(image, "Forward Right", (20,400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                    PressKey(OKEY) # press the O key
                    time.sleep(waitTimePressKey)
                    ReleaseKey(OKEY) # press the O key

                if (thumbTipY - pinkeyTipY ) > difHeight and not firePressed:
                    print('Forward Left', str(thumbTipY - pinkeyTipY))
                    cv2.rectangle(image, (20, 300), (500, 425), (255, 255, 0), cv2.FILLED)
                    cv2.putText(image, "Forward Left", (20,400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                    PressKey(UKEY) # press the U key
                    time.sleep(waitTimePressKey)
                    ReleaseKey(UKEY) # press the U key
                    
                if abs(thumbTipY - pinkeyTipY) < difHeight and not firePressed:
                    print('Forward stright', str(abs(thumbTipY - pinkeyTipY)))
                    cv2.rectangle(image, (20, 300), (500, 425), (255, 255, 0), cv2.FILLED)
                    cv2.putText(image, "Forward stright", (20,400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                    PressKey(IKEY) # press the I key
                    time.sleep(waitTimePressKey)
                    ReleaseKey(IKEY) # press the I key
           

        #if results.multi_hand_landmarks:
        #    for num, hand in enumerate(results.multi_hand_landmarks):
        #        mp_drwaing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)

        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        cv2.imshow('image',image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()