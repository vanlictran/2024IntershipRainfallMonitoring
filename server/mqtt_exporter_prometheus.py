import paho.mqtt.client as mqtt
import json

rain_data = {}
water_level_data = {}

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
    
    if 'data' in payload['object'] and payload['object']['data'].get('rain') is not None :
        # Update the global dictionary
        rain_value = payload['object']['data'].get('rain')
        rain_data[deveui] = rain_value
        print(f"Updated rain data for devEUI '{deveui}': {rain_value}")
        
    elif payload['object'].get('waterLevel') is not None :
        water_level_value = payload['object'].get('waterLevel')
        water_level_data[deveui] = water_level_value
        print(f"Updated water level data for devEUI '{deveui}': {water_level_value}")

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("application/84/device/+/event/up")

# Create an MQTT client instance
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# Connect to the broker
mqttc.connect("vngalaxy.vn", 1883, 60)

# Start the loop to process network traffic
mqttc.loop_forever()
