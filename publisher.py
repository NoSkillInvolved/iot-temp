import paho.mqtt.client as mqtt 
import time

dataPipe = [107.04, 115.03, 115.50, 118.69, 120.83, 121.33, 119.26, 110.36, 69.98, 94.82]
dataRoom = [24.06, 25.01, 23.80, 23.12, 22.96, 21.78, 17.99, 22.47, 22.75, 21.92]
topicPipe = "topicPipe"
topicRoom = "topicRoom"


def on_connect(client, userdata, flags, return_code):
    if return_code == 0:
        print("Connectection established")
    else:
        print("Could not connect, return code:", return_code)

def send(topic, data):
        result = client.publish(topic, data[i])
        status = result[0]
        if status == 0:
            print("Temp. "+ str(data[i]) + " is published to " + topic)
        else:
            print("Failed to send message to topic " + topic)
            if not client.is_connected():
                print("Client not connected, exiting...")
                return

broker_hostname = "localhost"
port = 1883 

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "Publisher1")
client.on_connect = on_connect

client.connect(broker_hostname, port)
client.loop_start()


try:
    for i in range (len(dataPipe)):
        time.sleep(1)
        send(topicPipe, dataPipe)
        send(topicRoom, dataRoom)
finally:
    client.disconnect()
    client.loop_stop()