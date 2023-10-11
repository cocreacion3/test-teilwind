import pymongo
from pymongo import MongoClient
import json
from bson import ObjectId
import copy
import time
import random
import sys
import logging


MONGO_URI = "mongodb://127.0.0.1:28018/"
MONGO_TIME_OUT = 2000

iot_db = 'maga'
consolidated_devices_db = 'consolidated_devices'
consolidated_devices_collection = 'consolidated_devices_collection'
devices_collection = 'devices'



# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s [%(levelname)s] %(message)s',
#     handlers=[
#         logging.StreamHandler(),  # Log to console
#         logging.FileHandler('/app/logs/app.log')  # Log to file within the container
#     ]
# )


print('DATABASE MANAGER STARTED')

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)
    
def print_json(results):
    documents = [doc for doc in results]
    json_str = json.dumps(documents, indent=4, cls=JSONEncoder)
    print(json_str)

def delete_all():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME_OUT)
        print("connection successful")

        db = client['maga']  # new db
        collection = db['devices']  # new collection
        collection.delete_many({})

        result = collection.find({})
        print("Datos en DB")
        print_json(result)

        client.close()

    except pymongo.errors.ServerSelectionTimeoutError as error:
        print("Timeout")
        pass
    except pymongo.errors.ConnectionFailure as errorConnection:
        print("Connection failure")

def add_test(id, hour, day, weekday, week, month, year ):
    sysId = 1
    # id = 'test-device-001'
    aplication = 'Maga'
    props = [
                    {
                        "name": "Manos limpias",
                        "prop": "clean_hands",
                        "value": 1#random.randrange(1,10,1)
                    },
                    {
                        "name": "manos sucias",
                        "prop": "dirty_hands",
                        "value": 1#random.randrange(1,10,1)
                    },
                    {
                        "name": "Consumo de guantes",
                        "prop": "box_chanes",
                        "value": 0               #random.randrange(1,100,1)
                    }
                ]
    location = get_device_location(id)
    update_daily(sysId, id, aplication, hour, day, weekday, week, month, year, props, location)

def print_device(id):
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME_OUT)
        print("connection successful")

        db = client['maga']  # new db
        collection = db['devices']  # new collection

    #/////////////////////////////////////////////////////////////////////////////////////////////////////////



        if collection.count_documents({'deviceId': id}) > 0:
            print("[!] El dispositivo existe")

            filter = {'deviceId': id}
            # //////
            filter = {}
            result = collection.find(filter)
            result = collection.find()
            print_json(result)
            client.close()

    except pymongo.errors.ServerSelectionTimeoutError as error:
        print("Timeout")
        pass
    except pymongo.errors.ConnectionFailure as errorConnection:
        print("Connection failure")

def add_device(deviceId, service, area, cubicle, room, delete_all):

    new_device = {
        'deviceId': deviceId,
        'service': service,
        'area': area,
        'cubicle': cubicle,
        'room': room
    }

    location = {
        'devices':[
            {'deviceId': deviceId,
            'service': service,
            'area': area,
            'cubicle': cubicle,
            'room': room}
        ]
    }

    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME_OUT)
        print("connection successful")
        db = client['location_devices']  # new db
        collection = db['location_devices']  # new collection

        if collection.count_documents({'devices': {'$exists': True}}) > 0:

            if collection.count_documents({'devices.deviceId': deviceId}) > 0:
                print('[!] Device already exist!')
                return "Device already exist"

            else:
                print('[!] Generating device!')
                
                collection.update_one({}, {'$push': {'devices': new_device}})
        else:
            collection.insert_one(location)



        doc_finder = collection.find({})
        if delete_all:
            collection.delete_many({})
        print_json(doc_finder)
        client.close()
        return "Device created"
    except pymongo.errors.ServerSelectionTimeoutError as error:
        print("Timeout")
        pass
    except pymongo.errors.ConnectionFailure as errorConnection:
        print("Connection failure")

def get_device_location(deviceId, all=False):
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME_OUT)
        print("connection successful")
        db = client['location_devices']  # new db
        collection = db['location_devices']  # new collection

        if all:
            if collection.count_documents({'devices': {'$exists': True}}) > 0:
                result = collection.find_one({})
                if result is not None:
                    devices_list = result['devices']
                    # print(devices_list)
                    client.close()
                    return devices_list

        if collection.count_documents({'devices.deviceId': deviceId}) > 0:
            result = collection.find_one({'devices.deviceId': deviceId})
            if result is not None:
                devices_list = result['devices']
                # print(devices_list)
                for index_list, i in enumerate(devices_list):
                    # print(daily_list[index_list]['hour'])
                    if devices_list[index_list]['deviceId'] == deviceId:
                        # print('hora encontrada', index_list)
                        device_index = index_list
                        print("LOCATION INFO")
                        del devices_list[index_list]['deviceId']
                        print(devices_list[index_list])
                        client.close()
                        return devices_list[index_list]
        client.close()
    except pymongo.errors.ServerSelectionTimeoutError as error:
        print("Timeout")
        pass
    except pymongo.errors.ConnectionFailure as errorConnection:
        print("Connection failure")

def update_daily(sysId, id, aplication, hour, day, weekday, week, month, year, props, location):
    print('ON UPDATE DAILY')
    print(sysId, id, aplication, hour, day, weekday, week, month, year)
    print(props)
    print(location)
    logging.info('sysid= %s id= %s app= %s h: %s d: %s wd: %s w: %s m: %s y: %s', sysId, id, aplication, hour, day, weekday, week, month, year)
    logging.info(props)

    if location is None:
        return

    daily_data = {
        "hour": hour,
        "day": day,
        "weekday": weekday,
        "week": week,
        "month": month,
        "year": year,
        "shift": '',
        "properties": props,
    }
          
    device = {"sysId": sysId,
            "deviceId": id,
            "aplication": aplication,
            "location": location,
            "daily": [
                {
                    "hour": hour,
                    "day": day,
                    "weekday": weekday,
                    "week": week,
                    "month": month,
                    "year": year,
                    "shift": '',
                    "properties": props   
                }
            ],
            "dailyDayConsolidated":[],
            "dailyNigthConsolidated":[],
            "weeklyDayConsolidated":[],
            "weeklyNigthConsolidated":[],
            "monthlyDayConsolidated":[],
            "monthlyNigthConsolidated":[],
            "yearlyDayConsolidated":[],
            "yearlyNigthConsolidated":[]
            }
    
    end_of_day_shift = 17
    if hour > end_of_day_shift:
        daily_data['shift'] = 'nigth'
        device['daily'][0]['shift'] = 'night'
    else:
        daily_data['shift'] = 'day'
        device['daily'][0]['shift'] = 'day'

    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME_OUT)
        print("connection successful")

        db = client['maga']  # new db
        collection = db['devices']  # new collection

    #/////////////////////////////////////////////////////////////////////////////////////////////////////////

        if collection.count_documents({'deviceId': id}) > 0:
            print("[!] El dispositivo existe")

            filter = {'deviceId': id}
            # //////
            result = collection.find_one(filter)
            # print(result)

            if result is not None:
                print('ACTUALIZAR')
                daily_list = result['daily']

                verify_hour = False
                for index_list, i in enumerate(daily_list):
                    # print("holi")
                    if daily_list[index_list]['hour'] == hour and daily_list[index_list]['day'] == day and daily_list[index_list]['week'] == week and daily_list[index_list]['month'] == month and daily_list[index_list]['year'] == year:
                        hour_index = index_list
                        verify_hour = True
                        break

                if verify_hour:
                    update={} 
                    for index, prop in enumerate(props):
                        update['daily.{}.properties.{}.value'.format(hour_index, index)] = props[index]['value']
                    collection.update_one(filter, {'$inc': update})

                else:
                    collection.update_one({'deviceId': id}, {'$push': {'daily': daily_data}})
          
        else:
            print("[!] Creando dispositivo")
            collection.insert_one(device)

    #////////////////////////////////////////////////////////////////////////////////////////////////////////


        client.close()

    except pymongo.errors.ServerSelectionTimeoutError as error:
        print("Timeout")
        pass
    except pymongo.errors.ConnectionFailure as errorConnection:
        print("Connection failure")

def get_daily_data(id, hour, day, weekday, week, month, year):
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME_OUT)
        print("connection successful")
        db = client['maga']  # new db
        collection = db['devices']  # new collection

        filter = {'deviceId': id, 'daily.hour': hour, 'daily.day': day,
                'daily.weekday': weekday,'daily.week': week, 'daily.month': month, 'daily.year': year}
        doc_finder = collection.find_one(filter)

        if collection.count_documents(filter) > 0:
            print("[!] Documento encontrado")
            # print_json(doc_finder)
            # print(doc_finder)
            client.close()
            return doc_finder
        else:
            print("nope")



        client.close()   
    except pymongo.errors.ServerSelectionTimeoutError as error:
        print("Timeout")
        pass
    except pymongo.errors.ConnectionFailure as errorConnection:
        print("Connection failure")

