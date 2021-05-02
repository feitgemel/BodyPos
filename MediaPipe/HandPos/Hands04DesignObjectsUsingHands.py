import mediapipe as mp 
import cv2
import time

# You can put your camera DIM here
camWidth = 1920
camHeight = 1080
roi=[0,0,0]

# read the dogs image - the image is in the GitHub repo.
dogsImageOrg = cv2.imread('C:\Python-Code\BodyPos\MediaPipe\MediaPipe-Hands\dogs3.jpg')
dogsImageOrg = cv2.resize(dogsImageOrg,(camWidth,camHeight), interpolation=cv2.INTER_AREA)

cap = cv2.VideoCapture(0)
cap.set(3,camWidth)
cap.set(4,camHeight)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

startTime = 0
flagZeroTime = True
flagCaptured = False

with mp_hands.Hands(min_detection_confidence=0.6 , min_tracking_confidence=0.5) as hands:
    

    while cap.isOpened():
        _ , frame = cap.read()

        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        #flip the image
        image = cv2.flip(image,1)

        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        dogsImage = dogsImageOrg.copy()


        if results.multi_hand_landmarks:
            for handLMS in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image,handLMS,mp_hands.HAND_CONNECTIONS)

                for id , lm in enumerate(handLMS.landmark):
                    h, w, c, = image.shape
                    cx , cy = int (lm.x * w) , int( lm.y * h)

                    if id == 4: # this is the thumb landmark
                        cv2.circle(image, (cx,cy) , 15 , (255,0,255), -1 ) # draw a circle in the camera image
                        cv2.circle(dogsImage, (cx,cy) , 15 , (255,0,255), -1 )# draw a circle in the dogs image
                        thumbX = cx
                        thumbY = cy

                    if id == 8: # this is the finger landmark
                        cv2.circle(image, (cx,cy) , 15 , (255,0,255), -1 ) # draw a circle in the camera image
                        cv2.circle(dogsImage, (cx,cy) , 15 , (255,0,255), -1 )# draw a circle in the dogs image
                        fingerTipX = cx
                        fingerTipY = cy

                    if id == 12: # this is the third landmark
                        cv2.circle(image, (cx,cy) , 15 , (255,0,255), -1 ) # draw a circle in the camera image
                        cv2.circle(dogsImage, (cx,cy) , 15 , (255,0,255), -1 )# draw a circle in the dogs image
                        thirdFongerX = cx
                        thirdFongerY = cy

                # draw a rectangle between the fingers
                cv2.rectangle(image,(thumbX,thumbY), (fingerTipX,fingerTipY), (255,255,0), 5)
                cv2.rectangle(dogsImage,(thumbX,thumbY), (fingerTipX,fingerTipY), (255,255,0), 5)

                # grab a region of interest
                if flagCaptured:
                    cv2.circle(image,(40,30),30 ,(255,0,0), -1 ) # red dot circle for indicate capture
                    cv2.putText(image,'Captured', (20,120), cv2.FONT_HERSHEY_COMPLEX,2, (255,0,0) ,2 ,cv2.LINE_AA )

                    # double check that the fingers does not create a negative or too small area
                    if fingerTipX-thumbX > 25 and thumbY-fingerTipY >25 :

                        roiHeight = ROI.shape[0]
                        roiWidth  = ROI.shape[1]

                        dogsImage[fingerTipY:fingerTipY + roiHeight , thumbX : thumbX + roiWidth ] = ROI


                    # release if the third finger is up

                    if thirdFongerY < fingerTipY:
                        print('Release the ROI')
                        dogsImage[fingerTipY:fingerTipY + roiHeight , thumbX : thumbX + roiWidth ] = ROI
                        flagCaptured=False
                        flagZeroTime=True
                        ROI = [0,0,0]
                        


                else: # if flag is not captured
                    if thumbX <= fingerTipX and thumbY >= fingerTipY :

                        if flagZeroTime :
                            startTime = time.time()
                            flagZeroTime=False
                        else:
                            if time.time() - startTime > 2 : # wait 2 seconds for capture
                                print('You grab a region of interest')
                                flagCaptured = True

                                p1X = thumbX
                                p2DeltaX = fingerTipX-thumbX

                                p2Y = fingerTipY
                                p2DeltaY = thumbY - fingerTipY

                                ROI = dogsImage[fingerTipY:p2Y+p2DeltaY , p1X : p1X + p2DeltaX]

                    else:
                        flagZeroTime=True

        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

        cv2.imshow('dogsImage',dogsImage)
        cv2.imshow('image',image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()


