#Proyecto de IA
#Daniel Avila Vergara

#Importamos la libreria de pygame
import pygame
#Importamos la libreria de fuentes
pygame.font.init()
#Importamos heapq para la cola de prioridad
import heapq

# Configuraciones iniciales
# Cambio del tamaño de ventana de 800x800 a 500x500
ANCHO_VENTANA = 500
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de Nodos")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
GRIS_CLARO = (192, 192, 192)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)
AMARILLO_NEON = (255, 255, 102)
AMARILLO = (255, 255, 0)


class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        #Fuente usada y tamaño de la fuente para las coordenadas dentro de los cuadros dibujados
        self.fuente =pygame.font.SysFont("Arial", 8)

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA

    def restablecer(self):
        self.color = BLANCO

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = GRIS_CLARO

    def hacer_fin(self):
        self.color = PURPURA
    
    #Lista abierta
    def hacer_abierto(self):
        self.color = VERDE
    
    #Lista Cerrada
    def hacer_cerrado(self):
        self.color = ROJO
    
    #Vecinos 
    def hacer_camino(self):
        self.color = AMARILLO_NEON

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
    
    #Agregar los vecinos al hacer el calculo 
    def actualizar_vecinos(self,grid):
        self.vecinos = []
        if self.fila < self.total_filas - 1 and not grid[self.fila + 1][self.col].es_pared():  # Abajo
            self.vecinos.append(grid[self.fila + 1][self.col])
        if self.fila > 0 and not grid[self.fila - 1][self.col].es_pared():  # Arriba
            self.vecinos.append(grid[self.fila - 1][self.col])
        if self.col < self.total_filas - 1 and not grid[self.fila][self.col + 1].es_pared():  # Derecha
            self.vecinos.append(grid[self.fila][self.col + 1])
        if self.col > 0 and not grid[self.fila][self.col - 1].es_pared():  # Izquierda
            self.vecinos.append(grid[self.fila][self.col - 1])
    

def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    # Fila y columna en la que se hizo click exeptuando los bordes
    fila = min(max(y // ancho_nodo, 0), filas - 1)
    col = min(max(x // ancho_nodo, 0), filas - 1)
    return fila, col

#Definir la funcion heuristica
def heuristica(nodo1, nodo2):
    x1,y1 = nodo1.get_pos()
    x2,y2 = nodo2.get_pos()
    return abs(x1 - x2) + abs(y1 - y2)  

#Definir la funcion para reconstruir el camino
def reconstruir_camino(came_from, actual, dibujar):
    while actual in came_from:
        actual = came_from[actual]
        actual.hacer_camino()
        dibujar()

#Definir la funcion para el algoritmo A*
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
        
        for vecino in actual.vecinos:
            temp_g_score = g_score[actual] + 1
            
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
            
#Funcion principal implementando el algoritmo A*
def main(ventana, ancho):
    FILAS = 10
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None

    corriendo = True

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
                
            #Funcion para reiniciar todo sin tener que borrar 1x1 usando ctrl+r
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    for fila in grid:
                        for nodo in fila:
                            nodo.restablecer()
                    inicio = None
                    fin = None
                    
                #Implementacion del algoritmo A*
                if event.key == pygame.K_SPACE and inicio and fin:
                    for fila in grid:
                        for nodo in fila:
                            nodo.actualizar_vecinos(grid)
                    algoritmo_A_asterisco(lambda: dibujar(ventana, grid, FILAS, ancho), grid, inicio, fin)

            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()

                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()

                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:  # Click derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)