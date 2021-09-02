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
    video_frames = []
    cap = cv2.VideoCapture(0)
    fps = 8 # fps = cap.get(cv2.CAP_PROP_FPS) # This returns 0.0 in the Raspberry Pi for some reason :/
    
    frame = np.array([])
    t0 = time.time()
    t1 = t0
    date_0 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    out = cv2.VideoWriter(f'saved_video_date_{date_0}.avi', cv2.VideoWriter_fourcc(*'MJPG'), fps, (320,240) )

    while t1 - t0 < video_len:
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        t1 = time.time()

        # Capture frame-by-frame
        ret, frame = cap.read()
        # Added date to video frame
        frame = cv2.putText(frame, date, (10,20), cv2.FONT_HERSHEY_DUPLEX, fontScale=0.5, color=(0,255,0))
        frame = cv2.resize(frame, (320,240), interpolation = cv2.INTER_AREA)

        out.write(frame)

        # Display the resulting frame
        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        video_frames.append(frame)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    date_0 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    GPIO.setmode(GPIO.BCM)
    # Setting up the GPIO23 pin as input with pull_down logic (default 0 state when connected to GND)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # while True:
    print("Waiting for rising edge on port 23")
    GPIO.wait_for_edge(23, GPIO.RISING)
    print("Rising edge detected.")
    save_video_len(5)
    time.sleep(3)
    print("Video saved")
