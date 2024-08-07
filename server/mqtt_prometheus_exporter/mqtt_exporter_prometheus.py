import paho.mqtt.client as mqtt
import json

from prometheus_client import start_http_server, Gauge
import time

rain_data = {}
humidity_data = {}
temperature_data = {}
voltage_data = {}
water_level_data = {}

rain_gauge = Gauge('rain_amount', 'Amount of rain measured', ['devEUI'])
humidity_gauge = Gauge('humidity_percentage', 'Percentage of humidity measured', ['devEUI'])
temperature_gauge = Gauge('temperature_level', 'Temperature measured', ['devEUI'])
voltage_gauge = Gauge('voltage_level', 'Voltage used by the rain gauge', ['devEUI'])
water_level_gauge = Gauge('water_level', 'Water level measured', ['devEUI'])

# Callback when a message is received
def on_message(client, userdata, message):
    payload_str = message.payload.decode()
    
    # Decode the JSON payload
    payload = json.loads(payload_str)
    
    # Check if 'devEUI' key exists
    if 'devEUI' not in payload:
        print(f"Missing 'devEUI' in payload: {payload_str}")
        return

    deveui = payload['devEUI']

    # Check if 'object' and 'data' keys exist in the payload
    if 'object' not in payload :
        print(f"Missing 'object' : {payload_str}")
        return
    
    if 'data' in payload['object'] :
        data = payload['object']['data']
        
        rain_value = data.get('rain')
        temperature_value = data.get('temperature')
        humidity_value = data.get('humidity')
        voltage_value = data.get('voltage')
        
        if rain_value is not None :
            rain_data[deveui] = rain_value
            rain_gauge.labels(devEUI=deveui).set(rain_value)
            print(f"Updated rain data for devEUI '{deveui}': {rain_value}")
        
        if temperature_value is not None :
            temperature_data[deveui] = temperature_data
            temperature_gauge.labels(devEUI=deveui).set(temperature_value)
            print(f"Updated temperature data for devEUI '{deveui}': {temperature_value}")
        
        if humidity_value is not None :
            humidity_data[deveui] = humidity_value
            humidity_gauge.labels(devEUI=deveui).set(humidity_value)
            print(f"Updated humidity data for devEUI '{deveui}': {humidity_value}")
        
        if voltage_value is not None :
            voltage_data[deveui] = voltage_value
            voltage_gauge.labels(devEUI=deveui).set(voltage_value)
            print(f"Updated voltage data for devEUI '{deveui}': {voltage_value}")
        
    elif payload['object'].get('waterLevel') is not None :
        water_level_value = payload['object'].get('waterLevel')
        water_level_data[deveui] = water_level_value
        water_level_gauge.labels(devEUI=deveui).set(water_level_value)
        print(f"Updated water level data for devEUI '{deveui}': {water_level_value}")

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("application/84/device/+/event/up")

# Start Prometheus HTTP server
start_http_server(8000)

# Create an MQTT client instance
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# Connect to the broker
mqttc.connect("vngalaxy.vn", 1883, 60)

# Start the loop to process network traffic
mqttc.loop_start()

# Keep the script running to allow the Prometheus server to serve metrics
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
    mqttc.loop_stop()