def get_data(id):
    # print("----------Start get_data----------")
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME_OUT)
        # print("connection successful")
        db = client['maga']  # new db
        collection = db['devices']  # new collection


        filter = {'deviceId': id}
        # print(">>>>>", filter)
        doc_finder = collection.find_one(filter)
        # print(doc_finder)

        if collection.count_documents(filter) > 0:
            # print("[!] Documento encontrado")
            # print_json(doc_finder)
            # print(doc_finder)
            # print("----------End get_data----------")
            client.close()
            return doc_finder
        else:
            print("File not found")
            print("----------End get_data----------")



        client.close()   
    except pymongo.errors.ServerSelectionTimeoutError as error:
        print("Timeout")
        pass
    except pymongo.errors.ConnectionFailure as errorConnection:
        print("Connection failure")
    



def add_consolidated_data(temporality, shift_day_data, shift_nigth_data, id, day, weekday,week, month, year):
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME_OUT)
        print("connection successful")

        db = client['maga']  # new db
        collection = db['devices']  # new collection
        if temporality == 'daily':
            daily_shift_day_consolidated = {
                                "day": day,
                                "weekday": weekday,
                                "week": week,
                                "month": month,
                                "year": year,
                                "shift": 'day',
                                "properties": shift_day_data,
                            }
            daily_shift_nigth_consolidated = {
                                "day": day,
                                "weekday": weekday,
                                "week": week,
                                "month": month,
                                "year": year,
                                "shift": 'nigth',
                                "properties": shift_nigth_data,
                            }


            filter = {'deviceId': id}
            result = collection.find_one(filter)
            print('RESULTADO')
            # print(result)
    
            if len(result['dailyDayConsolidated']) <= 0:
                print('creating day consolidated')
                collection.update_one({'deviceId': id}, {'$push': {'dailyDayConsolidated': daily_shift_day_consolidated}})
            consolidated_verify = True
            print(result['dailyDayConsolidated'])
            for index, condolidated in enumerate(result['dailyDayConsolidated']):
                if result['dailyDayConsolidated'][index]['day'] == day and result['dailyDayConsolidated'][index]['weekday'] == weekday and result['dailyDayConsolidated'][index]['week'] == week and result['dailyDayConsolidated'][index]['month'] == month and result['dailyDayConsolidated'][index]['year'] == year:
                    print('existe')
                    consolidated_verify = True
                    break
                else:
                    print('no existe')
                    consolidated_verify = False

            if not consolidated_verify:
                print('[!] Day consolidated')
                collection.update_one({'deviceId': id}, {'$push': {'dailyDayConsolidated': daily_shift_day_consolidated}})
                print('[!] Nigth consolidated')
                collection.update_one({'deviceId': id}, {'$push': {'dailyNigthConsolidated': daily_shift_nigth_consolidated}}) 

        client.close()
    except pymongo.errors.ServerSelectionTimeoutError as error:
        print("Timeout")
        pass
    except pymongo.errors.ConnectionFailure as errorConnection:
        print("Connection failure")
        pass
            
def update_day_consolidated(hour, day, weekday, week, month, year):
    try:
        devices = get_device_location({}, True)
        deviceId = []
        consolidated_props = {}

        for device in range(len(devices)):
            deviceId.append(devices[device]['deviceId'])
    except Exception as e:
        print('somthing wrong', e)
        pass

    for device in range(len(deviceId)):
        

        try:
            device_data = get_daily_data(deviceId[device], hour, day, weekday, week, month, year)
            device_data_copy_shift_day = copy.deepcopy(device_data)
            device_data_copy_shift_nigth = copy.deepcopy(device_data)


            device_properties = device_data['daily'][0]['properties']

            device_properties_shift_day = device_data_copy_shift_day['daily'][0]['properties']
            device_properties_shift_nigth = device_data_copy_shift_nigth['daily'][0]['properties']
            print(">>>>>>>RAW DATA<<<<<<")
            # print(device_data)
            print("---------------------")


            consolidated_props_shift_day = device_properties_shift_day
            consolidated_props_shift_nigth = device_properties_shift_nigth
            # print(device_data)
            for prop in range(len(device_properties)):
                consolidated_props_shift_day[prop]['value'] = 0
                consolidated_props_shift_nigth[prop]['value'] = 0
            # device_data = get_daily_data(6, deviceId[device])
            print("------------------------------------")
            print('DEVICE:', deviceId[device])
            print("------------------------------------")

            for hour in range(24):
                try:
                    for prop in range(len(device_properties)):
                        # consolidated_props_shift_day[prop]['value'] += device_data['daily'][hour]['properties'][0]['value']
                        if device_data['daily'][hour]['shift'] == 'day':
                            consolidated_props_shift_day[prop]['value'] += device_data['daily'][hour]['properties'][0]['value']

                        if device_data['daily'][hour]['shift'] == 'night':
                            consolidated_props_shift_nigth[prop]['value'] += device_data['daily'][hour]['properties'][0]['value']

                            # print(device_data['daily'][hour]['shift'])
                        # print(device_data)
                    # print('----------------------CONSOLIDATED DATA----------------------------')
                    # print('----------------------DAY----------------------')
                    # print(consolidated_props_shift_day)
                    # print('----------------------NIGTH----------------------')
                    # print(consolidated_props_shift_nigth)
                    add_consolidated_data('daily', consolidated_props_shift_day, consolidated_props_shift_nigth, deviceId[device], day, weekday, week, month, year)
                        
                except Exception as e:
                    # print('somthing wrong hours ', e)
                    pass
        except Exception as e:
            # print('somthing wrong id', e)
            pass

def update_week_consolidated(periodicity):
    try:
        devices = get_device_location({}, True)
        deviceId = []
        consolidated_props = {}

        for device in range(len(devices)):
            deviceId.append(devices[device]['deviceId'])
    except Exception as e:
        print('somthing wrong', e)
        pass

    for device in range(len(deviceId)):
        

        try:
            device_data = get_data(deviceId[device])
            device_data_copy_shift_day = copy.deepcopy(device_data)
            device_data_copy_shift_nigth = copy.deepcopy(device_data)

            device_properties = device_data['daily'][0]['properties']

            device_properties_shift_day = device_data_copy_shift_day['daily'][0]['properties']
            device_properties_shift_nigth = device_data_copy_shift_nigth['daily'][0]['properties']
            print(">>>>>>>RAW DATA<<<<<<")
            # print(device_data)
            print("---------------------")


            consolidated_props_shift_day = device_properties_shift_day
            consolidated_props_shift_nigth = device_properties_shift_nigth
            # print(device_data)
            for prop in range(len(device_properties)):
                consolidated_props_shift_day[prop]['value'] = 0
                consolidated_props_shift_nigth[prop]['value'] = 0
            # device_data = get_daily_data(6, deviceId[device])
            print("------------------------------------")
            print('DEVICE:', deviceId[device])
            print("------------------------------------")

            if periodicity == 'daily':
                for hour in range(24):
                    try:
                        for prop in range(len(device_properties)):
                            # consolidated_props_shift_day[prop]['value'] += device_data['daily'][hour]['properties'][0]['value']
                            if device_data['daily'][hour]['shift'] == 'day':
                                consolidated_props_shift_day[prop]['value'] += device_data['daily'][hour]['properties'][0]['value']

                            if device_data['daily'][hour]['shift'] == 'night':
                                consolidated_props_shift_nigth[prop]['value'] += device_data['daily'][hour]['properties'][0]['value']

                                # print(device_data['daily'][hour]['shift'])
                            # print(device_data)
                            
                        print('----------------------CONSOLIDATED DATA----------------------------')
                        print('----------------------DAY----------------------')
                        print(consolidated_props_shift_day)
                        print('----------------------NIGTH----------------------')
                        print(consolidated_props_shift_nigth)
                    except Exception as e:
                        print('somthing wrong hours ', e)
                        pass
            
            if periodicity == 'weekly':
                for day in range(1):
                    try:
                        for prop in range(len(device_properties)):
                            # consolidated_props_shift_day[prop]['value'] += device_data['daily'][hour]['properties'][0]['value']
                            if device_data['daily'][day]['shift'] == 'day':
                                # consolidated_props_shift_day[prop]['value'] += device_data['daily'][hour]['properties'][0]['value']
                                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                                print(device_data['dailyDayConsolidated'])

                            # if device_data['daily'][hour]['shift'] == 'night':
                                # consolidated_props_shift_nigth[prop]['value'] += device_data['daily'][hour]['properties'][0]['value']

                                # print(device_data['daily'][hour]['shift'])
                            # print(device_data)
                            
                        # print('----------------------CONSOLIDATED DATA----------------------------')
                        # print('----------------------DAY----------------------')
                        # print(consolidated_props_shift_day)
                        # print('----------------------NIGTH----------------------')
                        # print(consolidated_props_shift_nigth)
                    except Exception as e:
                        # print('somthing wrong hours ', e)
                        pass        
        except Exception as e:
            # print('somthing wrong id', e)
            pass
        # add_consolidated_data('daily', 1, consolidated_props_shift_day, consolidated_props_shift_nigth, deviceId[device], day, weekday, month, year)



