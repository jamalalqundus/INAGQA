
import paho.mqtt.client as mqtt #import the client1
import time
from config import settings

# This is the Publisher

def on_log(client, userdata, level, buf):
    print("publisher log: ",buf, settings['broker_address'],settings['port'])

client = mqtt.Client()
client.connect(settings['broker_address'], port=settings['port'], keepalive=settings['keepalive'], bind_address="")
client.on_log=on_log

#client.publish("topic/entityNotFound", "Fraunhofer_Institute_for_Open_Communication_Systems")
#time.sleep(5)
#client.publish("topic/entityNotFound", "Siemens_AG")
#time.sleep(5)
client.publish(settings['event_message'], "adidas")

client.disconnect()