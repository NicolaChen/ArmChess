import datetime
import json
import random
import threading

from paho.mqtt import client as mqtt_client


class Mqtt:

    def __init__(self):
        self.broker = "broker-cn.emqx.io"
        self.port = 1883
        self.topic = "esp32/test"
        self.client_id = None
        self.client = None
        self.r_dict = None
        self.setClientId()

    def setClientId(self):
        now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_number = random.randint(0, 1000)
        unique_number = str(now_time) + str(random_number)
        self.client_id = "python_controller_{0}".format(unique_number)

    def connectMqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT broker!")
            else:
                print("Failed to connect, return code %d" % rc)

        self.client = mqtt_client.Client(self.client_id)
        self.client.on_connect = on_connect
        self.client.connect(self.broker, self.port)

    def publish(self, msg):
        result = self.client.publish(self.topic, msg)
        if result[0] == 0:
            print("Mqtt publish message: {0}".format(msg))
        else:
            print("Failed to send message to topic {0}".format(self.topic))

    def subscribe(self):
        def on_message(client, userdata, msg):
            dict_json = json.loads(msg.payload.decode())
            if 'dev_id' in dict_json:
                self.r_dict = dict_json
                print("Receiving message '{0}: {1}' from {2}".format(self.r_dict['msg_code'],
                                                                     self.r_dict['msg'], self.r_dict['dev_id']))

        self.client.subscribe(self.topic)
        self.client.on_message = on_message

    def run(self):
        self.connectMqtt()
        self.subscribe()
        mqtt_thread = threading.Thread(target=self.client.loop_forever)
        mqtt_thread.setDaemon(True)
        mqtt_thread.start()
