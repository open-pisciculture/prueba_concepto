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
from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import time
import cv2
import glob
import os
import numpy as np

print("[INFO] opening video file...")
vid_folder_path = os.path.join(os.getcwd(),'videos') # Opening cwd and joining it with `videos` folder name
files_in_path = glob.glob(r"{}/*.avi".format(vid_folder_path)) # This returns a list of all files ending with .avi in the path `img_folder_path`

vs_list = []
for i in range(len(files_in_path)):
	vs_list.append(cv2.VideoCapture(files_in_path[i]))

for j in range(len(vs_list)):
	vs = vs_list[j]
	totalFrames = 0
	print(f"[INFO] Obtaining frame from video No. {j+1}")

	# loop over frames from the video stream
	while True:
		# grab the next frame and handle if we are reading from either
		# VideoCapture or VideoStream
		frame = vs.read()
		frame = frame[1]

		# if we are viewing a video and we did not grab a frame then we
		# have reached the end of the video
		if frame is None:
			break

		# resize the frame to have a maximum width of 500 pixels (the
		# less data we have, the faster we can process it), then convert
		# the frame from BGR to RGB for dlib
		frame = imutils.resize(frame, width=500)
		rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		if np.mean(frame)<30:
			break

		if totalFrames == 300:
			# show the output frame
			cv2.imshow("Frame", frame)
			# Saving selected image
			cv2.imwrite(f"frames_from_videos/imagefrom_{files_in_path[j].split('/')[-1]}.png", frame)
			break

		key = cv2.waitKey(1) & 0xFF
		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

		# increment the total number of frames processed thus far and
		# then update the FPS counter
		totalFrames += 1
	# otherwise, release the video file pointer
	else:
		vs.release()

	# close any open windows
	cv2.destroyAllWindows()
