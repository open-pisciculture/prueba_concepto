#!/usr/bin/python3

import cv2
import numpy as np

print("Versión de OpenCV:",cv2.__version__)

def quitar_ruido(img):
    # Create our sharpening kernel, the sum of all values must equal to one for uniformity
    kernel_sharpening = np.array([[-1,-1,-1],
                                 [-1, 9,-1],
                                 [-1,-1,-1]])
    sharpened_img = cv2.filter2D(img, -1, kernel_sharpening)
    return sharpened_img

cap = cv2.VideoCapture(-1)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # PROCESAMIENTO DE LA IMAGEN (frame)
    imagen_filtrada = quitar_ruido(frame)

    # Display the resulting frame
    cv2.imshow('ImagenEstanque', imagen_filtrada)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()