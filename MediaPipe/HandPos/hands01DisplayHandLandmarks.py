# this is a full tutorial 
# how to detect and display hands using live camera

# first pip install media pipe 
#https://google.github.io/mediapipe/getting_started/install.html

import mediapipe as mp
import cv2


mp_drawing = mp.solutions.drawing_utils #helps to render the landmarks
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
# You can setup your camera settings
cap.set(3,1920)
cap.set(4,1080)


with mp_hands.Hands(min_detection_confidence=0.5 , min_tracking_confidence=0.5) as hands:


    while cap.isOpened():

        re, frame = cap.read()

        # start the detection
        # ===================

        # convert the image to RGB
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        # flip the image
        image = cv2.flip(image,1)

        image.flags.writeable = False

        # this is the main process
        results = hands.process(image)

        image.flags.writeable = True

        # print the results
        #print(results.multi_hand_landmarks)

        if results.multi_hand_landmarks:

            #for num, hand in enumerate(results.multi_hand_landmarks):
            #    mp_drawing.draw_landmarks(image,hand,mp_hands.HAND_CONNECTIONS)

            # lets change the colors and the dots and joits
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image,hand,mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(255,0,0),thickness=2 , circle_radius=4),
                mp_drawing.DrawingSpec(color=(0,255,255),thickness=2 , circle_radius=2))


        # recolor back the image to BGR
        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        cv2.imshow('image',image)

        if cv2.waitKey(10) & 0xff == ord('q'):
            break



cap.release()
cv2.destroyAllWindows()