def update_data(periodicity,device_data, shift_day_data, shift_nigth_data, id, day, weekday, week, month, year, time_type_day, time_type_nigth):
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME_OUT)
        print("connection successful")

        db = client['maga']  # new db
        collection = db['devices']  # new collection

        
        if periodicity == 'daily':
            print("on dailyyyy")
            shift_day_consolidated = {
                    "hour": 0,
                    "day": day,
                    "weekday": weekday,
                    "week": week,
                    "month": month,
                    "year": year,
                    "shift": 'day',
                    "properties": shift_day_data,
                }
            shift_nigth_consolidated = {
                                "hour": 0,
                                "day": day,
                                "weekday": weekday,
                                "week": week,
                                "month": month,
                                "year": year,
                                "shift": 'nigth',
                                "properties": shift_nigth_data,
                            }


            new_device = False
            if len(device_data['dailyDayConsolidated']) <= 0:
                print('CREATING NEW INPUT ON DAILY')
                for index in range(len(time_type_day)):
                    shift_day_consolidated['hour'] = time_type_day[index]
                    shift_day_consolidated['properties'] = shift_day_data[index]                                                                     
                    collection.update_one({'deviceId': id}, {'$push': {'dailyDayConsolidated': {'$each': [shift_day_consolidated], '$position': 0}}})
                for index in range(len(time_type_nigth)):
                    shift_day_consolidated['hour'] = time_type_nigth[index]
                    shift_day_consolidated['properties'] = shift_nigth_data[index]
                    collection.update_one({'deviceId': id}, {'$push': {'dailyNigthConsolidated': {'$each': [shift_nigth_consolidated], '$position': 0}}})
                new_device = True

            new_input = True
            if not new_device:
                for index in range(len(device_data['dailyDayConsolidated'])):
                    if device_data['dailyDayConsolidated'][index]['day'] == day and device_data['dailyDayConsolidated'][index]['month'] == month and device_data['dailyDayConsolidated'][index]['year'] == year:
                        print("update input")
                        for index in range(len(time_type_day)):
                            shift_day_consolidated['hour'] = time_type_day[index]
                            shift_day_consolidated['properties'] = shift_day_data[index]
                            collection.update_one({'deviceId': id}, {'$set': {'dailyDayConsolidated.' + str(index): shift_day_consolidated}})

                        for index in range(len(time_type_nigth)):
                            shift_nigth_consolidated['hour'] = time_type_nigth[index]
                            shift_nigth_consolidated['properties'] = shift_nigth_data[index]
                            collection.update_one({'deviceId': id}, {'$set': {'dailyNigthConsolidated.' + str(index): shift_nigth_consolidated}})
                        new_input = False
                if new_input:
                    for index in range(len(time_type_day)):
                        shift_day_consolidated['hour'] = time_type_day[index]
                        shift_day_consolidated['properties'] = shift_day_data[index]
                        collection.update_one({'deviceId': id}, {'$push': {'dailyDayConsolidated': {'$each': [shift_day_consolidated], '$position': 0}}})
                    for index in range(len(time_type_nigth)):
                        shift_day_consolidated['hour'] = time_type_nigth[index]
                        shift_day_consolidated['properties'] = shift_nigth_data[index]
                        collection.update_one({'deviceId': id}, {'$push': {'dailyNigthConsolidated': {'$each': [shift_nigth_consolidated], '$position': 0}}})



        if periodicity == 'weekly':
            print("on weekly")
            shift_day_consolidated = {
                    "day": 0,
                    "week": week,
                    "month": month,
                    "year": year,
                    "shift": 'day',
                    "properties": shift_day_data,
                }
            shift_nigth_consolidated = {
                                "day": 0,
                                "week": week,
                                "month": month,
                                "year": year,
                                "shift": 'nigth',
                                "properties": shift_nigth_data,
                            }
            
            new_device = False
            if len(device_data['weeklyDayConsolidated']) <= 0:
                print('CREATING NEW INPUT ON WEEKLY')
                for index in range(len(time_type_day)):
                    shift_day_consolidated['day'] = time_type_day[index]
                    shift_day_consolidated['properties'] = shift_day_data[index]
                    collection.update_one({'deviceId': id}, {'$push': {'weeklyDayConsolidated': {'$each': [shift_day_consolidated], '$position': 0}}})
                for index in range(len(time_type_nigth)):
                    shift_day_consolidated['day'] = time_type_nigth[index]
                    shift_day_consolidated['properties'] = shift_nigth_data[index]
                    collection.update_one({'deviceId': id}, {'$push': {'weeklyNigthConsolidated': {'$each': [shift_nigth_consolidated], '$position': 0}}})
                new_device = True

            new_input = True
            if not new_device:
                print(shift_nigth_consolidated)
                for index in range(len(device_data['weeklyDayConsolidated'])):
                    if device_data['weeklyDayConsolidated'][index]['week'] == week and device_data['weeklyDayConsolidated'][index]['month'] == month and device_data['weeklyDayConsolidated'][index]['year'] == year:
                        print("update input")
                        for index in range(len(time_type_day)):
                            shift_day_consolidated['day'] = time_type_day[index]
                            shift_day_consolidated['properties'] = shift_day_data[index]
                            collection.update_one({'deviceId': id}, {'$set': {'weeklyDayConsolidated.' + str(index): shift_day_consolidated}})

                        for index in range(len(time_type_nigth)):
                            shift_nigth_consolidated['day'] = time_type_nigth[index]
                            shift_nigth_consolidated['properties'] = shift_nigth_data[index]
                            collection.update_one({'deviceId': id}, {'$set': {'weeklyNigthConsolidated.' + str(index): shift_nigth_consolidated}})
                        new_input = False
                if new_input:
                    for index in range(len(time_type_day)):
                        shift_day_consolidated['day'] = time_type_day[index]
                        shift_day_consolidated['properties'] = shift_day_data[index]
                        collection.update_one({'deviceId': id}, {'$push': {'weeklyDayConsolidated': {'$each': [shift_day_consolidated], '$position': 0}}})
                    for index in range(len(time_type_nigth)):
                        shift_day_consolidated['day'] = time_type_nigth[index]
                        shift_day_consolidated['properties'] = shift_nigth_data[index]
                        collection.update_one({'deviceId': id}, {'$push': {'weeklyNigthConsolidated': {'$each': [shift_nigth_consolidated], '$position': 0}}})


        if periodicity == 'monthly':
            print("on monthly")
            shift_day_consolidated = {
                    "week": 0,
                    "month": month,
                    "year": year,
                    "shift": 'day',
                    "properties": shift_day_data,
                }
            shift_nigth_consolidated = {
                                "week": 0,
                                "month": month,
                                "year": year,
                                "shift": 'nigth',
                                "properties": shift_nigth_data,
                            }
        
            new_device = False
            if len(device_data['monthlyDayConsolidated']) <= 0:
                print('CREATING NEW INPUT ON WEEKLY')
                for index in range(len(time_type_day)):
                    shift_day_consolidated['week'] = time_type_day[index]
                    shift_day_consolidated['properties'] = shift_day_data[index]
                    collection.update_one({'deviceId': id}, {'$push': {'monthlyDayConsolidated': {'$each': [shift_day_consolidated], '$position': 0}}})
                for index in range(len(time_type_nigth)):
                    shift_day_consolidated['week'] = time_type_nigth[index]
                    shift_day_consolidated['properties'] = shift_nigth_data[index]
                    collection.update_one({'deviceId': id}, {'$push': {'monthlyNigthConsolidated': {'$each': [shift_nigth_consolidated], '$position': 0}}})
                new_device = True

            new_input = True
            if not new_device:
                print(shift_nigth_consolidated)
                for index in range(len(device_data['monthlyDayConsolidated'])):
                    if device_data['monthlyDayConsolidated'][index]['month'] == month and device_data['monthlyDayConsolidated'][index]['year'] == year:
                        print("update input")
                        for index in range(len(time_type_day)):
                            shift_day_consolidated['week'] = time_type_day[index]
                            shift_day_consolidated['properties'] = shift_day_data[index]
                            collection.update_one({'deviceId': id}, {'$set': {'monthlyDayConsolidated.' + str(index): shift_day_consolidated}})

                        for index in range(len(time_type_nigth)):
                            shift_nigth_consolidated['week'] = time_type_nigth[index]
                            shift_nigth_consolidated['properties'] = shift_nigth_data[index]
                            collection.update_one({'deviceId': id}, {'$set': {'monthlyNigthConsolidated.' + str(index): shift_nigth_consolidated}})
                        new_input = False
                if new_input:
                    for index in range(len(time_type_day)):
                        shift_day_consolidated['week'] = time_type_day[index]
                        shift_day_consolidated['properties'] = shift_day_data[index]
                        collection.update_one({'deviceId': id}, {'$push': {'monthlyDayConsolidated': {'$each': [shift_day_consolidated], '$position': 0}}})
                    for index in range(len(time_type_nigth)):
                        shift_day_consolidated['week'] = time_type_nigth[index]
                        shift_day_consolidated['properties'] = shift_nigth_data[index]
                        collection.update_one({'deviceId': id}, {'$push': {'monthlyNigthConsolidated': {'$each': [shift_nigth_consolidated], '$position': 0}}})
        

        if periodicity == 'yearly':
            print("on yearly")
            shift_day_consolidated = {
                    "month": 0,
                    "year": year,
                    "shift": 'day',
                    "properties": shift_day_data,
                }
            shift_nigth_consolidated = {
                                "month": 0,
                                "year": year,
                                "shift": 'nigth',
                                "properties": shift_nigth_data,
                            }
        
            new_device = False
            if len(device_data['yearlyDayConsolidated']) <= 0:
                print('CREATING NEW INPUT ON WEEKLY')
                for index in range(len(time_type_day)):
                    shift_day_consolidated['month'] = time_type_day[index]
                    shift_day_consolidated['properties'] = shift_day_data[index]
                    collection.update_one({'deviceId': id}, {'$push': {'yearlyDayConsolidated': {'$each': [shift_day_consolidated], '$position': 0}}})
                for index in range(len(time_type_nigth)):
                    shift_day_consolidated['month'] = time_type_nigth[index]
                    shift_day_consolidated['properties'] = shift_nigth_data[index]
                    collection.update_one({'deviceId': id}, {'$push': {'yearlyNigthConsolidated': {'$each': [shift_nigth_consolidated], '$position': 0}}})
                new_device = True

            new_input = True
            if not new_device:
                print(shift_nigth_consolidated)
                for index in range(len(device_data['yearlyDayConsolidated'])):
                    if device_data['yearlyDayConsolidated'][index]['year'] == year:
                        print("update input")
                        for index in range(len(time_type_day)):
                            shift_day_consolidated['month'] = time_type_day[index]
                            shift_day_consolidated['properties'] = shift_day_data[index]
                            collection.update_one({'deviceId': id}, {'$set': {'yearlyDayConsolidated.' + str(index): shift_day_consolidated}})

                        for index in range(len(time_type_nigth)):
                            shift_nigth_consolidated['month'] = time_type_nigth[index]
                            shift_nigth_consolidated['properties'] = shift_nigth_data[index]
                            collection.update_one({'deviceId': id}, {'$set': {'yearlyNigthConsolidated.' + str(index): shift_nigth_consolidated}})
                        new_input = False
                if new_input:
                    for index in range(len(time_type_day)):
                        shift_day_consolidated['month'] = time_type_day[index]
                        shift_day_consolidated['properties'] = shift_day_data[index]
                        collection.update_one({'deviceId': id}, {'$push': {'yearlyDayConsolidated': {'$each': [shift_day_consolidated], '$position': 0}}})
                    for index in range(len(time_type_nigth)):
                        shift_day_consolidated['month'] = time_type_nigth[index]
                        shift_day_consolidated['properties'] = shift_nigth_data[index]
                        collection.update_one({'deviceId': id}, {'$push': {'yearlyNigthConsolidated': {'$each': [shift_nigth_consolidated], '$position': 0}}})
        
        client.close()
    except pymongo.errors.ServerSelectionTimeoutError as error:
        print("Timeout")
        pass
    except pymongo.errors.ConnectionFailure as errorConnection:
        print("Connection failure")
        pass

