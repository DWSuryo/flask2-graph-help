# https://www.emqx.io/blog/how-to-use-mqtt-in-python
# You can change MQTT broker with its username and password

import paho.mqtt.client as mqttc
import random
import time
import json

broker = 'localhost'
port = 1883

topic_s0 = "45856/esp8266/sensors0"    #here
topic_s1 = "45856/esp8266/sensors1"    #here
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = ''
password = ''

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqttc.Client(client_id)
    client.username_pw_set(username, password)    #set user pass
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        rng_01 = round(random.uniform(0,100),3)
        rng_02 = round(random.uniform(0,100),3)
        rng_03 = round(random.uniform(0,300),3)

        rng_11 = round(random.uniform(0,100),3)
        rng_12 = round(random.uniform(0,100),3)
        rng_13 = round(random.uniform(0,300),3)
        
        # JSON data
        esp_sensor0={
            'temperature1' : rng_01,
            'humidity1' : rng_02,
            'power1' : rng_03
        }
        esp_sensor1={
            'temperature1' : rng_11,
            'humidity1' : rng_12,
            'power1' : rng_13
        }

        #print(esp_sensor, type(esp_sensor))        #here
        print("convert to JSON")
        esp_sensor_out0 = json.dumps(esp_sensor0)
        esp_sensor_out1 = json.dumps(esp_sensor1)
        #print(esp_sensor_out, type(esp_sensor_out))    #here

        
        msg = f"messages: {msg_count}"
        # result = client.publish(topic1, rng1)
        # result = client.publish(topic2, rng2)
        # result = client.publish(topic3, rng3)
        result = client.publish(topic_s0, esp_sensor_out0)    #s0
        result = client.publish(topic_s1, esp_sensor_out1)    #s1
        status = result[0]
        if status == 0:
            # print(f"Send `{msg}` to topic `{topic1}`: {rng1}")
            # print(f"Send `{msg}` to topic `{topic2}`: {rng2}")
            # print(f"Send '{msg}' to topic '{topic3}': {rng3}")
            #print(f"Send '{msg}' to topic '{topic4}': {esp_sensor_out}")
            #print(f"Send '{msg}' to topic '{topic5}': {cam_sensor_out}\n")
            print(f"Send '{msg}' to topic '{topic_s0}': {esp_sensor_out0}\n")
            #print(f"Send '{msg}' to topic '{topic_s1}': {esp_sensor_out1}\n")
        else:
            # print(f"Failed to send message to topic {topic1} {topic2} {topic3}")
            print(f"Failed to send message")
        time.sleep(5)
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    print("starting program")
    run()