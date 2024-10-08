import time
import random
from paho.mqtt import client as mqtt_client
from datetime import datetime  # To generate timestamps

broker = 'broker.emqx.io'
port = 8083
voltage_topic = "topic/voltage"
current_topic = "topic/current"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
username = 'user1'
password = '123'

# Function to generate a timestamped filename
def generate_filename(data_type):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{data_type}_{timestamp}.txt"

# Function to generate a timestamp for the data
def get_current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id, transport="websockets")
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        message = msg.payload.decode()
        current_timestamp = get_current_timestamp()  # Get the current time for each data point
        print(f"Received `{message}` from `{msg.topic}` topic at {current_timestamp}")

        # Save the message with a timestamp in the file
        if msg.topic == voltage_topic:
            filename = generate_filename("voltage")
            with open(filename, 'w') as f:
                f.write(f"Timestamp: {current_timestamp}, Voltage: {message}\n")
            print(f"Saved voltage data to {filename}")
        elif msg.topic == current_topic:
            filename = generate_filename("current")
            with open(filename, 'w') as f:
                f.write(f"Timestamp: {current_timestamp}, Current: {message}\n")
            print(f"Saved current data to {filename}")
        else:
            print(f"Unknown topic: {msg.topic}")

    # Subscribe to both voltage and current topics
    client.subscribe(voltage_topic)
    client.subscribe(current_topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()
