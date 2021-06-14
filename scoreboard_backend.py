import paho.mqtt.client as mqtt
import re
import json,time

import sys,os
import curses

jsondata = [0] * 4


MQTT_ADDRESS = 'mqtt.championwescott.lan'
MQTT_USER = 'mqtt'
MQTT_PASSWORD = 'mqtt'
MQTT_TOPIC = 'curling/palmetto/+'
MQTT_REGEX = 'curling/palmetto/([^/]+)'
MQTT_CLIENT_ID = 'test_id'


def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    sheetnum = int(_parse_mqtt_message(msg.topic, msg.payload.decode('utf-8')))
    with open('/home/pi/curling-scores.json','r') as fd:
        jsondata = json.loads(fd.read())
    jsondata[sheetnum-1] = json.loads(msg.payload)
    with open('/home/pi/curling-scores.json','w') as fd:
        json.dump(jsondata,fd,indent=4)
    
    


def _parse_mqtt_message(topic, payload):
    match = re.match(MQTT_REGEX, topic)
    if match:
        location = match.group(1)
        return location
    else:
        return None



def main():
    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.connect(MQTT_ADDRESS, 1883)  
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.loop_forever()


if __name__ == '__main__':
    main()
