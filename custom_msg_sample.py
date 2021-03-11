import wiotp.sdk.device
import wiotp.sdk.messages
import yaml
import datetime
import pytz
import numpy as np
import time

print('time', datetime.datetime.now(pytz.timezone('UTC')))

options = wiotp.sdk.device.parseConfigFile("device_RasPi.yaml")
client = wiotp.sdk.device.DeviceClient(options)

def eventPublishCallback():
    print("Device Publish Event done!!!")

client.connect()

class CustomTimeCodec(wiotp.sdk.messages.MessageCodec):

    # @staticmethod
    # def encode(data=None, timestamp=datetime.datetime.now(pytz.timezone('Europe/Vienna')):
    #     print('DATA#####',data)
    #     return yaml.dump(data)
    
    @staticmethod
    def encode(data=None, timestamp=None):
        return data['hello_time'] + "," + str(data['temp_time']) + "," + str(data['hum_time'])

    # @staticmethod
    # def decode(message):
    #     try:
    #         data = yaml.loads(message.payload.decode("utf-8"))
    #     except ValueError as e:
    #         raise InvalidEventException("Unable to parse YAML.  payload=\"%s\" error=%s" % (message.payload, str(e)))

    #     timestamp = datetime.datetime.now(pytz.timezone('UTC'))

    #     return wiotp.sdk.messages.Message(data, timestamp)

    @staticmethod
    def decode(message):
        (hello, temp, hum) = message.payload.split(",")
        
        data = {}
        data['hello_time'] = hello
        data['temp_time'] = temp
        data['hum_time'] = hum

        timestamp = datetime.datetime.now(pytz.timezone('UTC'))
        
        return Message(data, timestamp)

client.setMessageCodec("custom", CustomTimeCodec)

data={'hello_time' : 'hey there', 'temp_time': np.sin( (2*np.pi/100) * time.time()), 'hum_time': 90*np.cos( (2*np.pi/300) * time.time())}
data={'hello_time' : 'hey there', 'temp_time': -100, 'hum_time': -50}
# success_0 = client.publishEvent("status", "json", data, 0, eventPublishCallback)
success_1 = client.publishEvent("status", "custom", data, 0, eventPublishCallback)
client.disconnect()