import sys
import paho.mqtt.client as mqtt
import json
import pytz
from dateutil.parser import isoparse
from database_manager import *
import datetime

sys.stderr.write("hi from worker!\n")

username = "hgm-maga@ttn"
password = "NNSXS.BUQAAO3FG77GWDTX6DHADX5FM6WNHMDRRSUIWIY.JH25PY3RE6FDWC4WMXOA5RC5YBK2RYQFBW5E52TZYSDHXI32LR7A"
public_adress = "nam1.cloud.thethings.network"
port = 1883
keepalive_interval = 0

keys = {}
maga_key = {
    'sysId': 1,
    'deviceId': 0,
    'aplication': 'Maga',
    'properties': [
        {'name': 'Manos limpias',
            'prop': 'clean_hands',
            'value': 0
        },
        {'name': 'manos sucias',
            'prop': 'dirty_hands',
            'value': 0
            },
        {'name': 'Consumo de guantes',
            'prop': 'box_chanes',
            'value': 0
            }    
    ],
    'location': [
        {'service': ''},
        {'area': ''},
        {'cubicle': ''},
        {'room': ''}
    ]
}
location = {
    'devices':[
        {'deviceId': 'maga-001',
         'service': 'uci',
         'area': 'none',
         'cubicle': 'none',
         'room': '1001'}
    ]
}
vumeter_key = {
            'sysId': 98,
            'aplication': 'Vumeter',
            'properties': [
                {'name': 'Decibeles',
                 'prop': 'db',
                }  
            ]
}
keys['maga_key'] = maga_key
keys['vumeter_key'] = vumeter_key


client = mqtt.Client()

class TtnClient:
    def __init__(self, client) :
        self._clear_json_input = {} # Initialize an empty dictionary to store JSON input
        self._client = client   # Store the client object
  
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+ str(rc))
        sys.stderr.write("Connected with result code " + str(rc) +  "\n")
        

    def on_message(self, client, userdata, message):
        mqtt_message = message # Store the received MQTT message
        payload = mqtt_message.payload # Extract the payload from the MQTT message
        text = payload.decode('utf-8') # Decode the payload as UTF-8 string
        json_input = json.loads(text) # Parse the JSON input from the decoded text
        uplink_message = json.dumps(json_input, indent=2, ensure_ascii=False) # Convert the JSON input back to string with formatting
        # print(uplink_message)
        if len(self._clear_json_input) == 0:
            self._clear_json_input = json_input 
        print("////////////////////////////////////////////////////")

    def suscribe_to_server(self):
        client.username_pw_set(username, password) # Set the username and password for authentication
        client.connect(public_adress, port, keepalive_interval) # Connect to the server using the provided address, port, and keepalive interval
        self._client.on_connect = self.on_connect
        self._client.on_message = self.on_message
        self._client.subscribe("v3/" + username + "/devices/#") # Subscribe to the specified topic

    def listen_ttn(self):
        stop_flag = True
        while stop_flag:
            client.loop() # Process network events and messages

            if len(self._clear_json_input) != 0:
                output_json = self._clear_json_input # Store the cleared JSON input
                self._clear_json_input = {} # Reset the cleared JSON input
                stop_flag = False # Stop the loop
                # print(output_json)
                return output_json

