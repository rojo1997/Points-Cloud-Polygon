# Vallado de Árboles

## Descripción

El problema del Vallado de Árboles consiste en determinar dado un conjunto de árboles en un espacio 2D el subconjunto que forme el perímetro del vallado para todo el conjunto. Todo árbol que no forme parte del perímetro debe quedar dentro del áerea que lo forma.

## Solución

La solución a este problema se puede describir mediante los siguientes pasos:

1. Restar al conjunto de puntos su centroide.
2. Pasar de coordenadas cartesianas a coordenadas polares.
3. Ordenar el conjunto por el ángulo (indiferente) y la distancia (decreciente).
4. Para subconjuntos que presenten mismo ángulo pero diferente distancia reducir al de mayor distancia.
5. Iterar mediante ternas del tipo ((i-1) mod #D, i, (i+1) mod #D) sobre D
