import numpy as np
import time
import random as rd
import pandas as pd
import math as mt
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from sklearn.preprocessing import StandardScaler

me = plt.figure(1)

def draw_polym (points, ty, text = ""):
    points_new = points.append(points.loc[0])
    plt.polar(points_new.theta,points_new.radius,ty,linewidth=1)
    plt.title(text)
    plt.draw()
    plt.waitforbuttonpress()
    me.clf()

def perimeter_fence (points):
    # Escalamos los puntos
    scaler = StandardScaler()
    scaler.fit(points)
    points[['x','y']] = scaler.transform(points)
    # Calculamos cordenadas polares
    print(points)
    points['radius'] = np.sqrt(points.x**2 + points.y**2)
    points['theta'] = np.arctan2(points.y, points.x)
    draw_polym(points,'ro', "Puntos originales")
    # Colocamos en el eje x el punto mas lejano rontando el resto
    points.theta -= points.theta[points['radius'].idxmax()]
    points.theta = (points.theta + 2 * mt.pi) % (2 * mt.pi)
    draw_polym(points,'ro', "Puntos girados")
    # Ordenamos en funcion del angulo y el modulo
    points = points.sort_values(by = ['theta','radius'])
    draw_polym(points,'r-', "Poligono")
    # Reseteamos los indices
    points = points.reset_index(drop=True)
    points['polym'] = True
    # Recalculamos las coordenadas cartesianas rotadas
    points['xn'] = points.radius * np.sin(points.theta)
    points['yn'] = points.radius * np.cos(points.theta)
    update = True
    while ((update == True) and (points.shape[0] > 3)):
        update = False
        for i in range(points.shape[0]):
            # Calibrar index a los puntos cercanos en angulos
            pre = (i - 1) % points.shape[0]
            nex = (i + 1) % points.shape[0]
            # Coeficientes de la recta entre los dos puntos
            a = (points.yn[pre] - points.yn[nex]) / (points.xn[pre] - points.xn[nex])
            b = (points.yn[pre] * points.xn[nex] - points.yn[nex] * points.xn[pre]) / (points.xn[nex] - points.xn[pre])
            # Coeficientes (0,0) a (xi,yi)
            c = points.yn[i] / points.xn[i]
            x = (-b) / (a - c)
            y = a * ((-b) / (a - c)) + b
            # Pasamos a coodenadas polares
            radius = np.sqrt(x**2 + y**2)
            if (radius >= points.radius[i]):
                points.set_value(i,'polym',False)
                update = True
        points = points[points['polym'] == True]
        #points = points.reset_index(drop=True)
        draw_polym(points, 'r-',"Poligono reducido")
    points[['x','y']] = scaler.inverse_transform(points[['x','y']])
    draw_polym(points, 'r-',"Poligono reducido")
    return (points)

def main ():
    s = 100
    n = 500
    points = pd.DataFrame(data = np.asarray([rd.uniform(-s,s) for _ in range (0, 2 * n)]).reshape(n,2), columns= ["x","y"])
    print(points)

    fence = perimeter_fence(points)

    

if __name__ == "__main__":
    main()