def get_consolidated(periodicity, day, weekday, week, month, year):
    print("--------------------START GET_CONSOLIDATED--------------------")
    try:
        devices = get_device_location({}, True)
        deviceId = []

        for device in range(len(devices)):
            deviceId.append(devices[device]['deviceId'])
            print(">>>>>>>>>>>>>>>>>>>>", devices[device]['deviceId'])
    except Exception as e:
        print('somthing wrong', e)
        pass

    data_day = []
    data_nigth = []
    time_type_day = []
    time_type_nigth = []

    for device in range(len(deviceId)):
        try:

            #////////////////////////////////////////////////////////////////////////////////////////////
            device_data = get_data(deviceId[device])
            device_data_copy_shift_day = copy.deepcopy(device_data)
            device_data_copy_shift_nigth = copy.deepcopy(device_data)

            device_properties = device_data['daily'][0]['properties']

            device_properties_shift_day = device_data_copy_shift_day['daily'][0]['properties']
            device_properties_shift_nigth = device_data_copy_shift_nigth['daily'][0]['properties']


            consolidated_props_shift_day = device_properties_shift_day
            consolidated_props_shift_nigth = device_properties_shift_nigth

            for prop in range(len(device_properties)):
                consolidated_props_shift_day[prop]['value'] = 0
                consolidated_props_shift_nigth[prop]['value'] = 0


            #////////////////////////////////////////////////////////////////////////////////////////////

            if periodicity == 'daily':
                print('on daily')
                #GET DAYS BY SHIFT
                device_data['daily'] = sorted(device_data['daily'], key=lambda x: x['day'])
                # print(json.dumps(device_data['daily'], indent=4))
                for index, data in enumerate(device_data['daily']):
                    if device_data['daily'][index]['day'] == day and device_data['daily'][index]['month'] == month and device_data['daily'][index]['year'] == year:
                        if device_data['daily'][index]['shift'] == 'day':
                            time_type_day.append(device_data['daily'][index]['hour'])
                        if device_data['daily'][index]['shift'] == 'nigth':
                            time_type_nigth.append(device_data['daily'][index]['hour'])
                print(time_type_day)
                print(time_type_nigth)
                #CONSOLIDATE DAY SHIFT
                time_type_day = list(set(time_type_day))
                for time_index, data in enumerate(time_type_day):
                    for index, data in enumerate(device_data['daily']):
                        if device_data['daily'][index]['hour'] == time_type_day[time_index] and device_data['daily'][index]['day'] == day and device_data['daily'][index]['month'] == month and device_data['daily'][index]['year'] == year:                         
                            for prop in range(len(device_properties)):
                                if device_data['daily'][index]['shift'] == 'day': 
                                    consolidated_props_shift_day[prop]['value'] += device_data['daily'][index]['properties'][prop]['value']
                    for index, prop in enumerate(consolidated_props_shift_day):
                        if consolidated_props_shift_day[index]['value'] != 0:
                            data_day.append(copy.deepcopy(consolidated_props_shift_day))

                    for prop in range(len(device_properties)):
                        consolidated_props_shift_day[prop]['value'] = 0
                    print(data_day)
                #CONSOLIDATE NIGTH SHIFT
                time_type_nigth = list(set(time_type_nigth))
                for time_index, data in enumerate(time_type_nigth):
                    for index, data in enumerate(device_data['daily']):
                        if device_data['daily'][index]['hour'] == time_type_nigth[time_index] and device_data['daily'][index]['day'] == day and device_data['daily'][index]['month'] == month and device_data['daily'][index]['year'] == year:
                            for prop in range(len(device_properties)):
                                if device_data['daily'][index]['shift'] == 'nigth':
                                    consolidated_props_shift_nigth[prop]['value'] += device_data['daily'][index]['properties'][prop]['value']
                    for index, prop in enumerate(consolidated_props_shift_nigth):
                        if consolidated_props_shift_nigth[0]['value'] != 0:
                            data_nigth.append(copy.deepcopy(consolidated_props_shift_nigth))
                    for prop in range(len(device_properties)):
                        consolidated_props_shift_nigth[prop]['value'] = 0

            # print(data_day)
            print(json.dumps(data_day, indent=4))
            print("//**************//")
            # print(json.dumps(data_nigth, indent=4))
            #////////////////////////////////////////////////////////////////////////////////////////////
            if periodicity == 'weekly':
                #GET DAYS BY SHIFT
                device_data['daily'] = sorted(device_data['daily'], key=lambda x: x['day'])
                for index, data in enumerate(device_data['daily']):
                    if device_data['daily'][index]['week'] == week and device_data['daily'][index]['month'] == month and device_data['daily'][index]['year'] == year:
                        if device_data['daily'][index]['shift'] == 'day':
                            time_type_day.append(device_data['daily'][index]['day'])
                        if device_data['daily'][index]['shift'] == 'nigth':
                                time_type_nigth.append(device_data['daily'][index]['day'])
                #CONSOLIDATE DAY SHIFT
                time_type_day = list(set(time_type_day))
                print(time_type_day)
                for time_index, data in enumerate(time_type_day):
                    for index, data in enumerate(device_data['daily']):
                        if device_data['daily'][index]['day'] == time_type_day[time_index] and device_data['daily'][index]['week'] == week and device_data['daily'][index]['month'] == month and device_data['daily'][index]['year'] == year:
                            for prop in range(len(device_properties)):
                                if device_data['daily'][index]['shift'] == 'day':    
                                    consolidated_props_shift_day[prop]['value'] += device_data['daily'][index]['properties'][prop]['value']

                    for index, prop in enumerate(consolidated_props_shift_day):
                        if consolidated_props_shift_day[index]['value'] != 0:
                            data_day.append(copy.deepcopy(consolidated_props_shift_day))
                    for prop in range(len(device_properties)):
                        consolidated_props_shift_day[prop]['value'] = 0
                #CONSOLIDATE NIGTH SHIFT
                time_type_nigth = list(set(time_type_nigth))
                print(time_type_nigth)
                for time_index, data in enumerate(time_type_nigth):
                    for index, data in enumerate(device_data['daily']):
                        if device_data['daily'][index]['day'] == time_type_nigth[time_index] and device_data['daily'][index]['week'] == week and device_data['daily'][index]['month'] == month and device_data['daily'][index]['year'] == year:
                            for prop in range(len(device_properties)):
                                if device_data['daily'][index]['shift'] == 'nigth':
                                    consolidated_props_shift_nigth[prop]['value'] += device_data['daily'][index]['properties'][prop]['value']

                    for index, prop in enumerate(consolidated_props_shift_nigth):
                        if consolidated_props_shift_nigth[0]['value'] != 0:
                            data_nigth.append(copy.deepcopy(consolidated_props_shift_nigth))
                    for prop in range(len(device_properties)):
                        consolidated_props_shift_nigth[prop]['value'] = 0

            if periodicity == 'monthly':
                #GET DAYS BY SHIFT
                device_data['daily'] = sorted(device_data['daily'], key=lambda x: x['day'])
                for index, data in enumerate(device_data['daily']):
                    if device_data['daily'][index]['month'] == month and device_data['daily'][index]['year'] == year:
                        if device_data['daily'][index]['shift'] == 'day':
                            time_type_day.append(device_data['daily'][index]['week'])
                        if device_data['daily'][index]['shift'] == 'nigth':
                                time_type_nigth.append(device_data['daily'][index]['week'])
                #CONSOLIDATE DAY SHIFT
                time_type_day = list(set(time_type_day))
                print(time_type_day)
                for time_index, data in enumerate(time_type_day):
                    for index, data in enumerate(device_data['daily']):
                        if device_data['daily'][index]['week'] == time_type_day[time_index] and device_data['daily'][index]['month'] == month and device_data['daily'][index]['year'] == year:
                            for prop in range(len(device_properties)):
                                if device_data['daily'][index]['shift'] == 'day':    
                                    consolidated_props_shift_day[prop]['value'] += device_data['daily'][index]['properties'][prop]['value']

                    for index, prop in enumerate(consolidated_props_shift_day):
                        if consolidated_props_shift_day[index]['value'] != 0:
                            data_day.append(copy.deepcopy(consolidated_props_shift_day))
                    for prop in range(len(device_properties)):
                        consolidated_props_shift_day[prop]['value'] = 0
                #CONSOLIDATE NIGTH SHIFT
                time_type_nigth = list(set(time_type_nigth))
                print(time_type_nigth)
                for time_index, data in enumerate(time_type_nigth):
                    for index, data in enumerate(device_data['daily']):
                        if device_data['daily'][index]['week'] == time_type_nigth[time_index] and device_data['daily'][index]['month'] == month and device_data['daily'][index]['year'] == year:
                            for prop in range(len(device_properties)):
                                if device_data['daily'][index]['shift'] == 'nigth':
                                    consolidated_props_shift_nigth[prop]['value'] += device_data['daily'][index]['properties'][prop]['value']

                    for index, prop in enumerate(consolidated_props_shift_nigth):
                        if consolidated_props_shift_nigth[0]['value'] != 0:
                            data_nigth.append(copy.deepcopy(consolidated_props_shift_nigth))
                    for prop in range(len(device_properties)):
                        consolidated_props_shift_nigth[prop]['value'] = 0

                # print(json.dumps(data_day, indent=4))
                # print("//**************//")
                # print(json.dumps(data_nigth, indent=4))
               
            if periodicity == 'yearly':
                #GET DAYS BY SHIFT
                device_data['daily'] = sorted(device_data['daily'], key=lambda x: x['day'])
                print(device_data['daily'])
                for index, data in enumerate(device_data['daily']):
                    if device_data['daily'][index]['year'] == year:
                        if device_data['daily'][index]['shift'] == 'day':
                            time_type_day.append(device_data['daily'][index]['month'])
                        if device_data['daily'][index]['shift'] == 'nigth':
                                time_type_nigth.append(device_data['daily'][index]['month'])
                #CONSOLIDATE DAY SHIFT
                time_type_day = list(set(time_type_day))
                print(time_type_day)
                for time_index, data in enumerate(time_type_day):
                    for index, data in enumerate(device_data['daily']):
                        if device_data['daily'][index]['month'] == month and device_data['daily'][index]['year'] == year:
                            for prop in range(len(device_properties)):
                                if device_data['daily'][index]['shift'] == 'day':    
                                    consolidated_props_shift_day[prop]['value'] += device_data['daily'][index]['properties'][prop]['value']

                    for index, prop in enumerate(consolidated_props_shift_day):
                        if consolidated_props_shift_day[index]['value'] != 0:
                            data_day.append(copy.deepcopy(consolidated_props_shift_day))
                    for prop in range(len(device_properties)):
                        consolidated_props_shift_day[prop]['value'] = 0
                #CONSOLIDATE NIGTH SHIFT
                time_type_nigth = list(set(time_type_nigth))
                print(time_type_nigth)
                for time_index, data in enumerate(time_type_nigth):
                    for index, data in enumerate(device_data['daily']):
                        if device_data['daily'][index]['month'] == month and device_data['daily'][index]['year'] == year:
                            for prop in range(len(device_properties)):
                                if device_data['daily'][index]['shift'] == 'nigth':
                                    consolidated_props_shift_nigth[prop]['value'] += device_data['daily'][index]['properties'][prop]['value']

                    for index, prop in enumerate(consolidated_props_shift_nigth):
                        if consolidated_props_shift_nigth[0]['value'] != 0:
                            data_nigth.append(copy.deepcopy(consolidated_props_shift_nigth))
                    for prop in range(len(device_properties)):
                        consolidated_props_shift_nigth[prop]['value'] = 0


            print("*****************************************************************")
            print("Consolidated data")
            print('DEVICE:', deviceId[device])
            # print('Consolidated shift day')
            # print(consolidated_props_shift_day)
            # print('Consolidated shift nigth')
            # print(consolidated_props_shift_nigth)
            print("*****************************************************************")
            update_data(periodicity, device_data, data_day, data_nigth, deviceId[device], day, weekday, week, month, year, time_type_day, time_type_nigth)

        except Exception as e:
            # print('somthing wrong id', e)
            pass
    print("--------------------END GET_CONSOLIDATED--------------------")




