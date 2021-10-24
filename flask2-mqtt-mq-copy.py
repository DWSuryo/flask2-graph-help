import paho.mqtt.client as mqtt
from flask import (Flask, render_template, request, redirect, url_for)
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import eventlet
from datetime import datetime    # show date
import time                      # time
import csv        # for storing data
import psycopg2 as psql   # PostgreSQL
import json
import atexit

# initialize mqtt broker
mqttc=mqtt.Client(client_id="webdev")
broker = 'localhost'
port = 1883
username = ''
password = ''
print("mqtt broker initialized")

class WRITE:
   def __init__(self):
      self.tgl_temp=0
      self.w=0
   def writesensor_csv(self,filedir,msg_json,step):
      with open(filedir, mode='a'):
         with open(filedir, mode='r+', newline='') as file:
            reader = csv.reader(file, delimiter=",")
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            tgl = datetime.now().replace(microsecond=0)
            print(f"{tgl.hour} --- {self.tgl_temp}")
            if tgl.hour != self.tgl_temp:
               print("energy reset")
               self.w = 0
            self.tgl_temp = tgl.hour

            power = float(msg_json["power1"])
            print(f"{self.w} --- {round((self.w + power/(3600/step)),3)}")
            self.w += round((power/(3600/step)),3)

            header = ['tgl','temp','hum','power','energy']
            row = [tgl,
                     # tgl.strftime("%x"),
                     # tgl.strftime("%X"),
                     msg_json["temperature1"],
                     msg_json["humidity1"],
                     msg_json["power1"],
                     #msg_json["energy1"],
                     self.w
                     ]
            print(row)

            #print(f'file opened: {msg_json["temperature1"]} --- {msg_json["humidity1"]} --- {msg_json["kwh1"]} --- {tgl}')
            #way to write to csv file
            print(enumerate(reader))
            rowcount = sum(1 for num in reader)     #row count
            if rowcount == 0:
               writer.writerow(header)
               print('header written, row count:',rowcount)
            writer.writerow(row)
            print("row written, row count",rowcount)

eventlet.monkey_patch()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'xDsTbiULqIrqXkO_X5kcyg'
socketio = SocketIO(app, ping_interval=5, ping_timeout=10)
CORS(app)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
   print("Connected with result code "+str(rc))

   # Subscribing in on_connect() means that if we lose the connection and
   # reconnect then subscriptions will be renewed.
   client.subscribe("45856/esp8266/sensors0")

# The callback for when a PUBLISH message is received from the ESP8266.
writefile = WRITE()
def on_message(client, userdata, message):
   
   print("Received message '" + str(message.payload) + "' on topic '"
      + message.topic + "' with QoS " + str(message.qos))
   if message.topic == "45856/esp8266/sensors0":
      esp1 = str(message.payload.decode('utf-8'))
      print('received esp1 ', type(esp1))
      esp1_conv = json.loads(esp1)
      print('convert esp1 ', type(esp1_conv))
      print(f'esp1_conv: temp1 {esp1_conv["temperature1"]} --- hum1 {esp1_conv["humidity1"]} --- power1 {esp1_conv["power1"]}')
      print(type(esp1_conv['temperature1']), type(esp1_conv['humidity1']), type(esp1_conv['power1']))

      # csv write
      writefile.writesensor_csv('./static/sensor_hour_mq.csv',esp1_conv,5)

# launch mqtt
mqttc.username_pw_set(username, password) #set user pass
#mqttc=mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect(broker,port,60)
mqttc.loop_start()
print("mqtt launched")

@app.route("/")
def home():
   #return redirect(url_for('main'))
   return render_template('placeholder.html')
@app.route("/chart")
@app.route("/chart/graph-gen")
def main_gen():
   # Pass the template data into the template main_csv_socket.html and return it to the user
   return render_template('main_amcharts5.html', async_mode=socketio.async_mode)
@app.route("/chart/graph-mq")
def main_mq():
   return render_template('main_amcharts_mq.html', async_mode=socketio.async_mode)

def OnExitApp():
    print("exit Flask application")
atexit.register(OnExitApp)

if __name__ == "__main__":
   socketio.run(app, host='0.0.0.0', port=8080, debug=True)
