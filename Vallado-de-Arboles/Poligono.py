import numpy as np
import matplotlib.pyplot as plt

def IMA(P: np.array):
    """
    Estructura de la matriz de datos M:
    - Columnas 0,1: coordenadas cartesianas x,y.
    - Columnas 2,3: coordenadas polares distancia,ángulo.
    - Columnas 4,5: coordenadas cartesianas centradas en un punto i.
    - Columnas 6,7: coordenadas polares centradas en un punto i.
    """
    # Declaración de la matriz de datos
    M = np.zeros(shape = (P.shape[0],8))
    # Centroide aritmético de la lista de puntos
    centroide = P.mean(axis = 0)
    # Centralizar puntos
    M[:,0:2] = P - centroide
    # Coordenadas polares
    M[:,2] = np.sqrt(M[:,0]**2 + M[:,1]**2)
    M[:,3] = (np.arctan2(M[:,1],M[:,0])) % (2*np.pi)
    # Eliminar posibles centros
    M = M[M[:,2] != 0]
    n = M.shape[0]
    # Índice del punto a mayor distancia del centro
    indice = np.argmax(M[:,2])
    # Lista de puntos del polígono
    poligono = [M[indice,0:2]]
    # Condición de parada
    fin = False
    # Cálculo vectorizado de ángulos entre pares de puntos
    def angulo(A,B):
        Z = (A * B).sum(axis = 1) / (np.linalg.norm(A,axis = 1) * np.linalg.norm(B,axis = 1))
        # Corrección de coma flotante
        Z[Z<0.0] = 0.0
        Z[Z>1.0] = 1.0
        return np.arccos(Z)
    # Bucle para agregar puntos por iteración
    while(not fin and len(poligono) <= n):
        # Centrar nube en punto i
        M[:,4:6] = M[:,0:2] - M[indice,0:2]
        # Pasar a cordenadas polares
        M[:,6] = np.sqrt(M[:,4]**2 + M[:,5]**2)
        M[:,7] = (np.arctan2(M[:,5],M[:,4])) % (2*np.pi)
        # Ordenamos por el ángulo i (creciente) distancia i (creciente)
        M = M[np.lexsort((M[:,6], M[:,7]))]
        # Generamos índices excluyendo al 0 sobre (i,i+1) para todo n
        I1 = np.arange(start = 1, stop = n)
        I2 = np.append(np.arange(start = 2, stop = n),1)
        # Diferencia máxima de ángulo entre pares consecutivos de puntos
        indice = np.argmax(angulo(M[I1,4:6],M[I2,4:6])) + 1
        # Elegir entre el punto i o su consecutivo
        punto = M[indice,0:2] if np.any(M[indice,0:2] != poligono[-1]) else M[(indice + 1) % n,0:2]
        # Polígono cerrado
        if np.all(punto == poligono[0]): fin = True
        else: poligono.append(punto)
    return np.array(poligono) + centroide


# Ecuación implícita vectorial para lista de pares de puntos
vimplicita = lambda P: np.array([
    - (P[:,3] - P[:,1]) / (P[:,2] - P[:,0]),
    np.ones(P.shape[0]),
    - (P[:,1] - ((P[:,3] - P[:,1]) / (P[:,2] - P[:,0])) * P[:,0])
]).T

# Clasificador
def h(X: np.array, line: np.array, A: np.array, B: np.array):
    # Filtro por error de coma flotante
    mask = np.logical_not(
        ((X[:,0] == A[0]) & (X[:,1] == A[1])) | 
        ((X[:,0] == B[0]) & (X[:,1] == B[1]))
    )
    X = X[mask,:]
    predict = np.hstack((X,np.ones((X.shape[0],1)))).dot(line)
    return np.all(predict >= 0) or np.all(predict <= 0)

def CCT(P: np.array):
    # Eliminar puntos iguales
    P = np.unique(P, axis = 0)
    # Media y desviación típica
    centroide, std = P.mean(axis = 0), P.std(axis = 0)
    # Estandarización
    P = (P - centroide) / std
    # Producto cartesiano menos parejas de elemenos iguales: n^2-n
    pair = np.vstack([np.hstack((
        P[(P[:,0] != A[0]) | (P[:,1] != A[1])],np.ones((P.shape[0] - 1,2)) * A
    )) for A in P])
    # Parejas de puntos y ecuación implícita de la recta que los une
    M = np.hstack((pair,vimplicita(pair)))
    # Comprobar si la incuación deja todos los puntos a un lado
    S = np.array([h(P,m[4:7],m[0:2],m[2:4]) for m in M])
    # Aplicar filtro y obtener puntos en el polígono
    poligono = np.unique(np.append(M[S][:,0:2],M[S][:,2:4], axis = 0), axis = 0)
    # Ordenar el polígono por el ángulo
    poligono = poligono[np.argsort(np.arctan2(poligono[:,1],poligono[:,0]))]
    # Dehacer la estandarización
    P = P * std + centroide
    poligono = poligono * std + centroide
    return poligono


np.random.seed(0)
n = 10000
P = np.random.rand(n,2)
P = np.zeros((n,4))
P[:,2] = np.random.uniform(low = 0, high = np.pi * 2, size = n)
P[:,3] = np.random.randint(low = 5, high = 6, size = n)
P[:,0] = P[:,3] * np.cos(P[:,2])
P[:,1] = P[:,3] * np.sin(P[:,2])

poligono = IMA(P[:,0:2])
poligono = CCT(P[:,0:2])

plt.plot(P[:,0],P[:,1], 'ro')
plt.plot(
    np.append(poligono[:,0],poligono[0,0]),
    np.append(poligono[:,1],poligono[0,1]), 
    color = 'blue'
)
plt.show()