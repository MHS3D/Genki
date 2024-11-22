import math
import numpy  as np
import json
import random

path_liegend = "liegend.json"
path_laufen = "laufen.json"
path_treppehoch = "Treppehoch.json"
path_trepperunter = "Trepperunter.json"

def load_json(path):
    data = None
    with open(path, 'r') as file:
        data = json.load(file)
    return data

def read_values(data):
    accel = data["accel"]
    gyro = data["gyro"]
    length = 0
    if len(accel) < len(gyro):
        length = len(accel)
    else:
        length = len(gyro)
    acc_list = []
    gyro_list = []
    for i in range(length):
        x = round(accel[i]["x"],2)
        y = round(accel[i]["y"],2)
        z = round(accel[i]["z"],2)
        t = round(accel[i]["timestamp"],2)
        acc_list.append(np.array([x,y,z,t]))
        x = round(gyro[i]["x"],2)
        y = round(gyro[i]["y"],2)
        z = round(gyro[i]["z"],2)
        t = round(gyro[i]["timestamp"],2)
        gyro_list.append(np.array([x,y,z,t]))
    acc_list = np.array(acc_list)
    gyro_list = np.array(gyro_list)
    return [acc_list,gyro_list]

def read_values_list(data):
    accel = data["accel"]
    gyro = data["gyro"]
    length = 0
    if len(accel) < len(gyro):
        length = len(accel)
    else:
        length = len(gyro)
    acc_list = []
    gyro_list = []
    for i in range(length):
        x = round(accel[i]["x"],2)
        y = round(accel[i]["y"],2)
        z = round(accel[i]["z"],2)
        t = round(accel[i]["timestamp"],2)
        acc_list.append(np.array([x,y,z,t]))
        x = round(gyro[i]["x"],2)
        y = round(gyro[i]["y"],2)
        z = round(gyro[i]["z"],2)
        t = round(gyro[i]["timestamp"],2)
        gyro_list.append(np.array([x,y,z,t]))
    return [acc_list,gyro_list]

def read_values_2(data, acc_list, gyro_list):
    accel = data["accel"]
    gyro = data["gyro"]
    length = 0
    if len(accel) < len(gyro):
        length = len(accel)
    else:
        length = len(gyro)
    for i in range(length):
        x = round(accel[i]["x"],2)
        y = round(accel[i]["y"],2)
        z = round(accel[i]["z"],2)
        t = round(accel[i]["timestamp"],2)
        acc_list.append(np.array([x,y,z,t]))
        x = round(gyro[i]["x"],2)
        y = round(gyro[i]["y"],2)
        z = round(gyro[i]["z"],2)
        t = round(gyro[i]["timestamp"],2)
        gyro_list.append(np.array([x,y,z,t]))
    acc_list = np.array(acc_list)
    gyro_list = np.array(gyro_list)
    return [acc_list,gyro_list]

def millisec_in_sec(times):
    val_list = []
    for i in range(len(times)):
        val_list.append(times[i]/6666)
    return np.array(val_list)

def noise_offset(val):
    if val == 0:
        val = 0.1
    val1 = math.pow(math.pow(val,2), 0.5)
    limit = int(val1*100)
    offset = random.randint(0,limit)
    direct = random.randint(0,limit)
    res = 0
    if direct % 2 == 0:
        res = val*1000+offset
    else:
        res = val*1000-offset
    return res/1000
    
def noise_offset_array(arr):
    for i in range(len(arr)):
        arr[i] = noise_offset(arr[i])
    return arr

def fill_test_array():
    count_values = 1000
    count_subarray = 4
    arr = np.zeros((count_subarray,count_values))
    count_x = 0
    count_y = 0
    count_z = 0
    for j in range(10):
        t1 = 1
        t2 = 1
        t3 = 0
        if j % 2 == 1:
            t1 = -1
        for i in range(j*100,j*100+100):
            if i%100 < 75:
                count_x +=t1
                count_z +=1
            else:
                count_y +=t1
            arr[0][i] = count_x
            arr[1][i] = count_y
            arr[2][i] = count_z
            arr[3][i] = i     
    return arr

def calc_acceleration(s1,s2,t1,t2):
    if (t2-t1) <= 0:
        return 0
    acc = 2 * (s2-s1) / ((t2-t1) ** 2)
    return acc

def calc_acceleration_array(route_arr, time_arr):
    res_arr = np.zeros(len(route_arr))
    if len(route_arr) != len(time_arr):
        return str(len(route_arr)) + "!=" + str(len(time_arr))
    for i in range(len(route_arr)-1):
        res_arr[i] = calc_acceleration(route_arr[i],route_arr[i+1],time_arr[i],time_arr[i+1])
    return res_arr

def getTestAcceleration(choose):
    match choose:
        case 1:
            json_data = load_json(path_liegend)
            values = read_values(json_data)
        case 2:
            json_data = load_json(path_laufen)
            values = read_values(json_data)
        case 3:
            json_data = load_json(path_treppehoch)
            values = read_values(json_data)
        case 4:
            json_data = load_json(path_trepperunter)
            values = read_values(json_data)
        case 99:
            json_data = load_json(path_treppehoch)
            json_data1 = load_json(path_trepperunter)
            values = read_values_list(json_data)
            values = read_values_2(json_data1, values[0], values[1])
        case _:
            return [[],[]]
    return values