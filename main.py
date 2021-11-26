#!bin/python

#: Importing good stuffs {{{
import os
from dotenv import load_dotenv
from paho.mqtt import client as mqtt_client
from read import dummy_data
#: }}}

#: Loading enviroment varables {{{
#: CHANNEL_ID,
#: MQTT_HOST,
#: MQTT_CLIENT_ID,
#: MQTT_USERNAME,
#: MQTT_PASSWORD,
#: T_TRANSPORT(websockets),
#: T_PORT(80),

"""
# Then enviroment varables can be used as
>>> os.getenv('CHANNEL_ID')
ABCDEF
"""

load_dotenv()
#: }}}


def get_topic():
    ''' return the publishable topic as per thinkspeak requirement '''

    return 'channels/' + str(os.getenv('CHANNEL_ID')) + '/publish'


def connect_mqtt() -> mqtt_client:
    '''
    This function connects to the
    MQTT broker and then returns the client
    '''

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT BROKER: {os.getenv('MQTT_HOST')}")
        else:
            print("Failed to connect.")

    client = mqtt_client.Client(
        os.getenv('MQTT_CLIENT_ID')
    )
    client.username_pw_set(
        os.getenv('MQTT_USERNAME'),
        os.getenv('MQTT_PASSWORD')
    )

    client.on_connect = on_connect
    client.connect(os.getenv('MQTT_HOST'))

    return client


def publish_data(client: mqtt_client, topic: str) -> None:
    ''' This function publishes the data to the broker '''

    while True:
        field_values = dummy_data()

        result = client.publish(topic, field_values, qos=2)

        if result[0] == 0:
            print('Successfull uploaded data')
        else:
            print('Something went wrong while uploading')


def run():
    ''' This function work as a main function to the file '''

    client = connect_mqtt()
    publish_data(client, get_topic())
    client.loop_forever()


if __name__ == '__main__':
    run()
