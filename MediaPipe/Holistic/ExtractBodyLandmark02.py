import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)
# you can set your camera 
cap.set(3,1920)
cap.set(4,1080)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        re , frame = cap.read()

        # change it to RGB
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        # for best performence
        image.flags.writeable = False

        results = pose.process(image)

        image.flags.writeable = True

        # back the color 
        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

        try:
            # if we have detection
            landmarks = results.pose_landmarks.landmark

            h , w , c = image.shape
            
            # right hand
            rightCx = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].x * w)
            rightCy =  int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].y * h)
            cv2.circle(image, (rightCx,rightCy) , 15 , (255,0,255 ), -1 )

            #left hand

            leftCx = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].x * w)
            leftCy =  int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].y * h)
            cv2.circle(image, (leftCx,leftCy) , 15 , (255,0,255 ), -1 )

            # Nose
            noseCx = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * w)
            noseCy =  int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * h)
            cv2.circle(image, (noseCx,noseCy) , 15 , (255,0,255 ), -1 )

            #Lets check of the hands above the nose 
            # check if the left hand above the nose and print a message 
            if leftCy < noseCy :
                cv2.putText(image,'Left up',(leftCx,leftCy-50), cv2.FONT_HERSHEY_COMPLEX , 2 , (255,0,0), 5 )

            # check if the left hand above the nose and print a message 
            if rightCy < noseCy :
                cv2.putText(image,'Right up',(rightCx,rightCy-50), cv2.FONT_HERSHEY_COMPLEX , 2 , (255,0,0), 5 )



        except:
            pass

        cv2.imshow('image',image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()