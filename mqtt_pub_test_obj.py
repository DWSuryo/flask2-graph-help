# https://www.emqx.io/blog/how-to-use-mqtt-in-python
# You can change MQTT broker with its username and password

import paho.mqtt.client as mqttc
import random
import time
import json

broker = 'localhost'
port = 1883

topic_cv0 = '45856/cv/auto0'
topic_cv1 = '45856/cv/auto1'
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
        # new
        left0 = random.randint(0,3)
        right0 = random.randint(0,3)
        left1 = random.randint(0,3)
        right1 = random.randint(0,3)
        
        # JSON data
        cam_sensor0={
            'RF0' : left0,
            'RF1' : right0
        }
        cam_sensor1={
            'RF0' : left1,
            'RF1' : right1
        }
        #print(cam_sensor, type(cam_sensor))
        print("convert to JSON")
        #cam_sensor_out = json.dumps(cam_sensor)
        cam_sensor_out0 = json.dumps(cam_sensor0)
        cam_sensor_out1 = json.dumps(cam_sensor1)
        #print(cam_sensor_out, type(cam_sensor_out))

        
        msg = f"messages: {msg_count}"
        # result = client.publish(topic1, rng1)
        # result = client.publish(topic2, rng2)
        # result = client.publish(topic3, rng3)
        #result = client.publish(topic4, esp_sensor_out)    #here
        #result = client.publish(topic5, cam_sensor_out)
        result = client.publish(topic_cv0, cam_sensor_out0)
        result = client.publish(topic_cv1, cam_sensor_out1)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            # print(f"Send `{msg}` to topic `{topic1}`: {rng1}")
            # print(f"Send `{msg}` to topic `{topic2}`: {rng2}")
            # print(f"Send '{msg}' to topic '{topic3}': {rng3}")
            #print(f"Send '{msg}' to topic '{topic4}': {esp_sensor_out}")
            #print(f"Send '{msg}' to topic '{topic5}': {cam_sensor_out}\n")
            print(f"Send '{msg}' to topic '{topic_cv0}': {cam_sensor_out0}\n")
            print(f"Send '{msg}' to topic '{topic_cv1}': {cam_sensor_out1}\n")
        else:
            # print(f"Failed to send message to topic {topic1} {topic2} {topic3}")
            print(f"Failed to send message")
        time.sleep(1)
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    print("starting program")
    run()