#!/usr/bin/python3
import serial
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import io
import binascii

# from ubi_test import post_request
baud_rate = 115200

#TODO: Esto es temporal. Mejor que el arduino envie un string que este mejor disenado para recuperar los datos.
def obtenerNumero(s):
    l = []
    for t in s.split():
        try:
            l.append(float(t))
        except ValueError:
            pass

    return l

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', baud_rate, timeout=1)
    ser.flush()
    while True:
        try:
            # print("Waiting for reading...")
            if ser.in_waiting > 0:
                print("Got something")
                # Read raw serial port
                data = ser.read(6000) #.rstrip() # 6000 is just a very high limit of bytes to read
                print(f'data type: {type(data)}')
                print(f'data length: {len(data)}')
                print(f'Data:\n {data}')

                # # Read decoded serial port
                # line = ser.readline().decode('utf-8').rstrip()

                # #desde 19 hasta 25
                # num = obtenerNumero(line)[0]
                # data = {"histogram_mean": num}
                # print(data)
                # post_request(data)
        except KeyboardInterrupt:
            ser.close()
            break
        