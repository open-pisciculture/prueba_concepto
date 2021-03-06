#!/usr/bin/python3

# import RPi.GPIO as GPIO
# import dht11
import time
import ibmiotf.device
import numpy as np
import yaml
import wiotp.sdk.device
import wiotp.sdk.messages
from datetime import datetime
import pytz

# import wiotp.sdk.messages.Message
# import wiotp.sdk.messages.MessageCodec

organization = "1pv9sa" #add organisation from the IoT platform service
deviceType = "RasPi" #add device type from the IoT platform service
deviceId = "665544332211" #add device ID from the IoT platform service
authMethod = "token"
authToken = "Tkn.1234" #add authentication token from the IoT platform service

LED_pin = 4
DHT11_pin = 22

temp = 0
hum = 0

# Initialize the device client.
deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
# client = wiotp.sdk.device.DeviceClient(deviceOptions)
client = ibmiotf.device.Client(deviceOptions)
print("init successful")

# DHT11_sensor = dht11.DHT11(pin = DHT11_pin)

# # initialize GPIO
# def init_GPIO():
#     GPIO.setwarnings(False)
#     GPIO.setmode(GPIO.BCM)
#     GPIO.cleanup()

#     # set LED pin as output
#     GPIO.setup(LED_pin, GPIO.OUT)
     
# get temperature and humidity from the sensor
def getTempHum():
    global temp
    global hum
    # temp_hum = DHT11_sensor.read()
    # if temp_hum.is_valid():
    #     temp = temp_hum.temperature
    #     hum =  temp_hum.humidity
    temp = np.sin( (2*np.pi/100) * time.time())
    hum = 90*np.cos( (2*np.pi/300) * time.time())


def myOnPublishCallback():
    print("Confirmed event received by IoTF")

# Connect and send a datapoint 
def send(data):
    success = client.publishEvent("data", "json", data, qos=0, on_publish=myOnPublishCallback)
    if not success:
        print("Not connected to IoTF")

# get a command from Watson IoT Platform
def myCommandCallback(cmd):
    print("Command received: %s\n" % cmd.data)
    if cmd.data['led_on'] == 1:
        print('LED ON')
        # GPIO.output(LED_pin, True)
    else:
        pass
        # GPIO.output(LED_pin, False)


if __name__=='__main__':
    # init_GPIO()
    client.connect()
    while True:
        try:
            getTempHum()
            local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            send( {"temp":temp, "hum": hum, "timestamp": local_time } )
            
            client.commandCallback = myCommandCallback
            
            time.sleep(15)
            
        except KeyboardInterrupt:
            client.disconnect()
            # GPIO.cleanup()
            break