
import plot
import json
import test_values
import calc

PLOT3D = True
CHOOSE = 7
ALPHA = 0.85
COUNT_FILTER = 100

acc, gyro = test_values.getTestAcceleration(CHOOSE)
acc1 = acc.copy()
acc[:,2] = 0
acc = calc.delete_mean(acc)
acc = calc.low_pass_filter(acc, ALPHA, COUNT_FILTER)
gyro = calc.delete_mean(gyro)
gyro = calc.low_pass_filter(gyro, ALPHA, COUNT_FILTER)

#plot.plotWithTime2(acc[:,0], acc[:,1], acc[:,2], acc[:,3], acc1[:,0], acc1[:,1], acc1[:,2], acc1[:,3])
snip = 0
x,y,z,t = calc.preparing_for_plot(acc, gyro)

if PLOT3D:
    plot.plot3D(x,y,z)
else:
    plot.plotWithTime(x, y, z, t)
