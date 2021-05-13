import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

cap = cv2.VideoCapture(0)

with mp_holistic.Holistic(min_detection_confidence= 0.5, min_tracking_confidence=0.5 ) as holistic:

    while cap.isOpened():

        re, frame = cap.read()
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        results = holistic.process(image)

        # fix back the color 
        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        
        # draw the face landmarks
        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS)
        
        # draw the body landmarks
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        
        # draw the left and right hand
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        


        cv2.imshow('image',image)
        cv2.imshow('frame',frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()