def get_query_data(device, periodicity, shift, day, week, month, year):

    try:

        #////////////////////////////////////////////////////////////////////////////////////////////
        device_data = get_data(device)
        device_data_copy_shift_day = copy.deepcopy(device_data)
        device_data_copy_shift_nigth = copy.deepcopy(device_data)

        device_properties = device_data['daily'][0]['properties']

        device_properties_shift_day = device_data_copy_shift_day['daily'][0]['properties']
        device_properties_shift_nigth = device_data_copy_shift_nigth['daily'][0]['properties']


        consolidated_props_shift_day = device_properties_shift_day
        consolidated_props_shift_nigth = device_properties_shift_nigth

        for prop in range(len(device_properties)):
            consolidated_props_shift_day[prop]['value'] = 0
            consolidated_props_shift_nigth[prop]['value'] = 0

        query_data = []
        #////////////////////////////////////////////////////////////////////////////////////////////
        if periodicity == 'daily':
            for hour_index, hour in enumerate(device_data['daily']):
                if device_data['daily'][hour_index]['shift'] == shift and device_data['daily'][hour_index]['day'] == day and device_data['daily'][hour_index]['month'] == month and device_data['daily'][hour_index]['year'] == year:
                    query_data.append(device_data['daily'][hour_index])
            query_data = sorted(query_data, key=lambda x: x['hour'])
            return query_data

        #////////////////////////////////////////////////////////////////////////////////////////////
        elif periodicity == 'weekly':
            if shift == 'day':
                data_type = 'weeklyDayConsolidated'
            elif shift == 'nigth':
                data_type = 'weeklyNigthConsolidated'

            for index in range(len(device_data[data_type])):
                if device_data[data_type][index]['week'] == week and device_data[data_type][index]['month'] == month and device_data[data_type][index]['year'] == year:
                    query_data.append(device_data[data_type][index])
            query_data = sorted(query_data, key=lambda x: x['day'])
            return query_data

        elif periodicity == 'monthly':
            if shift == 'day':
                data_type = 'monthlyDayConsolidated'
            elif shift == 'nigth':
                data_type = 'monthlyNigthConsolidated'
            for index in range(len(device_data[data_type])):
                if device_data[data_type][index]['month'] == month and device_data[data_type][index]['year'] == year:
                    query_data.append(device_data[data_type][index])
            query_data = sorted(query_data, key=lambda x: x['week'])
            return query_data

        elif periodicity == 'yearly':
            if shift == 'day':
                data_type = 'yearlyDayConsolidated'
            elif shift == 'nigth':
                data_type = 'yearlyNigthConsolidated'
            for index in range(len(device_data[data_type])):
                if device_data[data_type][index]['year'] == year:
                    query_data.append(device_data[data_type][index])
            query_data = sorted(query_data, key=lambda x: x['month'])
            return query_data
        else:
            return
        
    except Exception as e:
        print('somthing wrong', e)
        # pass

def get_query_devices(all=False):
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME_OUT)
        print("connection successful")
        db = client['location_devices']  # new db
        collection = db['location_devices']  # new collection

        if all:
            if collection.count_documents({'devices': {'$exists': True}}) > 0:
                result = collection.find_one({})
                if result is not None:
                    devices_list = result['devices']
                    devices_list = [entry['deviceId'] for entry in devices_list]
                    devices_list = list(set(devices_list))
                    # print(devices_list)
                    client.close()
                    return devices_list
        client.close()
    except pymongo.errors.ServerSelectionTimeoutError as error:
        print("Timeout")
        pass
    except pymongo.errors.ConnectionFailure as errorConnection:
        print("Connection failure")


