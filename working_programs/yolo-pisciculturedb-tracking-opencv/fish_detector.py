#!/usr/bin/python3

# USAGE
# To read and write back out to video:
# python fish_detector.py --yoloconf yolov4-tiny_testing_3chan.cfg \
# 	--weights yolov4-tiny-detector_best_pisciculturedb.weights --input true \
# 	--output true
#
# To read from webcam and write back out to disk:
# python fish_detector.py --yoloconf yolov4-tiny_testing_3chan.cfg \
# 	--weights yolov4-tiny-detector_best_pisciculturedb.weights \
#	--output output/webcam_output.avi

# import the necessary packages
from numpy.core.fromnumeric import round_
from posix import times_result
from pyimagesearch.centroidtracker import CentroidTracker
from pyimagesearch.trackableobject import TrackableObject
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import glob
import os
from datetime import datetime
import csv
import pandas as pd
import statistics
# from sklearn.metrics import pairwise_distances
from scipy.spatial import distance_matrix

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-y", "--yoloconf", required=True,
	help="path to Yolo config '.cfg' file")
ap.add_argument("-w", "--weights", required=True,
	help="path to Yolo pretrained weights '.weights' file")
ap.add_argument("-i", "--input", type=str,
	help="path to optional input video file")
ap.add_argument("-o", "--output", type=str,
	help="path to optional output video file")
ap.add_argument("-c", "--confidence", type=float, default=0.4,
	help="minimum probability to filter weak detections")
ap.add_argument("-s", "--skip-frames", type=int, default=5,
	help="# of skip frames between detections")
args = vars(ap.parse_args())

# initialize the list of class labels MobileNet SSD was trained to
# detect
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

# load our serialized model from disk
print("[INFO] loading model...")
# # net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
yolo_net = cv2.dnn.readNet(args["weights"], args["yoloconf"]) ################### Yolo ###################

yolo_layer_names = yolo_net.getLayerNames() ################### Yolo ###################
yolo_output_layers = [yolo_layer_names[i[0] - 1] for i in yolo_net.getUnconnectedOutLayers()] ################### Yolo ###################
classes = ["fish"] ################### Yolo ###################
colors = np.random.uniform(0, 255, size=(len(classes), 3)) ################### Yolo ###################

# if a video path was not supplied, grab a reference to the webcam
if not args.get("input", False):
	print("[INFO] starting video stream...")
	vs_list = [VideoStream(src=0).start()]

# otherwise, grab a reference to the video file
else:
	print("[INFO] opening video file...")
	timestamp_list = []
	vid_folder_path = os.path.join(os.getcwd(),'videos') # Opening cwd and joining it with `videos` folder name
	files_in_path = glob.glob(r"{}/*.avi".format(vid_folder_path)) # This returns a list of all files ending with .avi in the path `img_folder_path`


	vs_list = []
	for i in range(len(files_in_path)):
		vs_list.append(cv2.VideoCapture(files_in_path[i]))
		try:
			print(files_in_path[i][-23:-4].replace('_', ':'))
			timestamp = datetime.strptime(files_in_path[i][-23:-4].replace('_', ':'), '%Y-%m-%d %H:%M:%S') # Timestamp corresponds to last part of the video's name
		except ValueError as e: # If video's name doesn't include timestamp
			print(f"Couldn't get timestamp because {e}")
			timestamp = datetime.now()
		timestamp_list.append(timestamp)

