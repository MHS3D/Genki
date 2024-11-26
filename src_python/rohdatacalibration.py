import json

import matplotlib.pyplot as plt

# Load the JSON data
with open('./data.json') as f:
    data = json.load(f)

# Extract acceleration and gyro data
acceleration = data['accel']
gyro = data['gyro']

# Calculate the average of all acceleration and gyro axes (x, y, z)
acc_x_avg = sum([entry['x'] for entry in acceleration]) / len(acceleration)
acc_y_avg = sum([entry['y'] for entry in acceleration]) / len(acceleration)
acc_z_avg = sum([entry['z'] for entry in acceleration]) / len(acceleration)

gyro_x_avg = sum([entry['x'] for entry in gyro]) / len(gyro)
gyro_y_avg = sum([entry['y'] for entry in gyro]) / len(gyro)
gyro_z_avg = sum([entry['z'] for entry in gyro]) / len(gyro)

print(f'Average acceleration (X, Y, Z): {acc_x_avg:.2f}, {acc_y_avg:.2f}, {acc_z_avg:.2f}')
print(f'Average gyro (X, Y, Z): {gyro_x_avg:.2f}, {gyro_y_avg:.2f}, {gyro_z_avg:.2f}')