def update_services_old(periodicity, in_year, in_month, in_week, in_day):
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME_OUT)
        print("connection successful")

        db = client['maga']  # new db
        collection = db['devices']  # new collection

        consolidated_data = {}  # Dictionary to store consolidated data by service

        # Fetch data from collection
        devices = collection.find()
        consolidated_json = []
        prev_device_id = ''
        prev_service = None
        compacted_data = []
        for device in devices:
            device_id = device['deviceId']
            sys_id = device['sysId']
            service = device['location']['service']
            daily_data = device['daily']
            aplication = device['aplication']

            for day_data in daily_data:
                year = day_data['year']
                month = day_data['month']
                week = day_data['week']
                day = day_data['day']
                hour = day_data['hour']
                shift = day_data['shift']
                properties = day_data.get('properties', [])


                if periodicity == 'daily':
                    parameters = [service, year, month, day, sys_id, shift]

                elif periodicity == 'weekly':
                    parameters = [device_id, service, year, month, week, sys_id, shift]
                    
                elif periodicity == 'monthly':
                    parameters = [device_id, service, year, month, sys_id, shift]

                elif periodicity == 'yearly':                
                    parameters = [device_id, service, year, sys_id, shift]

                else:
                    return

                # Initialize entry in consolidated_data
                key = tuple(parameters)
                if key not in consolidated_data:
                    consolidated_data[key] = []

                # Consolidate properties
                for prop in properties:
                    existing_prop = next((p for p in consolidated_data[key] if p['name'] == prop['name']), None)
                    if existing_prop:
                        existing_prop['value'] += prop['value']
                    else:
                        consolidated_data[key].append(prop.copy())



            print("**SERVICIO = ", service)
            print("**DEVICE = ", device_id)
            service_copy = copy.deepcopy(service)
            device_copy = copy.deepcopy(device_id)


            for consolidated_key, properties in consolidated_data.items():
                print("SERVICIO = ", service)
                print("DEVICE = ", device_id)
                if periodicity == 'daily':
                    (service, year, month, day, sys_id, shift) = consolidated_key
                    filters = service == service_copy  and year == in_year and month == in_month and day == in_day
                
                elif periodicity == 'weekly':
                    (device_id, service, year, month, week, sys_id, shift) = consolidated_key
                    filters = service == service_copy and device_id == device_copy  and year == in_year and week == in_week
                
                elif periodicity == 'monthly':
                    (device_id, service, year, month, sys_id, shift) = consolidated_key
                    filters = service == service_copy and device_id == device_copy and year == in_year and month == in_month 
                
                elif periodicity == 'yearly':
                    (device_id, service, year, sys_id, shift) = consolidated_key
                    filters = service == service_copy and device_id == device_copy and year == in_year
                else:
                    return
                
                daily_data = []


                if filters:
                    consolidated_entry = {
                    "service" : service,
                    "device" : device_id, 
                    "hour": hour,
                    "day": day,
                    "week": week,
                    "month": month,
                    "year": year,
                    "shift": shift,
                    "properties": properties
                    }
                    daily_data.append(consolidated_entry)
                    daily = {
                    "service": service,
                    "aplication": aplication,
                    periodicity: daily_data
                    }
                    print("##########################################")
                    print(json.dumps(daily, indent=4))
                    print("##########################################")
                    # # print("---------------**---------------------")
                    compacted_data.append(copy.deepcopy(daily))

        # print("-------------------//-----------------------------")
        # print(json.dumps(compacted_data, indent=4))
        # print("-------------------//-----------------------------")

        # Create dictionaries to store the max values for each service in both shifts
        max_values_day = {}
        max_values_night = {}

        # Iterate through the compacted_data
        for entry in compacted_data:
            service = entry["service"]
            shift = entry[periodicity][0]["shift"]
            value = sum(prop["value"] for prop in entry["daily"][0]["properties"])
            
            if shift == "day":
                # print("en day")
                if service in max_values_day:
                    if value > max_values_day[service]["value"]:
                        max_values_day[service] = {"shift": shift, "value": value}
                else:
                    max_values_day[service] = {"shift": shift, "value": value}
            elif shift == "nigth":
                # print("en nigth")
                if service in max_values_night:
                    if value > max_values_night[service]["value"]:
                        max_values_night[service] = {"shift": shift, "value": value}
                else:
                    max_values_night[service] = {"shift": shift, "value": value}

        # Filter the compacted_data to keep only entries with max values for both shifts
        filtered_data = []
        for entry in compacted_data:
            service = entry["service"]
            shift = entry[periodicity][0]["shift"]
            value = sum(prop["value"] for prop in entry["daily"][0]["properties"])
            
            if (shift == "day" and value == max_values_day[service]["value"]) or (shift == "nigth" and value == max_values_night[service]["value"]):
                filtered_data.append(entry)

        # Convert the filtered data back to JSON format
        filtered_json = json.dumps(filtered_data, indent=4)
        # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        # print(filtered_json)

    except Exception as e:
        print('Something went wrong:', e)
    finally:
        client.close()

            # print("**", device_id, prev_device_id, "**")

            # if device != prev_device_id and prev_device_id != '':
            #     print(json.dumps(daily, indent=4))
            #     print("---------------**---------------------")
            #     prev_device_id = device_id
            # else:
            #     prev_device_id = device_id

            # print('***', service, prev_service, '***')
            # if service != prev_service and prev_service != '':
            #     print("holito")
            #     prev_service = service
            #     prev_device_id = ''
            # else:
            #     prev_service = service
            # print("///////////////////////////////////////////")


#////////////////////////////////////////////////////////////////////////////////////////// By Services 
def update_services(consolidate_type, in_year, in_month, in_week, in_day, in_hour):
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME_OUT)
        print("connection successful")

        db = client['maga']  # new db
        collection = db['devices']  # new collection

        # Fetch data from collection
        raw_data = collection.find()
        consolidated_data = {}

        
        # Iterate through each device record
        for record in raw_data:
            service = record['location']['service']
            daily_entries = record['daily']
            aplication = record['aplication']
            sys_id = record['sysId']

            for daily_entry in daily_entries:
                hour = daily_entry['hour']
                day = daily_entry['day']
                weekday = daily_entry['weekday']
                week = daily_entry['week']
                month = daily_entry['month']
                year = daily_entry['year']
                shift = daily_entry['shift']

                
                if consolidate_type == 'hour':
                    filters = hour == in_hour and day == in_day and month == in_month and year == in_year
                elif consolidate_type == 'day':
                    filters = day == in_day and month == in_month and year == in_year
                elif consolidate_type == 'week':
                    filters = week == in_week and year == in_year
                elif consolidate_type == 'month':
                    filters = month == in_month and year == in_year
                elif consolidate_type == 'year':
                    filters = year == in_year
                else:
                    client.close()
                    return
                
                # if consolidate_type == 'day':
                #     filters = hour == in_hour and day == in_day and month == in_month and year == in_year
                # elif consolidate_type == 'week':
                #     filters = day == in_day and month == in_month and year == in_year
                # elif consolidate_type == 'month':
                #     filters = week == in_week and year == in_year
                # elif consolidate_type == 'year':
                #     filters = month == in_month and year == in_year
                # else:
                #     return

                # Check if the current entry matches the desired day
                if filters:
                    # print('shift es: ',shift)

                    # Initialize the service entry in the consolidated data dictionary
                    if service not in consolidated_data:
                        consolidated_data[service] = {
                            'sysId': sys_id,
                            'aplication': aplication,
                            'consolidatedType': consolidate_type,
                            'hour': hour,
                            'day': day,
                            'weekday': weekday,
                            'week': week,
                            'month': month,
                            'year': year
                        }
                        consolidated_data[service]['dataShiftDay'] = []
                        consolidated_data[service]['dataShiftNigth'] = []
                        print('********************************************')
                        day_daily_data = {'properties': []}
                        nigth_daily_data = {'properties': []}

                    if shift == 'day':
                        if len(consolidated_data[service]['dataShiftDay']) <= 0 :
                            consolidated_data[service]['dataShiftDay'].append(day_daily_data)
                        day_daily_data = next(d for d in consolidated_data[service]['dataShiftDay'])
                        # Iterate through property values and aggregate them
                        for property_data in daily_entry['properties']:
                            property_name = property_data['prop']
                            property_value = property_data['value']

                            # Check if the property already exists in props, if not, add it
                            existing_property = next((p for p in day_daily_data['properties'] if p['prop'] == property_name), None)
                            if existing_property:
                                existing_property['value'] += property_value
                            else:
                                properties = {
                                    "name": property_data['name'],
                                    "prop": property_name,
                                    "value": property_value
                                }

                                day_daily_data['properties'].append(properties)

                    elif shift == 'nigth':
                        if len(consolidated_data[service]['dataShiftNigth']) <= 0 :
                            consolidated_data[service]['dataShiftNigth'].append(nigth_daily_data)
                        nigth_daily_data = next(d for d in consolidated_data[service]['dataShiftNigth'])
                        
                        # Iterate through property values and aggregate them
                        for property_data in daily_entry['properties']:
                            property_name = property_data['prop']
                            property_value = property_data['value']

                            # Check if the property already exists in props, if not, add it
                            existing_property = next((p for p in nigth_daily_data['properties'] if p['prop'] == property_name), None)
                            if existing_property:
                                existing_property['value'] += property_value
                            else:
                                properties = {
                                    "name": property_data['name'],
                                    "prop": property_name,
                                    "value": property_value
                                }
                                nigth_daily_data['properties'].append(properties)

 
        # print('holi')
        # print(json.dumps(consolidated_data, indent=4))
        client.close()
        save_consolidated_data_by_service(consolidated_data)


    except Exception as e:
        print('Something went wrong:', e)
    finally:
        client.close()