class Worker:
    def __init__(self, mongodb):
        self._mongodb = mongodb # Store the MongoDB object

    def _decoder(self, data_bytes):
        length = int(len(data_bytes)/2) # Calculate the length based on the byte array
        decoded_data = [] #99 only for test before change maga's firmware
        low_byte = 0
        high_byte = 0

        for i in range(length):
            decoded_data.append((data_bytes[low_byte] << 8) | data_bytes[high_byte + 1])
            # print('decoded_data[',i,']', 'bytes[',low_byte,']', 'bytes[',high_byte+1,']')
            low_byte+=2
            high_byte+=2
        print('DECODED PAYLOAD')
        print(decoded_data)
        return decoded_data     

    def _raw_data(self, data):
        try:
                end_device_id = data["end_device_ids"]["device_id"] # Extract the end device ID
                decoder_payload = data['uplink_message']["decoded_payload"]['data'] # Extract the decoded payload data
                # getway_id = data['uplink_message']['rx_metadata'][0]['gateway_ids']['gateway_id']
                # time = data['uplink_message']['rx_metadata'][0]['time']
                # timestamp = data['uplink_message']['rx_metadata'][0]["timestamp"]
                print('RAW DATA')
                print(end_device_id)
                print(decoder_payload)
                
                return {'devId': end_device_id, 'payload': decoder_payload}
        except Exception as e:
            print('somthing wrong on raw_data ', e)
            pass

    def get_timestamp(self):
        current_datetime = datetime.datetime.now()
        # hour = current_datetime.hour
        hour = current_datetime.hour
        day = current_datetime.day
        weekday = current_datetime.weekday()
        month = current_datetime.month
        year = current_datetime.year

        week = datetime.date(year, month, day)
        week = week.isocalendar()[1]
        week = int(week)

        return hour, day, week, weekday, month, year

    def process_data(self, data):
        try:
            raw_data = self._raw_data(data) # Get the raw data from the provided data
            device_id = raw_data['devId'] # Extract the device ID from raw data
            payload = self._decoder(raw_data['payload']) # Decode the payload from raw data
            sys_id = payload[0] # Extract the system ID from the payload

            keys_list = list(keys) # Convert the keys dictionary into a list of keys
            output ={} # Initialize an empty dictionary for the output
            # print('PROCESS DATA-----------------------')
            # print('sysID: ', sys_id)
            # print('deviceID: ', device_id)
            # print('payload: ', payload)


            for key in keys_list:
                if( keys[key]['sysId'] == sys_id):
                    output = keys[key].copy() # Copy the key details from the keys dictionary to the output dictionary
                    output['deviceId'] = device_id # Set the device ID in the output dictionary
                    for index, i in enumerate(output['properties']):
                        output['properties'][index]['value'] = payload[index + 1]
                        # print (i)
            print('PROCESS DATA-----------------------')
            # sysId, id, aplication, hour, day, weekday, month, year, props
            sysId = output['sysId']
            id = output['deviceId']
            aplication = output['aplication']
            hour, day,week, weekday, month, year = self.get_timestamp()
            props = output['properties']
            # print(sysId, id, aplication, hour, day, weekday, month, year, props)

            try:
                location = get_device_location(id)
            except Exception as e:
                print('somthing wrong on get_raw_data, get_device_location ', e)
            pass
            
            print('Current Time = ', datetime.datetime.now())
            update_daily(sysId, id, aplication, hour, day, weekday, week, month, year, props, location)

        except Exception as e:
            print('somthing wrong on get_raw_data ', e)
        pass

    def updateDB(self, previous_hour, current_hour):

        if current_hour == 0:
            hour, day, week, weekday, month, year = self.get_timestamp()
            new_timestamp = datetime.datetime(year, month, day, hour)
            new_timestamp = new_timestamp - datetime.timedelta(hours=1)
            previous_hour = new_timestamp.hour
            day = new_timestamp.day
            weekday = new_timestamp.weekday
            month = new_timestamp.month
            year = new_timestamp.year
            week = datetime.date(year, month, day)
            week = week.isocalendar()[1]
            week = int(week)
        else:
            hour, day, week, weekday, month, year = self.get_timestamp()

        get_consolidated('daily', day, weekday, week, month, year)
        get_consolidated('weekly', day, weekday, week, month, year)
        get_consolidated('monthly', day, weekday, week, month, year)
        get_consolidated('yearly', day, weekday, week, month, year)
        update_services('hour', year, month, week, day, previous_hour)
        update_services('day', year, month, week, day, previous_hour)
        update_services('week', year, month, week, day, previous_hour)
        update_services('month', year, month, week, day, previous_hour)

def main():
    print("------------------------------START----------------------------------------------------------")
    client_ttn = TtnClient(client)
    client_ttn.suscribe_to_server()
    worker = Worker(1)
    previous_hour = datetime.datetime.now().hour

    while True:
        data_to_process = client_ttn.listen_ttn()
        worker.process_data(data_to_process)
        current_hour = datetime.datetime.now().hour
        if(current_hour != previous_hour):
            worker.updateDB(previous_hour, current_hour)
            previous_hour = current_hour

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)





