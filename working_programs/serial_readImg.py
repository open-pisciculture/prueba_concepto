#!/usr/bin/python3
import random
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
                data = ser.read(20000)#.rstrip() # 6000 is just a very high limit of bytes to read
                # print(data)

                # r_data = binascii.unhexlify(data)
                r_data = data
                #r_data = "".unhexlify(chr(int(b_data[i:i+2],16)) for i in range(0, len(b_data),2))

                try:
                    stream = io.BytesIO(r_data)

                    img = Image.open(stream)
                    draw = ImageDraw.Draw(img)
                    print(f'Read image of length {len(r_data)} with format {img.format}')
                    img.show()

                    img_name = "a_test" + str(int(random.random()*100)) + ".png"
                    img.save(img_name)
                except Exception as e:
                    print(f'Error reading data of len {len(data)} because of: {e}')

                # print(data)

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
        