def delete_all_service_consolidate():

    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME_OUT)
    print("Connection successful")

    db = client[iot_db]
    collection = db[consolidated_devices_collection]  # Your collection name
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    # print(json.dumps(data, indent=4))
    # print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    print('borrar')
    collection.delete_many({})
    print_json(collection.find())
    print(collection.find_one())
    client.close()
    # return

def save_consolidated_data_by_service(data):
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME_OUT)
        print("Connection successful")

        db = client[iot_db]
        collection = db[consolidated_devices_collection]  # Your collection name

        services_list = list(data.keys())
        for service in services_list:
            service_data = data[service]  # Get the data for the current service

            # Create a document body for insertion/update
            service_body = {
                'service': service,
                "sysId": service_data['sysId'],
                "aplication": service_data['aplication'],
                "hourlyDay": [], 
                "hourlyNigth": [],
                "dailyDay": [],
                "dailyNigth": [],
                "weeklyDay": [],
                "weeklyNigth": [],
                "monthlyDay": [],
                "monthlyNigth": [],
                "yearlyDay": [],
                "yearlyNigth": [],
            }

            filter = {'service': service}
            document = collection.find_one(filter)

            if service_data['consolidatedType'] == 'hour':
                day_dated_data = {
                    'hour': service_data['hour'],
                    'day': service_data['day'],
                    'weekday': service_data['weekday'],
                    'week': service_data['week'],
                    'month': service_data['month'],
                    'year': service_data['year']
                    }

            elif service_data['consolidatedType'] == 'day':
                day_dated_data = {
                    'day': service_data['day'],
                    'week': service_data['week'],
                    'weekday': service_data['weekday'],
                    'month': service_data['month'],
                    'year': service_data['year']
                    }

            elif service_data['consolidatedType'] == 'week':
                day_dated_data = {
                    'week': service_data['week'],
                    'weekday': service_data['weekday'],
                    'month': service_data['month'],
                    'year': service_data['year']
                    }

            elif service_data['consolidatedType'] == 'month':
                day_dated_data = {
                    'month': service_data['month'],
                    'year': service_data['year']
                    }

            elif service_data['consolidatedType'] == 'year':
                day_dated_data = {
                    'year': service_data['year']
                    }

            else:
                return

            nigth_dated_data = copy.deepcopy(day_dated_data)

            if len(service_data['dataShiftDay']) > 0:
                day_dated_data['properties'] = service_data['dataShiftDay'][0]['properties']

            if len(service_data['dataShiftNigth']) > 0: 
                nigth_dated_data['properties'] = service_data['dataShiftNigth'][0]['properties']

            if document:
                if service_data['consolidatedType'] == 'hour':
                    periodicity_day = 'hourlyDay'
                    periodicity_nigth = 'hourlyNigth'

                elif service_data['consolidatedType'] == 'day':
                    periodicity_day = 'dailyDay'
                    periodicity_nigth = 'dailyNigth'

                elif service_data['consolidatedType'] == 'week':
                    periodicity_day = 'weeklyDay'
                    periodicity_nigth = 'weeklyNigth'

                elif service_data['consolidatedType'] == 'month':
                    periodicity_day = 'monthlyDay'
                    periodicity_nigth = 'monthlyNigth'

                # elif service_data['consolidatedType'] == 'year':
                #     periodicity_day = 'yearlyDay'
                #     periodicity_nigth = 'yearlyNigth'
                #     try:
                #         match_filter = document[periodicity_day][filter_index]['year'] == service_data['year']
                #     except IndexError:
                #         print('Idex ut of range, continue')
                #         pass

                else:
                    client.close()
                    return

                if service_data['consolidatedType'] == 'hour':
                    if len(service_data['dataShiftDay']) > 0:
                        if len(document[periodicity_day]) <= 0:
                            update = {'$push': {periodicity_day: day_dated_data}}
                            collection.update_one(filter, update)

                        else:
                            same_input_finded = False
                            for index, entry in enumerate(document[periodicity_day]): 
                                if(document[periodicity_day][index]['year'] == service_data['year'] and document[periodicity_day][index]['month'] == service_data['month']
                                and document[periodicity_day][index]['day'] == service_data['day'] and document[periodicity_day][index]['hour'] == service_data['hour']):
                                    update_query = {"$set": {f"{periodicity_day}.{index}": day_dated_data}}
                                    collection.update_one(filter, update_query)
                                    same_input_finded = True
                            if not same_input_finded:
                                update = {'$push': {periodicity_day: day_dated_data}}
                                collection.update_one(filter, update)

                    #/////////////////////////////////////////////////////////////////////////////////////////////////////////
                    if len(service_data['dataShiftNigth']) > 0:
                        if len(document[periodicity_nigth]) <= 0:
                            update = {'$push': {periodicity_nigth: nigth_dated_data}}
                            collection.update_one(filter, update)
                        
                        else:
                            same_input_finded = False
                            for index, entry in enumerate(document[periodicity_nigth]):
                                if(document[periodicity_nigth][index]['year'] == service_data['year'] and document[periodicity_nigth][index]['month'] == service_data['month']
                                and document[periodicity_nigth][index]['day'] == service_data['day'] and document[periodicity_nigth][index]['hour'] == service_data['hour']):
                                    update_query = {"$set": {f"{periodicity_nigth}.{index}": nigth_dated_data}}
                                    collection.update_one(filter, update_query)
                                    same_input_finded = True
                            if not same_input_finded:
                                update = {'$push': {periodicity_nigth: nigth_dated_data}}
                                collection.update_one(filter, update)
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                if service_data['consolidatedType'] == 'day':
                    if len(service_data['dataShiftDay']) > 0:
                        if len(document[periodicity_day]) <= 0:
                            update = {'$push': {periodicity_day: day_dated_data}}
                            collection.update_one(filter, update)

                        else:
                            same_input_finded = False
                            for index, entry in enumerate(document[periodicity_day]): 
                                if(document[periodicity_day][index]['year'] == service_data['year'] and document[periodicity_day][index]['month'] == service_data['month']\
                                and document[periodicity_day][index]['day'] == service_data['day']):
                                    update_query = {"$set": {f"{periodicity_day}.{index}": day_dated_data}}
                                    collection.update_one(filter, update_query)
                                    same_input_finded = True
                            if not same_input_finded:
                                update = {'$push': {periodicity_day: day_dated_data}}
                                collection.update_one(filter, update)

                    #/////////////////////////////////////////////////////////////////////////////////////////////////////////
                    if len(service_data['dataShiftNigth']) > 0:
                        if len(document[periodicity_nigth]) <= 0:
                            update = {'$push': {periodicity_nigth: nigth_dated_data}}
                            collection.update_one(filter, update)
                        
                        else:
                            same_input_finded = False
                            for index, entry in enumerate(document[periodicity_nigth]):
                                if(document[periodicity_nigth][index]['year'] == service_data['year'] and document[periodicity_nigth][index]['month'] == service_data['month']\
                                and document[periodicity_nigth][index]['day'] == service_data['day']):
                                    update_query = {"$set": {f"{periodicity_nigth}.{index}": nigth_dated_data}}
                                    collection.update_one(filter, update_query)
                                    same_input_finded = True
                            if not same_input_finded:
                                update = {'$push': {periodicity_nigth: nigth_dated_data}}
                                collection.update_one(filter, update)
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                if service_data['consolidatedType'] == 'week':
                    if len(service_data['dataShiftDay']) > 0:
                        if len(document[periodicity_day]) <= 0:
                            update = {'$push': {periodicity_day: day_dated_data}}
                            collection.update_one(filter, update)

                        else:
                            same_input_finded = False
                            for index, entry in enumerate(document[periodicity_day]): 
                                if(document[periodicity_day][index]['year'] == service_data['year'] and document[periodicity_day][index]['week'] == service_data['week']):
                                    update_query = {"$set": {f"{periodicity_day}.{index}": day_dated_data}}
                                    collection.update_one(filter, update_query)
                                    same_input_finded = True
                            if not same_input_finded:
                                update = {'$push': {periodicity_day: day_dated_data}}
                                collection.update_one(filter, update)

                    #/////////////////////////////////////////////////////////////////////////////////////////////////////////
                    if len(service_data['dataShiftNigth']) > 0:
                        if len(document[periodicity_nigth]) <= 0:
                            update = {'$push': {periodicity_nigth: nigth_dated_data}}
                            collection.update_one(filter, update)
                        
                        else:
                            same_input_finded = False
                            for index, entry in enumerate(document[periodicity_nigth]):
                                if(document[periodicity_nigth][index]['year'] == service_data['year'] and document[periodicity_nigth][index]['week'] == service_data['week']):
                                    update_query = {"$set": {f"{periodicity_nigth}.{index}": nigth_dated_data}}
                                    collection.update_one(filter, update_query)
                                    same_input_finded = True
                            if not same_input_finded:
                                update = {'$push': {periodicity_nigth: nigth_dated_data}}
                                collection.update_one(filter, update)
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////                
                if service_data['consolidatedType'] == 'month':
                    if len(service_data['dataShiftDay']) > 0:
                        if len(document[periodicity_day]) <= 0:
                            update = {'$push': {periodicity_day: day_dated_data}}
                            collection.update_one(filter, update)

                        else:
                            same_input_finded = False
                            for index, entry in enumerate(document[periodicity_day]): 
                                if(document[periodicity_day][index]['year'] == service_data['year'] and document[periodicity_day][index]['month'] == service_data['month']):
                                    update_query = {"$set": {f"{periodicity_day}.{index}": day_dated_data}}
                                    collection.update_one(filter, update_query)
                                    same_input_finded = True
                            if not same_input_finded:
                                update = {'$push': {periodicity_day: day_dated_data}}
                                collection.update_one(filter, update)

                    #/////////////////////////////////////////////////////////////////////////////////////////////////////////
                    if len(service_data['dataShiftNigth']) > 0:
                        if len(document[periodicity_nigth]) <= 0:
                            update = {'$push': {periodicity_nigth: nigth_dated_data}}
                            collection.update_one(filter, update)
                        
                        else:
                            same_input_finded = False
                            for index, entry in enumerate(document[periodicity_nigth]):
                                if(document[periodicity_nigth][index]['year'] == service_data['year'] and document[periodicity_nigth][index]['month'] == service_data['month']):
                                    update_query = {"$set": {f"{periodicity_nigth}.{index}": nigth_dated_data}}
                                    collection.update_one(filter, update_query)
                                    same_input_finded = True
                            if not same_input_finded:
                                update = {'$push': {periodicity_nigth: nigth_dated_data}}
                                collection.update_one(filter, update)
            else:
                if service_data['consolidatedType'] == 'hour':
                    periodicity_day = 'hourlyDay'
                    periodiciy_nigth = 'hourlyNigth'
                
                elif service_data['consolidatedType'] == 'day':
                    periodicity_day = 'dailyDay'
                    periodiciy_nigth = 'dailyNigth'
                
                elif service_data['consolidatedType'] == 'week':
                    periodicity_day = 'weeklyDay'
                    periodiciy_nigth = 'weeklyNigth'
                
                elif service_data['consolidatedType'] == 'month':
                    periodicity_day = 'monthlyDay'
                    periodiciy_nigth = 'monthlyNigth'
                
                elif service_data['consolidatedType'] == 'year':
                    periodicity_day = 'yearlyDay'
                    periodiciy_nigth = 'yearlyNigth'
                
                else:
                    return

                if len(service_data['dataShiftDay']) > 0:
                    print('ading data-....')
                    collection.insert_one(service_body)
                    update = {'$push': {periodicity_day: day_dated_data}}
                    collection.update_one(filter, update)

                if len(service_data['dataShiftNigth']) > 0:
                    collection.insert_one(service_body)
                    update = {'$push': {periodiciy_nigth: nigth_dated_data}}
                    collection.update_one(filter, update)

                print('Inserted new document for', service)

        print("Data insertion/updation completed.")
        # collection.delete_many({})
        print_json(collection.find())
        client.close()

    except Exception as e:
        print('Something went wrong:', e)
        pass
    finally:
        client.close()

