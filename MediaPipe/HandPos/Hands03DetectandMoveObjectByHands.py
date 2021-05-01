import mediapipe as mp 
import cv2
import time

# create an overlay image. You can use any image


startTime = 0
flagZeroTime=True
flagcaptured=False



alpha = 0.4
font = cv2.FONT_HERSHEY_SIMPLEX


foregroundOriginal = cv2.imread('C:\Python-Code\BodyPos\MediaPipe\MediaPipe-Hands\Basketball-PNG-HD.png')
scale_percent = 11 # percent of original size
widthOrg = int(foregroundOriginal.shape[1] * scale_percent / 100)
heightOrg = int(foregroundOriginal.shape[0] * scale_percent / 100)
foreground = cv2.resize(foregroundOriginal,(widthOrg,heightOrg),interpolation = cv2.INTER_AREA)



forgX1=400
forgY1=400
forgX2 = forgX1 +widthOrg
forgY2 = forgY1 + heightOrg
newXWidth = widthOrg
newXHeight = heightOrg


mp_drwaing = mp.solutions.drawing_utils #drawing uility - Help to render the landmarks
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080)



with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:

    while cap.isOpened():

        re, frame = cap.read()
        frame = cv2.flip(frame,1)

        # Select the region in the background where we want to add the image and add the images using cv2.addWeighted()
       
        added_image = cv2.addWeighted(frame[forgY1:forgY2 , forgX1:forgX2],alpha,foreground[0:heightOrg,0:widthOrg,:],1-alpha,0)
        # Change the region with the result
       
        frame[forgY1:forgY2 , forgX1:forgX2] = added_image
        
        
        # Start the detecion 
        #=======================
         
        # change it to RGB
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        #rectangle for the fordground image
        #cv2.rectangle(image,(forgX1,forgY1),(forgX2,forgY2),(255,255,0),5)
        
             
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        
        thumbX=0
        thumbY=0
        fingerTipX=0
        fingerTipY=0
        
        if results.multi_hand_landmarks:

            for handLMS in results.multi_hand_landmarks:
                #mpDraw.draw_landmarks(img,handLMS) # draw dots - handLMS is the hand index
                #mpDraw.draw_landmarks(img,handLMS, mpHands.HAND_CONNECTIONS) # draw connection - handLMS is the hand index
                for id , lm in enumerate(handLMS.landmark):
                    h , w , c = image.shape
                    cx , cy = int(lm.x * w) , int (lm.y * h)
                    #print (id, cx , cy)
                    
                    
                    if id == 4 : # this is the thumb landmark
                        cv2.circle(image, (cx,cy) , 15 , (255,0,255), -1 )
                        thumbX = cx
                        thumbY = cy
                                            
                    if id == 8 : # this is the finger landmark
                        cv2.circle(image, (cx,cy) , 15 , (255,0,255), -1 )
                        fingerTipX = cx
                        fingerTipY = cy

                    if id == 12 : #Higher finger
                       cv2.circle(image, (cx,cy) , 15 , (255,0,255), -1 )
                       higherFingerX = cx
                       higherFingerY = cy 
   
                #draw a line between the fingers and a draw rectangle
                
                #cv2.line(image,(thumbX,thumbY),(fingerTipX,fingerTipY),(0,0,255),9)   
                #cv2.rectangle(image,(thumbX,thumbY),(fingerTipX,fingerTipY),(255,255,0),5)

                # if the foreground is already captured by the fingers
                
                if flagcaptured :
                    cv2.circle(image,(40,30),30, (255,0,0),-1) # red circle means it was captured 
                    cv2.putText(image,'Captured',(20,120) , cv2.FONT_HERSHEY_COMPLEX,2,(255,0,0),2,cv2.LINE_AA)
                    
                    # double check that the finger does not create a negative value
                    if fingerTipX-thumbX > 25 and thumbY-fingerTipY > 25 :
                        
                        # find the middle between the finger position
                        newXpos = int((fingerTipX-thumbX) / 2) - int(widthOrg/2)
                        newYpos = int((fingerTipY-thumbY) / 2 ) - int(heightOrg/2)

                        forgX1 = thumbX + newXpos
                        forgX2 = forgX1 + widthOrg

                        forgY1 = thumbY + newYpos
                        forgY2 = forgY1 + heightOrg 

                        #print('forgY1:forgY2 ',forgY1,':',forgY2,'  forgX1:forgX2 ',forgX1,':',forgX2,'    ','heightOrg:',heightOrg, ' widthOrg:',widthOrg)

                    # release the forground if the third finger is open (full hand)
                    # ============================================================
                    
                    if higherFingerY < forgY1 : 
                        print('release the basket')
                        print(higherFingerY)
                        print(forgY1)
                        flagcaptured=False
                
                # if the fordgound is free and not captured
                
                else:
                    if thumbX <= forgX1 and fingerTipX>= forgX2:
                    
                        if flagZeroTime :
                            startTime = time.time()
                            flagZeroTime=False
                        
                        else :
                            if time.time() - startTime > 1 :
                                print('Time to grab the logo ') 
                                flagcaptured=True
                                
                    # we can zero the calulated time for the next garbbing 
                    else :
                        flagZeroTime = True


        
        # convert the image to BGR before display
        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

        cv2.imshow('image',image)
         
        
        #cv2.imshow('frame',frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
       

cap.release()
cv2.destroyAllWindows()