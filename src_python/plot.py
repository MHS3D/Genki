from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy  as np

def plot3D(x,y,z):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    # Data for a three-dimensional line
    fig.suptitle("Bewegung - 3D Ansicht ")
    ax.set_title('Strecke Ergebnis')
    ax.set_xlabel('x-Achse')
    ax.set_ylabel('y-Achse')
    ax.set_zlabel('z-Achse')
    ax.plot3D(x,y,z,'green')
    plt.show()
    fig = plt.figure()
    ax = plt.axes(projection='3d')

def plot3D_2(x,y,z,x1,y1,z1):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    # Data for a three-dimensional line
    fig.suptitle("Bewegung - 3D Ansicht ")
    ax.set_title('Strecke Ergebnis')
    ax.set_xlabel('x-Achse')
    ax.set_ylabel('y-Achse')
    ax.set_zlabel('z-Achse')
    ax.plot3D(x,y,z,'green')
    ax.plot3D(x1,y1,z1,'blue')
    plt.show()
    fig = plt.figure()
    ax = plt.axes(projection='3d')

def plot2D(x,y,axis):
    if axis == "xy":
        plt.xlabel("x-achse")
        plt.ylabel("y-achse")
    elif axis == "xz":
        plt.xlabel("x-achse")
        plt.ylabel("z-achse")
    elif axis == "yz":
        plt.xlabel("y-achse")
        plt.ylabel("z-achse")
    plt.plot(x,y)
    plt.show()

def plotWithTime(x,y,z,t):
    plt.ylabel("value")
    plt.xlabel("time")
    plt.plot(t,x, "blue")
    plt.plot(t,y, "green")
    plt.plot(t,z, "red")
    plt.show()

def plotSingle(x,t):
    plt.ylabel("value")
    plt.xlabel("time")
    plt.plot(t,x, "blue")
    plt.show()

def plotTowArrays(x,y,t):
    plt.ylabel("value")
    plt.xlabel("time")
    plt.plot(t,x, "red")
    plt.plot(t,y, "green")
    plt.show()