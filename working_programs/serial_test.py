#!/usr/bin/python3
import serial
from ubi_test import post_request

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
    ser = serial.Serial('/dev/ttyACM0', 38400, timeout=1)
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            # Read raw serial port
            print(ser.readline().rstrip())

            # # Read decoded serial port
            # line = ser.readline().decode('utf-8').rstrip()

            # #desde 19 hasta 25
            # num = obtenerNumero(line)[0]
            # data = {"histogram_mean": num}
            # print(data)
            # post_request(data)