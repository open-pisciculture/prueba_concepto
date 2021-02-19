#!/usr/bin/python3

import cv2
import numpy as np
import time

def save_video_len(video_len):
    video_frames = []
    cap = cv2.VideoCapture(-1)
    frame = np.array([])
    t0 = time.time()
    t1 = t0
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    out = cv2.VideoWriter('saved_videos/saved_video_date_{}.avi'.format(date), cv2.VideoWriter_fourcc(*'MJPG'), 30.0, (640,480) )

    while t1 - t0 < video_len:
        t1 = time.time()

        # Capture frame-by-frame
        ret, frame = cap.read()
        out.write(frame)

        # Display the resulting frame
        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        video_frames.append(frame)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

save_video_len(5)