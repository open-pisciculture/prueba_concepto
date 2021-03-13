#!/usr/bin/python3

import cv2
import numpy as np
import matplotlib.pyplot as plt
import threading
import retinex
from ubi_test import post_request

print("Versión de OpenCV:",cv2.__version__)

global cap, frame
cap = cv2.VideoCapture(-1)
frame = np.array([])

def quitar_ruido(img):
    # Create our sharpening kernel, the sum of all values must equal to one for uniformity
    kernel_sharpening = np.array([[-1,-1,-1],
                                 [-1, 9,-1],
                                 [-1,-1,-1]])
    sharpened_img = cv2.filter2D(img, -1, kernel_sharpening)
    return sharpened_img
    
def procesar_video():
    global cap, frame
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # PROCESAMIENTO DE LA IMAGEN (frame)
        imagen_filtrada = quitar_ruido(frame)
        # bordes = cv2.Canny(imagen_filtrada, 100,200)

        # Display the resulting frame
        cv2.imshow('ImagenEstanque', imagen_filtrada)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def inicializar_hist():
    color = 'gray'
    bins = 16
    resizeWidth = 0

    # Initialize plot.
    fig, ax = plt.subplots()
    if color == 'rgb':
        ax.set_title('Histogram (RGB)')
    else:
        ax.set_title('Histogram (grayscale)')
    ax.set_xlabel('Bin')
    ax.set_ylabel('Frequency')
    
    # Initialize plot line object(s). Turn on interactive plotting and show plot.
    lw = 3
    alpha = 0.5
    if color == 'rgb':
        lineR, = ax.plot(np.arange(bins), np.zeros((bins,)), c='r', lw=lw, alpha=alpha)
        lineG, = ax.plot(np.arange(bins), np.zeros((bins,)), c='g', lw=lw, alpha=alpha)
        lineB, = ax.plot(np.arange(bins), np.zeros((bins,)), c='b', lw=lw, alpha=alpha)
    else:
        lineGray, = ax.plot(np.arange(bins), np.zeros((bins,1)), c='k', lw=lw)
    ax.set_xlim(0, bins-1)
    ax.set_ylim(0, 1)
    plt.ion()
    plt.show()

    # Grab, process, and display video frames. Update plot line object(s).
    while True:
        (grabbed, frame) = cap.read()

        if not grabbed:
            break

        # Resize frame to width, if specified.
        if resizeWidth > 0:
            (height, width) = frame.shape[:2]
            resizeHeight = int(float(resizeWidth / width) * height)
            frame = cv2.resize(frame, (resizeWidth, resizeHeight),
                interpolation=cv2.INTER_AREA)

         # Normalize histograms based on number of pixels per frame.
        numPixels = np.prod(frame.shape[:2])
        if color == 'rgb':
            cv2.imshow('Imagen Estanque', frame)
            (b, g, r) = cv2.split(frame)
            histogramR = cv2.calcHist([r], [0], None, [bins], [0, 255]) / numPixels
            histogramG = cv2.calcHist([g], [0], None, [bins], [0, 255]) / numPixels
            histogramB = cv2.calcHist([b], [0], None, [bins], [0, 255]) / numPixels
            lineR.set_ydata(histogramR)
            lineG.set_ydata(histogramG)
            lineB.set_ydata(histogramB)
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('Org', frame)
            # RETINEX: descomentar para mostrar cómo queda la imagen luego de aplicar retinex
            # img_amsrcr = retinex.automatedMSRCR(frame,[15, 80, 250])
            # cv2.imshow('AMSRCR', img_amsrcr)
            histogram = cv2.calcHist([gray], [0], None, [bins], [0, 255]) / numPixels
            lineGray.set_ydata(histogram)

            # Calculo la media del histograma
            hist_mean = np.mean(histogram)

            # Creo un diccionario para publicarlo en Ubidots
            dict_data = {"histogram_mean": hist_mean}
            
            # Acá se publica en Ubidots
            # post_request(dict_data)
        fig.canvas.draw()

        # PROCESAMIENTO DE LA IMAGEN (frame)
        # bordes = cv2.Canny(frame, 100,200)

        # Display the resulting frame
        # cv2.imshow('Bordes Imagen', bordes)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()




if __name__ == '__main__':
   hist_process = threading.Thread(target = inicializar_hist)
   hist_process.start()