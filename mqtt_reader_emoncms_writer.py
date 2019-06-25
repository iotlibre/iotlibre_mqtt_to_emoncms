#! /usr/bin/python
# iotlibre/xxx_node/dato:valor
# @reboot sleep 180 && /home/pi/iotlibre/mqtt_reader_emoncms_writer.py

import time
import paho.mqtt.client as mqtt
import urllib2

class MyException(Exception):
    pass

ip_emoncms="91.121.222.125"
node_name="node_test"
name="temperatura"
value="33.4"
api_key ="1e6532c40e9208636447a85a12e2ce92"
response='nook'
url_long= 'http'

def tx_emoncms(ip_,node_name_,name_,value_,api_key_):
    result = 'ok'
    url_long= 'http://{0}/emoncms/input/post?node={1}&fulljson={{"{2}":{3}}}&apikey={4}'
    url_long=url_long.format(ip_,node_name_,name_,value_,api_key_)

    try:
        response = urllib2.urlopen(url_long, timeout=5)
    except:
        result="time_out"
    # print url_long
    # print response.getcode()
    # print result

def on_connect(client, obj, flags, rc):
    # print("rc: " + str(rc))
    client.subscribe("iotlibre/#")

def on_message(client, userdata, msg):
    cadena=msg.topic
    cadena_1=cadena.split("/")
    # print(cadena_1[1]+" -> "+cadena_1[2]+" -> "+str(msg.payload))
    # print(msg.topic+" "+str(msg.payload))
    tx_emoncms(ip_emoncms,cadena_1[1],cadena_1[2],str(msg.payload),api_key)

def on_disconnect(client, userdata, rc):
    if rc != 0:
       result="Unexpected disconnection"

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_diconnect = on_disconnect


client.username_pw_set("emonpi","emonpimqtt2016")
client.connect("127.0.0.1", 1883, 60)
# client.connect("192.168.1.113", 1883, 60)
client.loop_forever(timeout=1.0, max_packets=1, retry_first_connection=False)
