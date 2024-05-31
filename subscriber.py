import paho.mqtt.client as mqtt
import time
from datetime import datetime

dataPipe = []
dataRoom = []
topicPipe = "topicPipe"
topicRoom = "topicRoom"
msgCount = 0
expectedMsgCount = 20

tempPipeMin = 70
tempRoomMin = 18
tempRoomMax = 25

criticalPipeFlag = False
criticalRoomFlag = False



def on_connect(client, userdata, flags, return_code):
    if return_code == 0:
        print("Connectection established")
        client.subscribe(topicPipe)
        client.subscribe(topicRoom)
    else:
        print("Could not connect, return code:", return_code)
        client.failed_connect = True



def on_message(client, userdata, message):

    timestamp = datetime.fromtimestamp(time.time())
    
    if message.topic == topicPipe:
        dataPipe.append(float(message.payload))
        print(timestamp, "Curr. pipe temp. = ", str(message.payload.decode("utf-8")), ", avg. pipe temp. = ", round(sum(dataPipe)/len(dataPipe), 2))

        global criticalPipeFlag
        if float(message.payload) < tempPipeMin and criticalPipeFlag == False:
            criticalPipeFlag = True
            print ("[WARNING!!!] Critical pipe temp. detected! (", float(message.payload), ")")
        elif float(message.payload) > tempPipeMin and criticalPipeFlag == True:
            criticalPipeFlag = False
            print ("[INFO] Pipe temp has returned to normal.")

    elif message.topic == topicRoom:
        dataRoom.append(float(message.payload))
        print(timestamp, "Curr. room temp. = ", str(message.payload.decode("utf-8")), ", avg. room temp. = ", round(sum(dataRoom)/len(dataRoom), 2))

        global criticalRoomFlag
        if (float(message.payload) < tempRoomMin or float(message.payload) > tempRoomMax) and criticalRoomFlag == False:
            criticalRoomFlag = True
            print ("[WARNING!!!] Critical room temp. detected! (", float(message.payload), ")")
        elif (float(message.payload) > tempRoomMin and float(message.payload) < tempRoomMax) and criticalRoomFlag == True:
            criticalRoomFlag = False
            print ("[INFO] Room temp has returned to normal.")

    global msgCount
    msgCount += 1



broker_hostname ="localhost"
port = 1883 

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "Subscriber1")
client.connect(broker_hostname)
client.on_connect = on_connect
client.on_message = on_message
client.failed_connect = False

client.loop_start()

try:
    while msgCount != expectedMsgCount and client.failed_connect == False:
        time.sleep(1)

    if client.failed_connect == True:
        print('Connection failed, exiting...')

finally:
    print('Connection terminated')
    client.disconnect()
    client.loop_stop()