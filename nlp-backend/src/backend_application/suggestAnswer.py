#******************************************************************************#
#* Name:     suggestAnswer.py                                                 *#
#* Author:   ssa                                                              *#
#*                                                                            *#
#* Description:                                                               *#
#*  Implements the server-sent events concept for the suggestions in the      *#
#*  sidebar of the frontend application. Events published by the              *#
#*  mqtt_subscriber are pushed asynchronous to the frontend.                  *#
#*                                                                            *#
#*                                                                            *#
#******************************************************************************#

import json
import random
import requests
import time
from flask import Response
import paho.mqtt.client as mqtt
import queue
import os

class MessageAnnouncer:
    
    def __init__(self):
        self.listeners = []
        self.listener = queue.Queue(maxsize=5)

    def listen(self):
        # q = queue.Queue(maxsize=1)
        # self.listeners.append(q)
        # return q
        return self.listener

    def announce(self, msg):
        # for i in reversed(range(len(self.listeners))):
        #     try:
        #         self.listeners[i].put_nowait(msg)
        #     except queue.Full:
        #         del self.listeners[i]

        try:
            self.listener.put_nowait(msg)
        except queue.Full:
            self.listener.queue.clear()
            

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe(os.environ["MQTT_ANSWER"])

def on_message(client, userdata, msg):
    if msg.payload.decode() !='':
        announcer.announce(msg='data: {}\n\n'.format(str(msg.payload.decode())))
    
def on_log(client, userdata, level, buf):
    print("subscriber log: ", buf)

def eventStream():
    messages = announcer.listen()  # returns a queue.Queue
    try:
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg
    finally:
        # cleanup
        with messages.mutex:
            messages.queue.clear()

announcer = MessageAnnouncer()

def suggestAnswers():    
    client = mqtt.Client()
    client.connect(os.environ["MQTT_BROKER"], port=int(os.environ["MQTT_PORT"]), keepalive=int(os.environ["MQTT_KEEPALIVE"]), bind_address="")
    client.on_log = on_log
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_start()
    return Response(eventStream(), mimetype="text/event-stream", headers={'Content-Encoding': 'none'})

