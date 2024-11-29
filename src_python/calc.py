import math
from scipy.fft import fft, ifft
from scipy.signal import butter,filtfilt
import numpy  as np
from scipy.spatial.transform import Rotation as R
from filterpy.kalman import KalmanFilter
import plot
import json

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
P = np.eye(3) * 0.0001  # Schätzfehler-Kovarianzmatrix für Winkel (z.B. Roll, Pitch, Yaw)
R = np.eye(3) * 0.0001  # Messrauschen-Kovarianz (Schätzung der Messunsicherheit)
Q = np.eye(3) * 0.0001  # Prozessrauschen (Schätzung der Modellunsicherheit)


def low_pass_filter(data, alpha, count):
    """
    Filtert die Eingabedaten mit einem exponentiellen Glättungsfilter (Tiefpassfilter).
    
    :param data: Die zu filternden Daten (z.B. Beschleunigungswerte).
    :param alpha: Glättungsfaktor (0 < alpha <= 1). Je näher alpha bei 1 ist, desto weniger wird geglättet.
    :return: Gefilterte Daten.
    """
    result = data.copy()
    for j in range(count):
        filtered_data = np.zeros(data.shape)
        filtered_data[0][0] = data[0][0]  # Startwert (der erste Wert bleibt unverändert)
        filtered_data[0][1] = data[0][1]
        filtered_data[0][2] = data[0][2]
        filtered_data[0][3] = data[0][3]
    
    # Anwendung des exponentiellen Glättungsfilters
        for i in range(1, len(data[:,0])):
            filtered_data[i][0] = alpha * data[i][0] + (1 - alpha) * filtered_data[i - 1][0]
            filtered_data[i][1] = alpha * data[i][1] + (1 - alpha) * filtered_data[i - 1][1]
            filtered_data[i][2] = alpha * data[i][2] + (1 - alpha) * filtered_data[i - 1][2]
            filtered_data[i][3] = data[i][3]
        data = filtered_data.copy()
    
    result = data.copy()
    return result

##########################################################################################
##########################################################################################
##########################################################################################

def update_position(acceleration, gyro, dt):
    global POSITION, VELOCITY, ANGLE, G, P, R, Q

    # Winkelgeschwindigkeit integrieren (Gyroskop)
    ANGLE = kalman_filter(gyro, dt)  # Winkel in Rad berechnen

    # Beschleunigungswerte in Weltkoordinaten transformieren (Rotation basierend auf Winkel)
    acc_world = rotate_to_world(acceleration, ANGLE)
    #acc_world -= np.array([0.0,0.0,G])

    # Integration der Geschwindigkeit und Position (Euler-Integration)
    VELOCITY += acc_world * dt
    POSITION += VELOCITY * dt

    return POSITION, VELOCITY, ANGLE

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

def kalman_filter(gyro, dt):
    global ANGLE, P, Q
    
    # Vorhersage (Prediction Step)
    # Angenommene Winkeländerung aufgrund des Gyroskops (nur auf Gyroskopdaten basierend)
    predicted_angle = ANGLE + gyro * dt
    
    # Vorhersage der Schätzfehler-Kovarianz
    F = np.eye(3)  # Zustandetransitionsmatrix (hier als Identitätsmatrix)
    P = F @ P @ F.T + Q  # Schätzfehler-Kovarianz aktualisieren
    
    # Da wir keine Messung (angle_meas) haben, gibt es keinen "Measurement Update"
    # Der Kalman-Filter wird hier ohne externes Signal betrieben.
    
    # Korrektur der Schätzung durch Prozessrauschen und Schätzfehler
    ANGLE = predicted_angle  # Die Schätzung bleibt die gleiche, aber die Kovarianz wird angepasst
    P = P  # Keine externe Messung zur weiteren Korrektur, P bleibt unverändert
    return ANGLE

def delete_mean(arr):
    arr[:,0] = arr[:,0]-arr[0][0]
    arr[:,1] = arr[:,1]-arr[0][1]
    arr[:,2] = arr[:,2]-arr[0][2]
    #arr[:,3] = arr[:,3]-arr[0][3]
    return arr

def delete_mean_2(arr):
    arr[:,0] = arr[:,0]-np.mean(arr[:,0])
    arr[:,1] = arr[:,1]-np.mean(arr[:,1])
    arr[:,2] = arr[:,2]-np.mean(arr[:,2])
    #arr[:,3] = arr[:,3]-arr[0][3]
    return arr

def calc_delta_time(times):
    t_sum = 0
    for i in range(len(times)-1):
        t_sum += (times[i+1]-times[i])
    return (t_sum/(len(times)-1))

def preparing_for_plot(accel, gyro):
    global LAST_TIME
    dt = calc_delta_time(accel[:,3])
    LAST_TIME = accel[0][3]-dt
    route_x = []
    route_y = []
    route_z = []
    times = []
    for i in range(len(accel)):
        if accel[i][3] > LAST_TIME:
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


def preparing_json(data, accel, gyro):
    global LAST_TIME, COUNT_DATA
    dt = calc_delta_time(accel[:,3])
    LAST_TIME = accel[0][3]-dt
    for i in range(len(accel)):
        if accel[i][3] > LAST_TIME:
            dt = accel[i][3]-LAST_TIME
            LAST_TIME = accel[i][3]
            position, velocity, angle = update_position(accel[i][:3], gyro[i][:3], dt)
            neue_daten = [{"x": position[0],"y": position[1],"z": position[2],"timestamp": accel[i][3]}]
            data.extend(neue_daten)
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
