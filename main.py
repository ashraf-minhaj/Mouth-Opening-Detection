""" Detect Mouth State - Open/Closed

 author  : ashraf minhaj
 personal: ashraf_minhaj@yahoo.com

(c) Ashraf Minhaj
"""

""" install -
$ pip install opencv-contrib-python
$ pip install mediapipe
"""

# import necessary librariy(ies)
import cv2 
import mediapipe as mp 

cam = cv2.VideoCapture(0)                     # start video capture object with camera

face_mesh_detector = mp.solutions.face_mesh   # to get face mesh result and landmarks
face_mesh = face_mesh_detector.FaceMesh(max_num_faces=1, 
										min_detection_confidence=0.5, 
										min_tracking_confidence=0.5)

# variables for lips
upper_lip = 0
lower_lip = 14

upper_loc = 0
lower_loc = 0

text = ''

while True:
    ret, frame = cam.read()    # read from camera
    frame = cv2.flip(frame, 1) # mirror frame
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # change image color from BGR to RGB
    output = face_mesh.process(rgb_frame)               # output of detection
    landmark_points = output.multi_face_landmarks       # all landmark points
    # print(landmark_points)

    if landmark_points:
        frame_height, frame_width, dimension = frame.shape  # get frame things, dimension is not needed in our application

        landmarks = landmark_points[0].landmark          # get all landmark points in values                                      # if landmarks are found
        for id, landmark in enumerate(landmarks):        # use enumerate to get index and values
            x, y = landmark.x, landmark.y                # ladnmark points
            x_on_frame = int(x*frame_width)              # relative to frame width
            y_on_frame = int(y*frame_height)             # relative to frame height

            # draw point(circle) on each landmark to show (Optional) 
            if id == upper_lip:
                upper_loc = y_on_frame
                cv2.circle(img=frame, center=(x_on_frame, y_on_frame), radius = 3, color=(0,255,0))

            elif id == lower_lip:
                lower_loc = y_on_frame
                cv2.circle(img=frame, center=(x_on_frame, y_on_frame), radius = 3, color=(0,255,0))

        diff = int(lower_loc - upper_loc)
        print(diff)

        #show diff/text
        if diff > 20:
            text = 'Mouth Open'
        else:
            text = 'Mouth Closed'
        cv2.putText(img = frame, 
					text = text, 
					org = (10, 100), 
					fontFace = cv2.FONT_HERSHEY_DUPLEX, 
					fontScale = 2, 
					color = (125, 246, 55),
					thickness = 3)
            
    
    cv2.imshow('img', frame)  # show image
    # wait a little also read input
    # if q pressed, break while loop and get out
    if cv2.waitKey(1) ==ord('q'):
        break

# after the job done
cam.release()             # release camera so that other apps can use it
cv2.destroyAllWindows()   # kill all windows created by opencv