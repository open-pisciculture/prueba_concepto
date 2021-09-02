#!/usr/bin/python3

'''
    Records video from two cameras, frame-by-frame
'''

import cv2
import numpy as np
import time
# import RPi.GPIO as GPIO
# from ubi_test import post_request

def get_cam_frame(index):
    cap = cv2.VideoCapture(index) # Index '0' is the default one
    ret, frame = cap.read()
    cap.release()

    return frame


def save_video_len(video_len):
    video_frames_1 = []
    video_frames_2 = []
    # print(f'FPS 1: {fps_1}\nFPS 2: {fps_2}')

    t0 = time.time()
    t1 = t0
    date_0 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    out_1 = cv2.VideoWriter(f'cam1_video_date_{date_0}.avi', cv2.VideoWriter_fourcc(*'MJPG'), 1.2, (320,240) )
    out_2 = cv2.VideoWriter(f'cam2_video_date_{date_0}.avi', cv2.VideoWriter_fourcc(*'MJPG'), 1.2, (320,240) )

    while t1 - t0 < video_len:
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        t1 = time.time()

        # Capture frame-by-frame
        frame_1 = get_cam_frame(0)
        frame_2 = get_cam_frame(2)
        # Added date to video frame
        frame_1 = cv2.putText(frame_1, date, (10,20), cv2.FONT_HERSHEY_DUPLEX, fontScale=0.5, color=(0,255,0))
        frame_1 = cv2.resize(frame_1, (320,240), interpolation = cv2.INTER_AREA)
        frame_2 = cv2.putText(frame_2, date, (10,20), cv2.FONT_HERSHEY_DUPLEX, fontScale=0.5, color=(0,255,0))
        frame_2 = cv2.resize(frame_2, (320,240), interpolation = cv2.INTER_AREA)

        out_1.write(frame_1)
        out_2.write(frame_2)

        # Display the resulting frame
        cv2.imshow('Cam 1', frame_1)
        cv2.imshow('Cam 2', frame_2)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        video_frames_1.append(frame_1)
        video_frames_2.append(frame_2)

    # When everything done, release the capture
    cv2.destroyAllWindows()

if __name__ == "__main__":
    date_0 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # GPIO.setmode(GPIO.BCM)
    # # Setting up the GPIO23 pin as input with pull_down logic (default 0 state when connected to GND)
    # GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # while True:
    print("Waiting for rising edge on port 23")
    # GPIO.wait_for_edge(23, GPIO.RISING)
    print("Rising edge detected.")
    save_video_len(5)
    print("Video saved")
