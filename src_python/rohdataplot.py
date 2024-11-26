import json

import matplotlib.pyplot as plt

# Load the JSON data
with open('./roh_einfach_laufend.json') as f:
    data = json.load(f)

# Extract acceleration and gyro data
acceleration = data['accel']
gyro = data['gyro']

# Extract timestamps and x, y, z values for acceleration
acc_timestamps = [entry['timestamp'] for entry in acceleration]
acc_x = [entry['x'] for entry in acceleration]
acc_y = [entry['y'] for entry in acceleration]
acc_z = [entry['z'] for entry in acceleration]

# Extract timestamps and x, y, z values for gyro
gyro_timestamps = [entry['timestamp'] for entry in gyro]
gyro_x = [entry['x'] for entry in gyro]
gyro_y = [entry['y'] for entry in gyro]
gyro_z = [entry['z'] for entry in gyro]

# Plot acceleration data
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(acc_timestamps, acc_x, label='X')
plt.plot(acc_timestamps, acc_y, label='Y')
plt.plot(acc_timestamps, acc_z, label='Z')
plt.title('Acceleration Data')
plt.xlabel('Timestamp')
plt.ylabel('Acceleration')
plt.legend()

# Plot gyro data
plt.subplot(2, 1, 2)
plt.plot(gyro_timestamps, gyro_x, label='X')
plt.plot(gyro_timestamps, gyro_y, label='Y')
plt.plot(gyro_timestamps, gyro_z, label='Z')
plt.title('Gyro Data')
plt.xlabel('Timestamp')
plt.ylabel('Gyro')
plt.legend()

plt.tight_layout()
plt.show()