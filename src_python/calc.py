import math
import numpy  as np
from scipy.spatial.transform import Rotation as R
import plot
import json
import test_values

# Definiere Filterkonstanten
G = 0.981
ALPHA = 0.98 # Konstante für den Komplementärfilter
# Initialisierungen
POSITION = np.array([0.0, 0.0, 0.0])  # Startposition (x, y, z)
VELOCITY = np.array([0.0, 0.0, 0.0])  # Anfangsgeschwindigkeit (x, y, z)
ANGLE = np.array([0.0, 0.0, 0.0])     # Orientierung (Roll, Pitch, Yaw)
LAST_TIME = 0
JSON_DATA = []
COUNT_DATA = 0
PLOT3D = True
PLOT_GYRO = True
CHOOSE = 4 # 1 = liegend; 2 = laufen; 3 = Treppenhoch; 4 = Trepperunter

def iirFilter(arr, alpha):
    old_arr = arr.copy()
    length = len(arr)
    dst = []
    for j in range(0,length-1):
        dst.append(alpha*arr[j] + (1-alpha)*old_arr[j+1])
    return np.array(dst)

##########################################################################################
##########################################################################################
##########################################################################################

def update_position(acceleration, gyro, dt):
    global POSITION, VELOCITY, ANGLE, G

    # Winkelgeschwindigkeit integrieren (Gyroskop)
    ANGLE += gyro * dt  # Winkel in Rad berechnen

    # Komplementärfilter anwenden (Nutzung von Beschleunigung und Gyro zur Stabilisierung)
    '''
    roll_acc, pitch_acc = calc_roll_pitch(acceleration)
    ANGLE[0] = ALPHA * (ANGLE[0]) + (1 - ALPHA) * roll_acc
    ANGLE[1] = ALPHA * (ANGLE[1]) + (1 - ALPHA) * pitch_acc
    '''
    # Beschleunigungswerte in Weltkoordinaten transformieren (Rotation basierend auf Winkel)
    acc_world = rotate_to_world(acceleration, ANGLE)
    #acc_world -= np.array([0.0,0.0,G])

    # Integration der Geschwindigkeit und Position (Euler-Integration)
    VELOCITY += acc_world * dt
    POSITION += VELOCITY * dt

    return POSITION, VELOCITY, ANGLE

def calc_roll_pitch(acceleration):
    roll_acc = math.atan2(acceleration[1], acceleration[2])
    #pitch_acc = math.atan2(-acceleration[0], math.sqrt(acceleration[1]**2 + acceleration[2]**2))
    pitch_acc = math.atan2(-acceleration[0], acceleration[2])
    return roll_acc, pitch_acc

def rotate_to_world(acceleration, angle):
    """Rotation der Beschleunigung in Weltkoordinaten basierend auf den Winkeln."""
    roll, pitch, yaw = angle
    # Erzeuge Rotationsmatrix für die Transformation
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(roll), -np.sin(roll)],
                   [0, np.sin(roll), np.cos(roll)]])
    
    Ry = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                   [0, 1, 0],
                   [-np.sin(pitch), 0, np.cos(pitch)]])
    
    Rz = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                   [np.sin(yaw), np.cos(yaw), 0],
                   [0, 0, 1]])
    
    # Gesamte Rotationsmatrix
    R = Rz @ Ry @ Rx
    return R @ acceleration

def preparing_for_plot(accel, gyro):
    global LAST_TIME
    LAST_TIME = accel[0][3]-0.01
    route_x = []
    route_y = []
    route_z = []
    times = []
    dt = 0.01
    for i in range(len(accel)):
        dt = accel[i][3]-LAST_TIME
        LAST_TIME = accel[i][3]
        position, velocity, angle = update_position(accel[i][:3], gyro[i][:3], dt)
        route_x.append(position[0])
        route_y.append(position[1])
        route_z.append(position[2])
        times.append(accel[i][3])
    route_x = np.array(route_x)
    route_y = np.array(route_y)
    route_z = np.array(route_z)
    times = np.array(times)
    return route_x, route_y, route_z, times

def preparing_for_plot_2(pos):
    route_x = []
    route_y = []
    route_z = []
    times = []
    for i in range(len(pos)):
        route_x.append(pos[i][0])
        route_y.append(pos[i][1])
        route_z.append(pos[i][2])
        times.append(pos[i][3])
    route_x = np.array(route_x)
    route_y = np.array(route_y)
    route_z = np.array(route_z)
    times = np.array(times)
    return route_x, route_y, route_z, times

def preparing_json(data, accel, gyro):
    global LAST_TIME, COUNT_DATA
    LAST_TIME = accel[0][3]-0.01
    dt = 0.01
    COUNT_DATA = len(data)
    for i in range(len(accel)):
        if accel[i][3] >= LAST_TIME:
            dt = accel[i][3]-LAST_TIME
            LAST_TIME = accel[i][3]
            position, velocity, angle = update_position(accel[i][:3], gyro[i][:3], dt)
            neue_daten = [{"x": position[0],"y": position[1],"z": position[2],"timestamp": accel[i][3]}]
            data.extend(neue_daten)
            COUNT_DATA += 1
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
        x = accel[i]["x"]
        y = accel[i]["y"]
        z = accel[i]["z"]
        t = accel[i]["timestamp"]
        acc_list.append(np.array([x,y,z,t]))
        x = gyro[i]["x"]
        y = gyro[i]["y"]
        z = gyro[i]["z"]
        t = gyro[i]["timestamp"]
        gyro_list.append(np.array([x,y,z,t]))
    acc_list = np.array(acc_list)
    gyro_list = np.array(gyro_list)
    return [acc_list,gyro_list]   

##########################################################################################
##########################################################################################
##########################################################################################
'''
acc, gyro = test_values.getTestAcceleration(6)

xmean = np.mean(acc[:,0])
acc[:,0] = acc[:,0] - xmean
ymean = np.mean(acc[:,1])
acc[:,1] = acc[:,1] - ymean
zmean = np.mean(acc[:,2])
acc[:,2] = acc[:,2] - zmean

xmean = np.mean(gyro[:,0])
gyro[:,0] = gyro[:,0] - xmean
ymean = np.mean(gyro[:,1])
gyro[:,1] = gyro[:,1] - ymean
zmean = np.mean(gyro[:,2])
gyro[:,2] = gyro[:,2] - zmean


plot.plotWithTime(acc[:,0],acc[:,1],acc[:,2],acc[:,3])
x,y,z,t = preparing_for_plot(acc, gyro)
if PLOT3D:
    plot.plot3D(x,y,z)
else:
    plot.plotWithTime(x, y, z, t)
'''
