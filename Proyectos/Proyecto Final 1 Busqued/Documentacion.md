# Cambios en el codigo base 
- Se cambio el tamaño de la ventana de 800x800 a 500x500
- Se agrego la posibilidad de poder ver en cada casilla el numero correspondiente a esa casilla 
- Se agrego la posibilidad de poder ver las coordenadas en cada casilla
```Python 
#Inicio de las fuentes 
pygame.font.init()

#Fuente usada y tamaño de la fuente para las coordenadas dentro de los cuadros dibujados
self.fuente =pygame.font.SysFont("Arial", 8)

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))
        #Llamado a la funcion para dibujar los numeros en cada casilla
        self.dibujar_numero(ventana)
        self.dibujar_coordenadas(ventana)
        
    #Funcion para dibujar el numero dentro de las casillas
    def dibujar_numero(self, ventana):
        numero = self.col * self.total_filas + self.fila + 1
        texto = self.fuente.render(str(numero), True, NEGRO)
        ventana.blit(texto, (self.x + 5, self.y + 5))
        
    #Dibujar coordenadas
    def dibujar_coordenadas(self, ventana):
        coordenadas = f"({self.fila}, {self.col})"
        texto = self.fuente.render(coordenadas, True, NEGRO)
        ventana.blit(texto, (self.x + 5, self.y + 15))
```

- Se agrego la capacidad de borrar las paredes, punto de inicio y punto final usando la combinacion de teclas "ctrl+r", lo que facilita reiniciar todo sin tener que borrar uno por uno, esto se agrego dentro del bucle principal del codigo
  
```Python
 #Funcion para reiniciar todo sin tener que borrar 1x1 usando ctrl+r
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    for fila in grid:
                        for nodo in fila:
                            nodo.restablecer()
                    inicio = None
                    fin = None
```

- En este caso para la implementacion del algoritmo A* tomare encuenta los apuntes que nos dio el profesor, en donde viene el primer pseudocodigo de lo que tiene que hacer nuestro programa, para este caso tuvimos que analizar cada parte del pseudocodigo para llegar a las partes del codigo que tendriamos que agregar.

El Algoritmo se basa en los siguientes pasos:

Etapas del Algoritmo

- Inicialización:
Se parte de un nodo inicial (el punto de partida) y se agrega a una estructura de datos (generalmente una cola de prioridad).
Cada nodo tiene un valor de f(n), calculado como la suma de g(n) y h(n) , donde g(n) es 0 para el nodo inicial y h(n) es el valor heurístico estimado.

- Expansión de Nodos:
En cada paso, el algoritmo extrae el nodo con el menor valor f(n) de la cola de prioridad. Luego, el algoritmo expande este nodo, es decir, explora todos sus nodos vecinos.
Para cada vecino, se calcula el nuevo costo g(n) como la distancia acumulada desde el nodo inicial y se actualiza el valor de f(n)

- Actualización de Nodos Vecinos:
Si un vecino aún no ha sido explorado, o si se ha encontrado un camino más corto a dicho vecino, se actualizan sus valores de g(n) y f(n) , y se agrega a la cola de prioridad para ser evaluado más adelante.

- Heurística:
La heurística h(n) es crucial para guiar la búsqueda hacia el objetivo. Una buena heurística hace que A* sea más eficiente, ya que prioriza la expansión de los nodos más prometedores.
Las heurísticas comunes incluyen la distancia Manhattan (para cuadrículas donde solo se puede mover en horizontal o vertical) y la distancia Euclidiana (para espacios donde se puede mover en diagonal).

- Terminación:
El algoritmo termina cuando se extrae el nodo objetivo (el nodo final) de la cola de prioridad, lo que significa que se ha encontrado el camino más corto.

- Reconstrucción del Camino:
Una vez que se ha encontrado el nodo final, el camino se reconstruye retrocediendo desde el nodo final al nodo inicial a través de los nodos predecesores.

En este caso podemos ver que son pasos algo complejos pero podemos en este caso expresarlos en codigo sin problema, la siguiente parte podemos ver como se implemento este pseudocodigo en el codigo cascaron:

## Aplicacion de pseudocodigo dentro del cascaron

- Inicio 
Antes de empezar hacemos una pequeña configuracion para saber cuales seran los colores que representaran los cuadros vecinos y tambien cuales seran los colores para los cuadros que estaran en la lista abierta y en la lista cerrada

```Python

 #Lista abierta
    def hacer_abierto(self):
        self.color = VERDE
    
    #Lista Cerrada
    def hacer_cerrado(self):
        self.color = ROJO
    
    #Vecinos 
    def hacer_camino(self):
        self.color = AMARILLO_NEON
```

1. Nodos y valores 
Se crea una funcion para darle valores a cada cuadricula como lo hicimos en este caso durante las practicas, siendo movimiento vertical y horizontal de 10 y diagonales en 14

