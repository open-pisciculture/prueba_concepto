#!/usr/bin/python3
import serial
import numpy as np
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

printBytes = False

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', baud_rate, timeout=1)
    ser.reset_input_buffer()
    ser.flush()
    while True:
        try:
            # print("Waiting for reading...")
            if ser.in_waiting > 0:
                print("Got something -------------------------->")
                # Read raw serial port
                data = ser.read(25000) #.rstrip() # 6000 is just a very high limit of bytes to read
                print(f'data type: {type(data)}')
                print(f'data length: {len(data)}')

                pieceSize = 8192
                if len(data) == pieceSize:
                    data_pkg = []
                    data_pkg.append(data[:])
                    i = 0
                    while True:
                        if ser.in_waiting > 0:
                            i += 1
                            print(f'Got another piece of pkg of len: {len(data)} (#{i})')
                            data = ser.read(pieceSize+1000)
                            data_pkg.append(data[:])
                            if len(data) != pieceSize:
                                print(f'Received last piece of size {len(data)}\n')
                                break
                    print(f'Size of final pkg is {len(np.array(data_pkg).flatten())}')
                    print(f'Last piece was:\n {data_pkg[-1]}')
 
                if len(data) < 1000: # only print if data is short
                    print(data)
                    if printBytes:
                        hexBytes = ',0x'.join('{:02x}'.format(x) for x in data)
                        print(f'Data: {hexBytes}\n')
                    else:
                        print(data)

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
        