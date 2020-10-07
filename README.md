# Vallado de Árboles

### 1. Descripción

El problema del Vallado de Árboles consiste en determinar dado un conjunto de árboles (puntos) en un espacio 2D el subconjunto que forme el perímetro del vallado mínimo. Todo árbol que no forme parte del perímetro debe quedar dentro del área que lo forma.

### 2. Solución: Iteración por maximización del ángulo (IMA)

La solución a este problema se puede describir mediante los siguientes pasos:

1. Determinar el punto más alejado del centroide de la nube.
2. Agregar al polígono 1 de los 2 puntos que forman la pareja de puntos consecutivos (ordenados por el ángulo) con mayor diferencia de ángulo entre sí desde la perspectiva del último añadido al polígono como centro de coordenadas.

### 3. Solución: Combinación de clasificadores totales (CCT)

1. Generar las $n^2-n$ rectas para las combinaciones de pares de puntos.
2. Determinar el subconjunto de las rectas que dividen el plano dejando los $n$ puntos a un lado.

### 4. Eficiencia

Cota superior asintótica

$$
O\left ( g\left ( x \right ) \right )=\begin{Bmatrix}
f\left ( x \right ): \textup{existen}\:  x_0,c \: \textup{tales que}\\ 
\forall x\geq x_0> 0:0\leq \left | f\left ( x \right ) \right |\leq c\left | g\left ( x \right )) \right |
\end{Bmatrix}
$$

#### 4.1 Eficiencia teórica

Iteración por maximización del ángulo:
$$O(n^2\cdot log(n))$$

Combinación de clasificadores totales:
$$O(n^4)$$


#### 4.2 Eficiencia empírica

