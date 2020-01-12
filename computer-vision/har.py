# import the necessary packages
from scipy.spatial import distance as dist
from imutils import face_utils
from threading import Thread
from util.activity_tracker import ActivityTracker
import numpy as np
import playsound
import argparse
import imutils
import time
import dlib
import cv2

# Check if a point is inside a rectangle
def rect_contains(rect, point) :
    if point[0] < rect[0] :
        return False
    elif point[1] < rect[1] :
        return False
    elif point[0] > rect[2] :
        return False
    elif point[1] > rect[3] :
        return False
    return True

# Draw delaunay triangles
def draw_delaunay(img, subdiv, delaunay_color ) :
    triangleList = subdiv.getTriangleList()
    size = img.shape
    r = (0, 0, size[1], size[0])
 
    for t in triangleList :
        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])

        if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3) :         
            cv2.line(img, pt1, pt2, delaunay_color, 1)
            cv2.line(img, pt2, pt3, delaunay_color, 1)
            cv2.line(img, pt3, pt1, delaunay_color, 1)

def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])

	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])

	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)

	# return the eye aspect ratio
	return ear
 
# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold for to set off the
# alarm
EYE_AR_THRESH = 0.27
EYE_AR_CONSEC_FRAMES = 48

# initialize the frame counter as well as a boolean used to
# indicate if the alarm is going off
COUNTER = 0
ALARM_ON = False

shape_predictor_path = r"C:\Users\Stefa\Desktop\nwHacks2020\nwHacks-2020-Back-End\computer-vision\shape_predictor_68_face_landmarks.dat"

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shape_predictor_path)

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
# (nStart, nEnd) = face_utils.FACIAL_LANDMARKS_IDXS["nose_tip"]
# (cStart, cEnd) = face_utils.FACIAL_LANDMARKS_IDXS["chin"]
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
# (lmStart, lmEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_mouth_corner"]
# (rmStart, rmEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_mouth_corner"]

# start the video stream thread
print("[INFO] starting video stream thread...")
# vs = VideoStream(src=args["webcam"]).start()
cap = cv2.VideoCapture(0)
time.sleep(1.0)
last_iteration = time.time()

tracker = ActivityTracker()

# loop over frames from the video stream
while True:
	# grab the frame from the threaded video file stream, resize
	# it, and convert it to grayscale
	# channels)
	ret, frame = cap.read(0)
	# frame = imutils.resize(frame, width=450)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	size = frame.shape
	
	# detect faces in the grayscale frame
	rects = detector(gray, 0)

	# loop over the face detections
	for rect in rects:
		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)
		

		# extract the left and right eye coordinates, then use the
		# coordinates to compute the eye aspect ratio for both eyes
		image_points = np.array([
									(shape[33, :]),     # Nose tip
									(shape[8,  :]),     # Chin
									(shape[36, :]),     # Left eye left corner
									(shape[45, :]),     # Right eye right corne
									(shape[48, :]),     # Left Mouth corner
									(shape[54, :])      # Right mouth corner
								], dtype="double")
		
		many_points = np.array([(shape[i,:]) for i in range(68)], dtype="double")
								# 	(shape[0, :]),     
								# 	(shape[3, :]),     
								# 	(shape[13, :]),    
								# 	(shape[16, :]),    
								# 	(shape[29, :]),    
								# 	(shape[30, :]),    
								# 	(shape[17, :]),     
								# 	(shape[21, :]),     
								# 	(shape[26, :]),     
								# 	(shape[22, :]),     
								# 	(shape[33, :]),     # Nose tip
								# 	(shape[8,  :]),     # Chin
								# 	(shape[36, :]),     # Left eye left corner
								# 	(shape[45, :]),     # Right eye right corne
								# 	(shape[48, :]),     # Left Mouth corner
								# 	(shape[54, :])      # Right mouth corner
								# ], dtype="double")
		# 3D model points.
		model_points = np.array([
									(0.0, 0.0, 0.0),             # Nose tip
									(0.0, -330.0, -65.0),        # Chin
									(-225.0, 170.0, -135.0),     # Left eye left corner
									(225.0, 170.0, -135.0),      # Right eye right corne
									(-150.0, -150.0, -125.0),    # Left Mouth corner
									(150.0, -150.0, -125.0)      # Right mouth corner                     
								])

		# Camera internals
		focal_length = size[1]
		center = (size[1]/2, size[0]/2)
		camera_matrix = np.array(
								[[focal_length, 0, center[0]],
								[0, focal_length, center[1]],
								[0, 0, 1]], dtype = "double"
								)
		# print ("Camera Matrix :\n {0}".format(camera_matrix))

		dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion
		(success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
		# print ("Rotation Vector:\n {0}".format(rotation_vector))
		# print ("Translation Vector:\n {0}".format(translation_vector))
		
		# Project a 3D point (0, 0, 1000.0) onto the image plane.
		# We use this to draw a line sticking out of the nose
		(nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 500.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)
		
		for p in many_points:
			cv2.circle(frame, (int(p[0]), int(p[1])), 2, (0,255,0), -1)

		p1 = ( int(image_points[0][0]), int(image_points[0][1]))
		p2 = ( int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))
		
		diff = (p1[0] - p2[0], p1[1] - p2[1])
		sq_dist = diff[0] * diff[0] + diff[1] * diff[1]
		
		if sq_dist > 6000:
			tracker.start_activity("Distracted")
			cv2.putText(frame, "DISTRACTION ALERT!", (10, 60),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		else:
			tracker.start_activity("Focused")
		cv2.arrowedLine(frame, p1, p2, (0,255,0), 2) 
		
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]

		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)

		# average the eye aspect ratio together for both eyes
		ear = (leftEAR + rightEAR) / 2.0

		# check to see if the eye aspect ratio is below the blink
		# threshold, and if so, increment the blink frame counter
		if ear < EYE_AR_THRESH:
			COUNTER += 1
			if COUNTER >= EYE_AR_CONSEC_FRAMES:
				if not ALARM_ON:
					ALARM_ON = True
				tracker.start_activity("Drowsy")
				cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		else:
			tracker.start_activity("Focused")
			COUNTER = 0
			ALARM_ON = False

		# draw the computed eye aspect ratio on the frame to help
		# with debugging and setting the correct eye aspect ratio
		# thresholds and frame counters
		cv2.putText(frame, "Eye Aspect Ratio: {:.2f}".format(ear), (330, 420),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

		cv2.putText(frame, "Head Vector: {0}".format(rotation_vector), (80, 450),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

		try:
			delauney_rect = (0, 0, size[1], size[0])
			subdiv = cv2.Subdiv2D(delauney_rect)
			
			for p in many_points:
				subdiv.insert((int(p[0]), int(p[1])))
			
			draw_delaunay(frame, subdiv, (0, 100, 0))
		except:
			print("error drawing delaunay")
		
		# compute the convex hull for the left and right eye, then
		# visualize each of the eyes
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 0, 128), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 0, 128), 1)

	if time.time() - last_iteration > 1:
		tracker.print_activities()
		last_iteration = time.time()

	# show the frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
cap.release()