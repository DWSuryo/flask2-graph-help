# Energy Test
## Running the program
1. make virtual environment
2. install the requirement `pip install -r requirements.txt`
3. run flask `python flask2-mqtt-mq.py`

Types of testing:
1. Energy test from MQTT
2. Energy test from generator

## 1. Energy test from MQTT
1. Change the html and JS in flask program to `main_amcharts_mq.html` and `main_amcharts_mq.js`
2. run `python mqtt_pub_test_sensor.py` for mqtt

## 2. Energy test from generator
1. Change the html and JS in flask program to `main_amcharts5.html` and `main_amcharts5.html`
2. run `python date_test_rt.html` for csv generator