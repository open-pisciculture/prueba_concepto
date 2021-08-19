#!/usr/bin/python3

'''
    Run Wait_for_edge program
'''

import cv2
import numpy as np
import time
import RPi.GPIO as GPIO
# from ubi_test import post_request

def save_video_len(video_len):
    video_frames_1 = []
    video_frames_2 = []
    cap_1 = cv2.VideoCapture(0) # Index '0' is the default one
    cap_2 = cv2.VideoCapture(2) # Index '2' was obtained by trial and error
    fps_1 = 8 # fps_1 = cap_1.get(cv2.CAP_PROP_FPS) # Getting FPS for Cam 1, but this returns 0.0 in the Raspberry Pi for some reason :/
    fps_2 = 8 # fps_2 = cap_2.get(cv2.CAP_PROP_FPS) # Getting FPS for Cam 2, but this returns 0.0 in the Raspberry Pi for some reason :/
    # print(f'FPS 1: {fps_1}\nFPS 2: {fps_2}')

    frame_1 = np.array([])
    frame_2 = np.array([])
    t0 = time.time()
    t1 = t0
    date_0 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    out_1 = cv2.VideoWriter(f'cam1_video_date_{date_0}.avi', cv2.VideoWriter_fourcc(*'MJPG'), fps_1, (320,240) )
    out_2 = cv2.VideoWriter(f'cam2_video_date_{date_0}.avi', cv2.VideoWriter_fourcc(*'MJPG'), fps_2, (320,240) )

    while t1 - t0 < video_len:
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        t1 = time.time()

        # Capture frame-by-frame
        ret_1, frame_1 = cap_1.read()
        ret_2, frame_2 = cap_2.read()
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
    cap_1.release()
    cap_2.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    date_0 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    GPIO.setmode(GPIO.BCM)
    # # Setting up the GPIO23 pin as input with pull_down logic (default 0 state when connected to GND)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # while True:
    print("Waiting for rising edge on port 23")
    GPIO.wait_for_edge(23, GPIO.RISING)
    print("Rising edge detected.")
    save_video_len(5)
    time.sleep(3)
    print("Video saved")