for j in range(len(vs_list)):
	list_traveled_x = []
	list_traveled_y = []
	list_pwdist = []
	print(f"[INFO] STARTED processing video No. {j+1}")
	vs = vs_list[j]
	# initialize the video writer (we'll instantiate later if need be)
	writer = None

	# initialize the frame dimensions (we'll set them as soon as we read
	# the first frame from the video)
	W = None
	H = None

	# instantiate our centroid tracker, then initialize a list to store
	# each of our dlib correlation trackers, followed by a dictionary to
	# map each unique object ID to a TrackableObject
	ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
	trackers = []
	trackableObjects = {}

	# initialize the total number of frames processed thus far, along
	# with the total number of objects that have moved either up or down
	totalFrames = 0
	totalDown = 0
	totalUp = 0

	# start the frames per second throughput estimator
	fps = FPS().start()

	# loop over frames from the video stream
	while True:
		# grab the next frame and handle if we are reading from either
		# VideoCapture or VideoStream
		frame = vs.read()
		frame = frame[1] if args.get("input", False) else frame

		# if we are viewing a video and we did not grab a frame then we
		# have reached the end of the video
		if args["input"] is not None and frame is None:
			break

		# resize the frame to have a maximum width of 500 pixels (the
		# less data we have, the faster we can process it), then convert
		# the frame from BGR to RGB for dlib
		frame = imutils.resize(frame, width=500)
		rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		# if the frame dimensions are empty, set them
		if W is None or H is None:
			(H, W) = frame.shape[:2]
			height, width, channels = frame.shape ################### Yolo ###################

		# if we are supposed to be writing a video to disk, initialize
		# the writer
		if args["output"] is not None and writer is None:
			fourcc = cv2.VideoWriter_fourcc(*"MJPG")
			writer = cv2.VideoWriter(f"output/processedVid_{files_in_path[j].split('/')[-1]}", fourcc, 30,
				(W, H), True)

		# initialize the current status along with our list of bounding
		# box rectangles returned by either (1) our object detector or
		# (2) the correlation trackers
		status = "Waiting"
		rects = []

		# check to see if we should run a more computationally expensive
		# object detection method to aid our tracker
		if totalFrames % args["skip_frames"] == 0:
			# set the status and initialize our new set of object trackers
			status = "Detecting"
			trackers = []

			# convert the frame to a blob and pass the blob through the
			# network and obtain the detections
			yolo_blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False) ################### Yolo ###################
			yolo_net.setInput(yolo_blob) ################### Yolo ###################
			yolo_outs = yolo_net.forward(yolo_output_layers) ################### Yolo ###################

			# Showing informations on the screen
			class_ids = []
			confidences = []
			boxes = []
			for out in yolo_outs:
				for detection in out:
					scores = detection[5:]
					class_id = np.argmax(scores)
					confidence = scores[class_id]
					if confidence > args["confidence"]:
						# Object detected
						center_x = int(detection[0] * width)
						center_y = int(detection[1] * height)
						w = int(detection[2] * width)
						h = int(detection[3] * height)

						# Rectangle coordinates
						x = int(center_x - w / 2)
						y = int(center_y - h / 2)

						boxes.append([x, y, w, h])
						confidences.append(float(confidence))
						class_ids.append(class_id)

			indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
			font = cv2.FONT_HERSHEY_PLAIN
			for i in range(len(boxes)):
				if i in indexes:
					# num_peces += 1 # Not counting for the moment
					x, y, w, h = boxes[i]
					label = str(classes[class_ids[i]])
					color = colors[class_ids[i]]
					# cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
					# cv2.putText(frame, label, (x, y + 30), font, 2, color, 2)
					(startX, startY, endX, endY) = (x, y, x + w, y + h)

					# construct a dlib rectangle object from the bounding
					# box coordinates and then start the dlib correlation
					# tracker
					tracker = dlib.correlation_tracker()
					rect = dlib.rectangle(startX, startY, endX, endY)
					tracker.start_track(rgb, rect)

					# add the tracker to our list of trackers so we can
					# utilize it during skip frames
					trackers.append(tracker)

					# Add current position so we can calculate avg (x,y) position later
					list_traveled_x.append(x)
					list_traveled_y.append(y)

		# otherwise, we should utilize our object *trackers* rather than
		# object *detectors* to obtain a higher frame processing throughput
		else:
			# loop over the trackers
			for tracker in trackers:
				# set the status of our system to be 'tracking' rather
				# than 'waiting' or 'detecting'
				status = "Tracking"

				# update the tracker and grab the updated position
				tracker.update(rgb)
				pos = tracker.get_position()

				# unpack the position object
				startX = int(pos.left())
				startY = int(pos.top())
				endX = int(pos.right())
				endY = int(pos.bottom())

				# add the bounding box coordinates to the rectangles list
				rects.append((startX, startY, endX, endY))

		# # draw a horizontal line in the center of the frame -- once an
		# # object crosses this line we will determine whether they were
		# # moving 'up' or 'down'
		# cv2.line(frame, (0, H // 2), (W, H // 2), (0, 255, 255), 2)

		# use the centroid tracker to associate the (1) old object
		# centroids with (2) the newly computed object centroids
		objects = ct.update(rects)

		objs_positions_x = []
		objs_positions_y = []
		# loop over the tracked objects
		for (objectID, centroid) in objects.items():
			# check to see if a trackable object exists for the current
			# object ID
			to = trackableObjects.get(objectID, None)

			# if there is no existing trackable object, create one
			if to is None:
				to = TrackableObject(objectID, centroid)

			# otherwise, there is a trackable object so we can utilize it
			# to determine direction
			else:
				# the difference between the y-coordinate of the *current*
				# centroid and the mean of *previous* centroids will tell
				# us in which direction the object is moving (negative for
				# 'up' and positive for 'down')
				y = [c[1] for c in to.centroids]
				direction = centroid[1] - np.mean(y)
				to.centroids.append(centroid)

				# # check to see if the object has been counted or not
				# if not to.counted:
				# 	# if the direction is negative (indicating the object
				# 	# is moving up) AND the centroid is above the center
				# 	# line, count the object
				# 	if direction < 0 and centroid[1] < H // 2:
				# 		totalUp += 1
				# 		to.counted = True

				# 	# if the direction is positive (indicating the object
				# 	# is moving down) AND the centroid is below the
				# 	# center line, count the object
				# 	elif direction > 0 and centroid[1] > H // 2:
				# 		totalDown += 1
				# 		to.counted = True

			# store the trackable object in our dictionary
			trackableObjects[objectID] = to
			
			# Calculate average traveled distance
			avg_dist = statistics.mean( ct.traveledDistances.values() )
			# print(f"Traveled distance avg: {avg_dist}")

			# draw both the ID of the object and the centroid of the
			# object on the output frame
			text = "ID {}".format(objectID)
			cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
			cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

			# Saving all positions so we can calculate avg pairwise distance later
			objs_positions_x.append([centroid[0], centroid[1]])
			# objs_positions_y.append(centroid[1])

		try:
			objs_positions_x = np.array(objs_positions_x)
			objs_positions_y = np.array(objs_positions_y)
			current_pwdist = np.mean( distance_matrix(objs_positions_x, objs_positions_x) ) # Obtaining distances matrix and calculating mean
			list_pwdist.append(current_pwdist) # Saving current avg pwdist so we can calculate average again later
		except ValueError as e:
			print(f'No objects detected to calculate pairwise distances yet. ({e})... Skipping frame')

		# # construct a tuple of information we will be displaying on the
		# # frame
		# info = [
		# 	("Up", totalUp),
		# 	("Down", totalDown),
		# 	("Status", status),
		# ]

		# # loop over the info tuples and draw them on our frame
		# for (i, (k, v)) in enumerate(info):
		# 	text = "{}: {}".format(k, v)
		# 	cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
		# 		cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

		# check to see if we should write the frame to disk
		if writer is not None:
			writer.write(frame)

		# show the output frame
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

		# increment the total number of frames processed thus far and
		# then update the FPS counter
		totalFrames += 1
		fps.update()

	# stop the timer and display FPS information
	fps.stop()
	print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

	# check to see if we need to release the video writer pointer
	if writer is not None:
		writer.release()

	# if we are not using a video file, stop the camera video stream
	if not args.get("input", False):
		vs.stop()

	# otherwise, release the video file pointer
	else:
		vs.release()

	# close any open windows
	cv2.destroyAllWindows()

	avg_pwdist = statistics.mean(list_pwdist) # Average Pairwise Distances
	avg_x = statistics.mean(list_traveled_x) # Average X position
	avg_y = statistics.mean(list_traveled_y) # Average Y position
	csv_path = os.path.join(os.getcwd(),'video_data.csv')
	df = pd.DataFrame([{'Average Distance': round(avg_dist,4),
						'Average X': round(avg_x),
						'Average Y': round(avg_y),
						'Average Pairwise Distance': round(avg_pwdist,4),
						'timestamp': timestamp_list[j]}])

	df.to_csv(csv_path, mode='a', index=False, header=False)

	print(f"[INFO] Saving to CSV {csv_path}")
