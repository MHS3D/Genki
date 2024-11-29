
import plot
import json
import test_values
import calc

PLOT3D = True
CHOOSE = 7
ALPHA = 0.85
COUNT_FILTER = 10

acc, gyro = test_values.getTestAcceleration(CHOOSE)
acc = calc.delete_mean(acc)
acc = calc.low_pass_filter(acc, ALPHA, COUNT_FILTER)
gyro = calc.delete_mean(gyro)
gyro = calc.low_pass_filter(gyro, ALPHA, COUNT_FILTER)

snip = 0
x,y,z,t = calc.preparing_for_plot(acc, gyro)

if PLOT3D:
    plot.plot3D(x,y,z)
else:
    plot.plotWithTime(x, y, z, t)
