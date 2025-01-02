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
POSITION = np.zeros(3)  # Startposition (x, y, z)
VELOCITY = np.zeros(3)  # Anfangsgeschwindigkeit (x, y, z)
ANGLE = np.zeros(3)    # Orientierung (Roll, Pitch, Yaw)
DRIFT = np.zeros(3)     # Startwert für den Drift des Gyroskops

LAST_TIME = 0
JSON_DATA = []
COUNT_DATA = 0
P = np.eye(12) * 0.0001  # Schätzfehler-Kovarianzmatrix für Winkel (z.B. Roll, Pitch, Yaw)
R = np.eye(3) * 0.0001  # Messrauschen-Kovarianz (Schätzung der Messunsicherheit)
Q = np.eye(12) * 0.0001  # Prozessrauschen (Schätzung der Modellunsicherheit)


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
    global POSITION, VELOCITY, ANGLE, DRIFT, P, Q, R, G

    # Winkelgeschwindigkeit integrieren (Gyroskop)
    ANGLE += gyro * dt # Winkel in Rad berechnen

    # Beschleunigungswerte in Weltkoordinaten transformieren (Rotation basierend auf Winkel)
    #acceleration -= np.array([0.0,0.0,G])
    acc_world = rotate_to_world(acceleration, ANGLE)
    

    if np.linalg.norm(VELOCITY) < 0.01:  # Wenn Geschwindigkeit fast null ist, verwenden wir ZUPT
        #print("ZUPT-Korrektur angewendet: Geschwindigkeit auf Null gesetzt")
        VELOCITY = np.zeros(3)  # Geschwindigkeit auf Null setzen

    # Integration der Geschwindigkeit und Position (Euler-Integration)
    VELOCITY += acc_world * dt
    POSITION += 0.5*VELOCITY * dt
    POSITION, VELOCITY, ANGLE, P = kalman_filter_update(gyro, dt)
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

def kalman_filter_update(gyro, dt):
    global POSITION, VELOCITY, ANGLE, DRIFT, P, R, Q, P_update
    # Vorhersage der nächsten Zustände
    # Zustand: [Position, Geschwindigkeit, Winkel, Drift]
    dim = 3
    x_pred = np.hstack([POSITION, VELOCITY, ANGLE, DRIFT])  # Vektor des aktuellen Zustands
    length = len(x_pred)
    F = np.eye(length) #* dt  # Übergangsmatrix (Identität, da wir nur eine einfache Integration haben)

    F[0:3, 3:6] = np.eye(dim) * dt  # Geschwindigkeit beeinflusst die Position
    F[6:9, 9:12] = np.eye(dim) * dt  # Drift beeinflusst den Winkel
    # Vorhersage des neuen Zustands
    x_pred = F @ x_pred
    # Vorhersage der Kovarianz
    P_pred = F @ P @ F.T + Q

    # Messung: Gyroskop (Winkelgeschwindigkeit)
    z = gyro  # Gyroskopmessungen

    # Messmodell: Der aktuelle Winkel sollte sich durch die Geschwindigkeit des Gyroskops ändern
    H = np.zeros((dim, length))  # Messmatrix

    # Kalman-Gewicht
    S = H @ P_pred @ H.T + R  # Messunsicherheit
    K = P_pred @ H.T @ np.linalg.inv(S)  # Kalman-Verstärkung

    # Update des Zustands
    x_update = x_pred + K @ (z - H @ x_pred)

    # Update der Schätzfehler-Kovarianz
    P_update = (np.eye(12) - K @ H) @ P_pred

    return x_update[:dim], x_update[dim:dim*2], x_update[dim*2:dim*3], P_update

def delete_mean(arr):
    arr[:,0] = arr[:,0]-arr[0][0]
    arr[:,1] = arr[:,1]-arr[0][1]
    arr[:,2] = arr[:,2]-arr[0][2]
    #arr[:,3] = arr[:,3]-arr[0][3]
    return arr

def calc_delta_time(times):
    t_sum = 0
    count = 0
    for i in range(len(times)-1):
        if times[i+1] > times[i]:
            t_sum += (times[i+1]-times[i])
            count += 1
    return (t_sum/count)

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