```Python
def actualizar_vecinos(self, grid):
        self.vecinos = []
        # Movimientos verticales y horizontales
        if self.fila < self.total_filas - 1 and not grid[self.fila + 1][self.col].es_pared():  # Abajo
            self.vecinos.append((grid[self.fila + 1][self.col], 10))
        if self.fila > 0 and not grid[self.fila - 1][self.col].es_pared():  # Arriba
            self.vecinos.append((grid[self.fila - 1][self.col], 10))
        if self.col < self.total_filas - 1 and not grid[self.fila][self.col + 1].es_pared():  # Derecha
            self.vecinos.append((grid[self.fila][self.col + 1], 10))
        if self.col > 0 and not grid[self.fila][self.col - 1].es_pared():  # Izquierda
            self.vecinos.append((grid[self.fila][self.col - 1], 10))
        
        # Movimientos diagonales
        if self.fila < self.total_filas - 1 and self.col < self.total_filas - 1 and not grid[self.fila + 1][self.col + 1].es_pared():  # Abajo-Derecha
            self.vecinos.append((grid[self.fila + 1][self.col + 1], 14))
        if self.fila < self.total_filas - 1 and self.col > 0 and not grid[self.fila + 1][self.col - 1].es_pared():  # Abajo-Izquierda
            self.vecinos.append((grid[self.fila + 1][self.col - 1], 14))
        if self.fila > 0 and self.col < self.total_filas - 1 and not grid[self.fila - 1][self.col + 1].es_pared():  # Arriba-Derecha
            self.vecinos.append((grid[self.fila - 1][self.col + 1], 14))
        if self.fila > 0 and self.col > 0 and not grid[self.fila - 1][self.col - 1].es_pared():  # Arriba-Izquierda
            self.vecinos.append((grid[self.fila - 1][self.col - 1], 14))
```


1. Inicialización 
Para esta parte necesitamos realizar las estructuras para poder calcular los valores iniciales para el nodo inicial.

```Python
def algoritmo_A_asterisco(dibujar, grid, inicio, fin):
    count = 0
    abiertos = []
    heapq.heappush(abiertos, (0, count, inicio))
    came_from = {}
    g_score = {nodo: float("inf") for fila in grid for nodo in fila}
    g_score[inicio] = 0
    f_score = {nodo: float("inf") for fila in grid for nodo in fila}
    f_score[inicio] = heuristica(inicio, fin)
    
    abiertos_hash = {inicio}
```

2. Expansión de Nodos
Despues de la inicializacion se agarra el modo con menor valor, explorando los vecinos.

```Python
   while abiertos:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        actual = heapq.heappop(abiertos)[2]
        abiertos_hash.remove(actual)
        
        if actual == fin:
            reconstruir_camino(came_from, fin, dibujar)
            fin.hacer_fin()
            return True
        
        for vecino, costo in actual.vecinos:
            temp_g_score = g_score[actual] + costo
```

3. Actualización de Nodos Vecinos
En este apartado para cada vecino se calcula su costo y se actualiza el valor, en esta parte sucede el evento que al encontrar un camino mas corto a un vecino se actualizaran sus valores.

```python
        if temp_g_score < g_score[vecino]:
                came_from[vecino] = actual
                g_score[vecino] = temp_g_score
                f_score[vecino] = temp_g_score + heuristica(vecino, fin)
                if vecino not in abiertos_hash:
                    count += 1
                    heapq.heappush(abiertos, (f_score[vecino], count, vecino))
                    abiertos_hash.add(vecino)
                    vecino.hacer_abierto()
        
        dibujar()
        
        if actual != inicio:
            actual.hacer_cerrado()
```

4. Heurística
En esta parte se hace el calculo de manhattan entre dos nodos.

```python
def heuristica(nodo1, nodo2):
    x1, y1 = nodo1.get_pos()
    x2, y2 = nodo2.get_pos()
    return (abs(x1 - x2) + abs(y1 - y2))*10
```

5. Terminación
Cuando se terminan los calculos anteriores, se extrae el nodo objetivo, lo que podemos entender como que se a encontrado el camino mas corto.

```python
        if actual == fin:
            reconstruir_camino(came_from, fin, dibujar)
            fin.hacer_fin()
            return True
```

6. Reconstrucción del Camino
Cuando encontramos el nodo final se construye el camino retrocediendo del nodo final al nodo inicial 

```python
def reconstruir_camino(came_from, actual, dibujar):
    while actual in came_from:
        actual = came_from[actual]
        actual.hacer_camino()
        dibujar()
```
- * Ver error 2 *

# Errores dentro del codigo y su ejecucion que eh encontrado 

## Problema 1
- Existe un problema en el que no existe un limite al dibujar las paredes al salir el curso de la ventana se genera un error que detiene la ejecucion 
   "Exception has occurred: IndexError
list index out of range
  File "C:\Users\avila\OneDrive\Escritorio\IA\Proyecto Final 1 Busqued\Aasterisco.py", line 109, in main
    nodo = grid[fila][col]
           ~~~~^^^^^^
  File "C:\Users\avila\OneDrive\Escritorio\IA\Proyecto Final 1 Busqued\Aasterisco.py", line 133, in <module>
    main(VENTANA, ANCHO_VENTANA)
IndexError: list index out of range"

## Problemas 2 
- Durante la ejecucion si busca el camino mas corto, pero ignora las paredes

## Problema 3
- En este caso descubri  que cuando cambio el costo del valor del movimiento de 1 , 1.4 a 10 o 14 respectivamente, hay un error en el que la busqueda busca recorrer todo el mapa causando errores.


# Problematicas a resolver 

## Problema 1 
 - Resolver que intente dibujar fuera de los limites y se detenga la ejecucion del codigo * (Resuleto) * 

## Problema 2
 - Ignora las paredes y no hace la ruta 

## Problema 3
 - Hace un calculo raro en el que explora todo el mapa, lo cual no es correcto 

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

## Solucion al problema 2
- Se acomodo el color de las paredes porque al parecer eso genera errores al momento de hacer el calculo 

## Solucion al problema 3
- No mover los calculos ya que son los ideales para poder hacer el calculo tomando en cuenta los costos existentes