def get_query_data_by_service(service, periodicity, shift, day, week, month, year):
    try:

        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME_OUT)
        # print("connection successful")
        db = client[iot_db]
        collection = db[consolidated_devices_collection] 

        filter = {'service': service}
        # filter = {}
        doc_finder = collection.find_one(filter)
        # print(doc_finder)
        if collection.count_documents(filter) > 0:
            print('File founded')
        else:
            print("File not found")



        #////////////////////////////////////////////////////////////////////////////////////////////
        device_data = doc_finder
        device_data_copy_shift_day = copy.deepcopy(device_data)
        device_data_copy_shift_nigth = copy.deepcopy(device_data)

        device_properties = device_data['hourlyDay'][0]['properties']

        device_properties_shift_day = device_data_copy_shift_day['hourlyDay'][0]['properties']
        device_properties_shift_nigth = device_data_copy_shift_nigth['hourlyDay'][0]['properties']


        consolidated_props_shift_day = device_properties_shift_day
        consolidated_props_shift_nigth = device_properties_shift_nigth

        for prop in range(len(device_properties)):
            consolidated_props_shift_day[prop]['value'] = 0
            consolidated_props_shift_nigth[prop]['value'] = 0
        query_data = []
        #////////////////////////////////////////////////////////////////////////////////////////////
        if periodicity == 'daily':
            if shift == 'day':
                data_type = 'hourlyDay'
            elif shift == 'nigth':
                data_type = 'hourlyNigth'
            # print(device_data)
            # print(device_data[data_type])
            for index in range(len(device_data[data_type])):
                if device_data[data_type][index]['day'] == day and device_data[data_type][index]['month'] == month and device_data[data_type][index]['year'] == year:
                    query_data.append(device_data[data_type][index])
            query_data = sorted(query_data, key=lambda x: x['hour'])
            client.close()
            return query_data


        #////////////////////////////////////////////////////////////////////////////////////////////
        elif periodicity == 'weekly':
            if shift == 'day':
                data_type = 'dailyDay'
            elif shift == 'nigth':
                data_type = 'dailyNigth'

            for index in range(len(device_data[data_type])):
                if device_data[data_type][index]['week'] == week and device_data[data_type][index]['year'] == year:
                    query_data.append(device_data[data_type][index])
            query_data = sorted(query_data, key=lambda x: x['day'])
            client.close()
            return query_data

        elif periodicity == 'monthly':
            if shift == 'day':
                data_type = 'weeklyDay'
            elif shift == 'nigth':
                data_type = 'weeklyNigth'

            for index in range(len(device_data[data_type])):
                if device_data[data_type][index]['month'] == month and device_data[data_type][index]['year'] == year:
                    query_data.append(device_data[data_type][index])
            query_data = sorted(query_data, key=lambda x: x['week'])
            client.close()
            return query_data

        elif periodicity == 'yearly':
            if shift == 'day':
                data_type = 'monthlyDay'
            elif shift == 'nigth':
                data_type = 'monthlyNigth'
            for index in range(len(device_data[data_type])):
                if device_data[data_type][index]['year'] == year:
                    query_data.append(device_data[data_type][index])
            query_data = sorted(query_data, key=lambda x: x['month'])
            return query_data
        else:
            client.close()
            return
        client.close()
    except Exception as e:
        print('somthing wrong', e)
        # pass

def get_query_services(all=False):
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME_OUT)
        print("connection successful")
        db = client['location_devices']  # new db
        collection = db['location_devices']  # new collection

        if all:
            if collection.count_documents({'devices': {'$exists': True}}) > 0:
                result = collection.find_one({})
                services_list = result['devices']
                if result is not None:
                    services_list = result['devices']
                    services_list = [entry['service'] for entry in services_list]
                    services_list = list(set(services_list))
                    client.close()
                    return services_list
        client.close()
    except pymongo.errors.ServerSelectionTimeoutError as error:
        print("Timeout")
        pass
    except pymongo.errors.ConnectionFailure as errorConnection:
        print("Connection failure")


#/////////////////////////////////--------------------------------------------------------//////////////////////////////////////////////
id = 'maga-003'
# id = 'test-dev2'
service = 'UCI-test'
hour = 1
day = 10
weekday = 5
week = 41
month = 10
year = 2023

# test-serv1 daily day 31 5 8 2023

# add_test(id, hour, day, weekday, week, month, year) #id, hour, day, weekday, week, month, year
# delete_all()
# delete_all_service_consolidate()
# periodicity = 'weekly'
# #UPDATE DEVICES
# get_consolidated(periodicity, day, weekday, week, month, year)

# add_device(id, service, 'test-area99', 'cubicle-99', 'None', False )
# add_device('maga-006', service, 'test-area99', 'cubicle-99', 'None', False )

# get_consolidated('daily', day, weekday, week, month, year)
# get_consolidated('weekly', day, weekday, week, month, year)
# get_consolidated('monthly', day, weekday, week, month, year)
# get_consolidated('yearly', day, weekday, week, month, year)
# #GET QUERY DEVICES


# print_device(id)
# print('////////////////////////////////////////**//////////////////////////////')
# print(get_query_data(id, periodicity, 'day', day, week, month, year))

# #UPDATE SERVICES
# update_services('hour', year, month, week, day, hour)
# update_services('day', year, month, week, day, hour)
# update_services('week', year, month, week, day, hour)
# update_services('month', year, month, week, day, hour)
# GET QUERY DEVICES

# print_device(id)
# print(get_query_data(id, 'weekly', 'day', day, week, month, year))

# print('---------------------------------/Query/-----------------------------------------------')
# add_device(id,'maga-service', 'test-area99', 'cubicle-99', 'None', False )



# delete_all()
# delete_all_service_consolidate()



# print("----------------------------------------------------------------------------")
# print_device(id)
# print('//////////*******////////////////////////////////////////////')

# print(get_query_data(id, 'yearly', 'day', day, week, month, year))
# print(json.dumps(get_query_data(id, 'daily', 'day', day, week, month, year), indent=4))
# get_query_devices(True)


# update_week_consolidated('daily')

# get_data(id)



# add_test(id, hour, day, weekday, week, month, year) #id, hour, day, weekday, week, month, year





# add_device('test-device-001', 'test-service', 'none', 'none', 'test-room001', False)
# add_device('test-device-001', 'test-service', 'none', 'none', 'test-room001', True)
# get_device_location('test-device001')
# get_daily_data(7, 'test-device-001')



# update_day_consolidated(hour, day, weekday, week, month, year)

                        # dated_data = {
                        #     'hour': service_data['hour'],
                        #     'day': service_data['day'],
                        #     'weekday': service_data['weekday'],
                        #     'week': service_data['week'],
                        #     'month': service_data['month'],
                        #     'year': service_data['year']
                        # }