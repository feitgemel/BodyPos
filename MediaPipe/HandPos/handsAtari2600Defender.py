import mediapipe as mp 
import cv2
import time
#from directkeys import right_pressed,left_pressed
#from directkeys import PressKey, ReleaseKey    

from activateKeyboard import RIGHT,LEFT,UP,DOWN,SPACE
from activateKeyboard import PressKey, ReleaseKey    


#rigthKeyPressed=left_pressed
#leftKeyPressed=right_pressed


rigthKeyPressed=RIGHT
leftKeyPressed=LEFT
upKeyPressed=UP
downKeyPressed=DOWN

SpaceKeyPressed=SPACE

time.sleep(2.0)
current_key_pressed = set()



mp_drwaing = mp.solutions.drawing_utils #drawing uility - Help to render the landmarks
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080) 

# only one hand
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5,max_num_hands=1) as hands:

    while cap.isOpened():
        
        finger2TipX=0
        finger2TipY=0
        finger2BaseX=0
        finger2BaseY=0

        # set everything to Zero or False
        keyPressed = False
        rightPressed=False
        leftPressed=False
        upPressed=False
        downPressed=False
        spacePressed=False
        key_count=0
        key_pressed=0
        

        re, frame = cap.read()
        
        # Start the detecion 
         
        # change it to RGB
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        
        # flip the image
        image = cv2.flip(image, 1)
      
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        if results.multi_hand_landmarks:

            for handLMS in results.multi_hand_landmarks:
                #mpDraw.draw_landmarks(img,handLMS) # draw dots - handLMS is the hand index
                #mpDraw.draw_landmarks(img,handLMS, mpHands.HAND_CONNECTIONS) # draw connection - handLMS is the hand index
                for id , lm in enumerate(handLMS.landmark):
                    h , w , c = image.shape
                    cx , cy = int(lm.x * w) , int (lm.y * h)
                    #print (id, cx , cy)
                    

                    # check point 8 and 5 
                    # this is finger number 2 
                    # the X position of each point is right or left


                    if id == 5 : # this is base of the second finger
                        cv2.circle(image, (cx,cy) , 15 , (255,0,255), -1 )
                        #print (results.multi_handedness[0])
                        finger2BaseX=cx
                        finger2BaseY=cy

                    if id == 8 : # this is the top landmark of the second finger
                        cv2.circle(image, (cx,cy) , 15 , (255,0,255), -1 )
                        finger2TipX=cx
                        finger2TipY=cy


                    print('TipX-BaseX :',abs(finger2TipX-finger2BaseX))

                    if finger2TipX>0 and finger2BaseX>0 :
                        
                        # full finger points to the right
                        if (finger2TipX - finger2BaseX)  > 100 and abs(finger2BaseY - finger2TipY) < 100: 
                                                                            
                            # check if the finger points to right or left 
                            print('right')
                            cv2.rectangle(image, (20, 300), (270, 425), (255, 255, 0), cv2.FILLED)
                            cv2.putText(image, "Right", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                            PressKey(rigthKeyPressed) # press the key
                            rightPressed=True
                            current_key_pressed.add(rigthKeyPressed)
                            key_pressed=rigthKeyPressed
                            keyPressed = True
                            key_count=key_count+1

                        # full finger points to the left
                        if (finger2BaseX - finger2TipX)  > 100 and abs(finger2BaseY - finger2TipY) < 100: 
                        
                            print('left')
                            cv2.rectangle(image, (20, 300), (270, 425), (255, 255, 0), cv2.FILLED)
                            cv2.putText(image, "Left", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                            PressKey(leftKeyPressed)
                            key_pressed=leftKeyPressed
                            leftPressed=True
                            keyPressed = True
                            current_key_pressed.add(leftKeyPressed)
                            key_count=key_count+1

                        # fire 
                        if abs(finger2TipX - finger2BaseX ) < 130 : # -> finger fire 
                            print('Fire')
                            cv2.rectangle(image, (20, 300), (270, 425), (255, 255, 0), cv2.FILLED)
                            cv2.putText(image, "Fire", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                            PressKey(SpaceKeyPressed) # press the space key
                            spacePressed=True
                            current_key_pressed.add(SpaceKeyPressed)
                            key_pressed=SpaceKeyPressed
                            keyPressed = True
                            key_count=key_count+1

                            # stop moving right and left
                            ReleaseKey(leftKeyPressed)
                            ReleaseKey(rigthKeyPressed)
                        
                        
                        
                        if  (finger2BaseY - finger2TipY) > 150 :  # point up
                            #print('UP:', finger2BaseY - finger2TipY )
                            cv2.rectangle(image, (20, 300), (270, 425), (255, 255, 0), cv2.FILLED)
                            cv2.putText(image, "Up", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                            PressKey(upKeyPressed) # press the up key
                            upPressed=True
                            current_key_pressed.add(upKeyPressed)
                            key_pressed=upKeyPressed
                            keyPressed = True
                            key_count=key_count+1


                        if  (finger2TipY - finger2BaseY ) > 150 :  # point down
                            print('DOWN:', finger2TipY - finger2BaseY )
                            cv2.rectangle(image, (20, 300), (270, 425), (255, 255, 0), cv2.FILLED)
                            cv2.putText(image, "DOWN", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                            
                            PressKey(downKeyPressed) # press the down key
                            downPressed=True
                            current_key_pressed.add(downKeyPressed)
                            key_pressed=downKeyPressed
                            keyPressed = True
                            key_count=key_count+1

                        

        for key in current_key_pressed:
            time.sleep(0.15)
            ReleaseKey(key)
        current_key_pressed = set()


        # if not keyPressed and len(current_key_pressed) != 0:
        #     for key in current_key_pressed:
        #         ReleaseKey(key)
        #     current_key_pressed = set()
        # elif key_count==1 and len(current_key_pressed)==2:    
        #     for key in current_key_pressed:             
        #         if key_pressed!=key:
        #             ReleaseKey(key)
        #     current_key_pressed = set()
        #     for key in current_key_pressed:
        #         ReleaseKey(key)
        #     current_key_pressed = set()


        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        cv2.imshow('image',image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()