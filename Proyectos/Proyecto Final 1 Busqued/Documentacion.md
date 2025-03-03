# Errores dentro del codigo y su ejecucion que eh encontrado 

## Problema 1
 -Existe un problema en el que no existe un limite al dibujar las paredes al salir el curso de la ventana se genera un error que detiene la ejecucion 
   "Exception has occurred: IndexError
list index out of range
  File "C:\Users\avila\OneDrive\Escritorio\IA\Proyecto Final 1 Busqued\Aasterisco.py", line 109, in main
    nodo = grid[fila][col]
           ~~~~^^^^^^
  File "C:\Users\avila\OneDrive\Escritorio\IA\Proyecto Final 1 Busqued\Aasterisco.py", line 133, in <module>
    main(VENTANA, ANCHO_VENTANA)
IndexError: list index out of range"


# Problematicas a resolver 

## Problema 1 
 - Resolver que no intente dibujar y se detenga la ejecucion del codigo

## Problema 2


# Soluciones del codigo para los problemas 

## Solucion al problema 1
- En este caso podemos decir que las coordenadas "fila" y "col" pueden ser mayores que el número de filas o columnas al dar click fuera de los bordes lo que ocasiona un crasheo, en este caso la solución fue crear una validación que verifica si las coordenadas están dentro del rango válido. 

```Python 
def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    # Fila y columna en la que se hizo click exeptuando los bordes
    fila = min(max(y // ancho_nodo, 0), filas - 1)
    col = min(max(x // ancho_nodo, 0), filas - 1)
    return fila, col
```



