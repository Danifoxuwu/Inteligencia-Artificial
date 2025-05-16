import pygame
import random
import os

# Inicializar Pygame
pygame.init()

# Inicializar el mezclador de sonido
pygame.mixer.init()

# Dimensiones de la pantalla
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego: Disparo de Bala, Salto, Nave y Menú")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Variables del jugador, bala, nave, fondo, etc.
jugador = None
bala = None
fondo = None
nave = None
menu = None

# Variables de la bala vertical
bala_vertical = None
velocidad_bala_vertical = 4  #velocidad *ajustar despues
bala_vertical_disparada = False
tiempo_ultimo_disparo = 0

# Variables de salto
salto = False
salto_altura = 15  # Velocidad inicial de salto
gravedad = 1
en_suelo = True

# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False  # Indica si el modo de juego es automático

# Lista para guardar los datos de velocidad, distancia y salto (target)
datos_modelo = []

# Cargar las imágenes
base_path = os.path.dirname(__file__)

jugador_frames = [
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/kirby 1.png')), (48, 48)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/kirby 2.png')), (48, 48)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/kirby 3.png')), (48, 48)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/kirby 4.png')), (48, 48)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/kirby 5.png')), (48, 48)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/kirby 6.png')), (48, 48)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/kirby 7.png')), (48, 48)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/kirby 8.png')), (48, 48)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/kirby 9.png')), (48, 48)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/kirby 10.png')), (48, 48))
]


bala_frames = [
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/apple1.png')), (40, 40)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/apple2.png')), (40, 40)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/apple3.png')), (40, 40)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/apple4.png')), (40, 40)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/apple5.png')), (40, 40)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/apple6.png')), (40, 40))
]

# Escalar los frames de la nave para hacerlos más grandes
nave_frames = [
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/enemigo1.png')), (80, 80)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/enemigo2.png')), (80, 80)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/enemigo3.png')), (80, 80)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/enemigo4.png')), (80, 80)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/enemigo5.png')), (80, 80)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/enemigo6.png')), (80, 80))
]

fondo_img = pygame.image.load(os.path.join(base_path, 'assets 2/Radish Ruins 1.png'))
menu_img = pygame.image.load(os.path.join(base_path, 'assets/game/menu.png'))

# Cargar la música de fondo
musica_fondo = os.path.join(base_path, 'assets 2/music/Kirby Nightmare in Dreamland .ogg')
pygame.mixer.music.load(musica_fondo)

# Configurar el volumen de la música (opcional)
pygame.mixer.music.set_volume(0.5)  # Volumen entre 0.0 y 1.0

# Escalar la imagen de fondo para que coincida con el tamaño de la pantalla
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear el rectángulo del jugador y de la bala
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)
menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)  # Tamaño del menú

bala_vertical = pygame.Rect(jugador.x + 16, 0, 16, 16) 

# Variables para la animación del jugador
current_frame = 0
frame_speed = 10  # Cuántos frames antes de cambiar a la siguiente imagen
frame_count = 0
# Variables para el movimiento del jugador
pos_x_min = 20  # Límite mínimo de movimiento hacia la izquierda
pos_x_max = 100  # Límite máximo de movimiento hacia la derecha
velocidad_x = 50  # Velocidad de movimiento lateral

# Variables para el retroceso automático
retrocediendo = False
tiempo_movimiento = 0
TIEMPO_RETORNO = 1500  # milisegundos (1.5 segundos)
posicion_origen = (50, h - 100)

# Variables para la bala
velocidad_bala = -10  # Velocidad de la bala hacia la izquierda
bala_disparada = False

# Variables para la animación de la bala
bala_frame_actual = 0
bala_frame_contador = 0
bala_frame_velocidad = 5  # Velocidad de cambio de frame

# Variables para la animación de la nave
nave_frame_actual = 0
nave_frame_contador = 0
nave_frame_velocidad = 7  # Velocidad de cambio de frame

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w

# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-8, -3)  # Velocidad aleatoria negativa para la bala
        bala_disparada = True

# Función para disparar la bala vertical
def disparar_bala_vertical():
    global bala_vertical_disparada, bala_vertical
    if not bala_vertical_disparada:
        bala_vertical.x = jugador.x + 16  # Centrar la bala con el jugador
        bala_vertical.y = 0  # Iniciar desde la parte superior
        bala_vertical_disparada = True

# Función para reiniciar la posición de la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50  # Reiniciar la posición de la bala
    bala_disparada = False

# Función para manejar el salto
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura  # Mover al jugador hacia arriba
        salto_altura -= gravedad  # Aplicar gravedad (reduce la velocidad del salto)

        # Si el jugador llega al suelo, detener el salto
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15  # Restablecer la velocidad de salto
            en_suelo = True


# Función para actualizar el juego
def update(permitir_bala_vertical=True):
    global bala, velocidad_bala, current_frame, frame_count, fondo_x1, fondo_x2, bala_vertical, bala_vertical_disparada, tiempo_ultimo_disparo, bala_frame_actual, bala_frame_contador, nave_frame_actual, nave_frame_contador

    # Lógica para disparar la bala vertical aleatoriamente (solo si está permitido)
    tiempo_actual = pygame.time.get_ticks()
    if permitir_bala_vertical and not bala_vertical_disparada and tiempo_actual - tiempo_ultimo_disparo > random.randint(2000, 5000):
        disparar_bala_vertical()
        tiempo_ultimo_disparo = tiempo_actual


    # Mover el fondo
    fondo_x1 -= 1
    fondo_x2 -= 1

    # Si el primer fondo sale de la pantalla, lo movemos detrás del segundo
    if fondo_x1 <= -w:
        fondo_x1 = w

    # Si el segundo fondo sale de la pantalla, lo movemos detrás del primero
    if fondo_x2 <= -w:
        fondo_x2 = w

    # Dibujar los fondos
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    # Dibujar el jugador con la animación
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))

    # Animación de la nave
    nave_frame_contador += 1
    if nave_frame_contador >= nave_frame_velocidad:
        nave_frame_actual = (nave_frame_actual + 1) % len(nave_frames)
        nave_frame_contador = 0

    # Dibujar la nave animada
    pantalla.blit(nave_frames[nave_frame_actual], (nave.x, nave.y))

    # Mover y dibujar la bala
    if bala_disparada:
        bala.x += velocidad_bala

    # Si la bala sale de la pantalla, reiniciar su posición
    if bala.x < 0:
        reset_bala()

    # Animación de la bala
    bala_frame_contador += 1
    if bala_frame_contador >= bala_frame_velocidad:
        bala_frame_actual = (bala_frame_actual + 1) % len(bala_frames)
        bala_frame_contador = 0

    # Dibujar la bala animada
    pantalla.blit(bala_frames[bala_frame_actual], (bala.x, bala.y))

    # Mover y dibujar la bala vertical
    if bala_vertical_disparada:
        bala_vertical.y += velocidad_bala_vertical
        
        # Si la bala llega al suelo, resetearla
        if bala_vertical.y > h:
            bala_vertical_disparada = False
        
        # Animación de la bala vertical
        bala_frame_contador += 1
        if bala_frame_contador >= bala_frame_velocidad:
            bala_frame_actual = (bala_frame_actual + 1) % len(bala_frames)
            bala_frame_contador = 0

        # Dibujar la bala vertical animada
        pantalla.blit(bala_frames[bala_frame_actual], (bala_vertical.x, bala_vertical.y))
        
        # Colisión con el jugador
        if jugador.colliderect(bala_vertical):
            print("Colisión con bala vertical detectada!")
            reiniciar_juego()

    # Colisión entre la bala y el jugador
    if jugador.colliderect(bala):
        print("Colisión detectada!")
        reiniciar_juego()  # Terminar el juego y mostrar el menú

# Función para guardar datos del modelo en modo manual (solo en memoria)
def guardar_datos(accion):
    global jugador, bala, bala_vertical, velocidad_bala, salto
    distancia_horizontal = abs(jugador.x - bala.x)
    distancia_vertical = abs(jugador.y - bala_vertical.y)
    if bala_vertical.y > jugador.y:  # Si la bala está por debajo del jugador
        distancia_vertical = 0  # Distancia vertical es 0 si ya pasó al jugador

    # Guardar velocidad de la bala, distancias, posiciones del jugador y acción tomada
    datos_modelo.append({
        "velocidad_bala": velocidad_bala,
        "distancia_horizontal": distancia_horizontal,
        "distancia_vertical": distancia_vertical,
        "jugador_pos": (jugador.x, jugador.y),
        "accion": accion
    })
    # Imprimir los datos guardados
    print(f"Datos guardados: Velocidad Bala: {velocidad_bala}, "
          f"Distancia Horizontal: {distancia_horizontal}, Distancia Vertical: {distancia_vertical}, "
          f"Posición Jugador: {jugador.x, jugador.y}, Acción: {accion}")

# Función para pausar el juego y guardar los datos
def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
    else:
        print("Juego reanudado.")

# Función para mostrar el menú y seleccionar el modo de juego
def mostrar_menu():
    global menu_activo, modo_auto

    # Colores para los botones
    COLOR_BOTON = (100, 100, 255)
    COLOR_TEXTO = (255, 255, 255)
    COLOR_BOTON_HOVER = (150, 150, 255)

    # Crear botones
    boton_auto = pygame.Rect(w // 2 - 100, h // 2 - 60, 200, 50)
    boton_manual = pygame.Rect(w // 2 - 100, h // 2, 200, 50)
    boton_salir = pygame.Rect(w // 2 - 100, h // 2 + 60, 200, 50)

    while menu_activo:
        pantalla.fill(NEGRO)

        # Obtener la posición del mouse
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # Dibujar botones con hover
        pygame.draw.rect(pantalla, COLOR_BOTON_HOVER if boton_auto.collidepoint(mouse_pos) else COLOR_BOTON, boton_auto)
        pygame.draw.rect(pantalla, COLOR_BOTON_HOVER if boton_manual.collidepoint(mouse_pos) else COLOR_BOTON, boton_manual)
        pygame.draw.rect(pantalla, COLOR_BOTON_HOVER if boton_salir.collidepoint(mouse_pos) else COLOR_BOTON, boton_salir)

        # Dibujar texto en los botones
        texto_auto = fuente.render("Modo Auto (A)", True, COLOR_TEXTO)
        texto_manual = fuente.render("Modo Manual (M)", True, COLOR_TEXTO)
        texto_salir = fuente.render("Salir (Q)", True, COLOR_TEXTO)
        pantalla.blit(texto_auto, (boton_auto.x + 20, boton_auto.y + 10))
        pantalla.blit(texto_manual, (boton_manual.x + 20, boton_manual.y + 10))
        pantalla.blit(texto_salir, (boton_salir.x + 20, boton_salir.y + 10))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # Click izquierdo
                if boton_auto.collidepoint(mouse_pos):
                    modo_auto = True
                    menu_activo = False
                elif boton_manual.collidepoint(mouse_pos):
                    modo_auto = False
                    menu_activo = False
                elif boton_salir.collidepoint(mouse_pos):
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()
            if evento.type == pygame.KEYDOWN:  # Atajos de teclado
                if evento.key == pygame.K_a:
                    modo_auto = True
                    menu_activo = False
                elif evento.key == pygame.K_m:
                    modo_auto = False
                    menu_activo = False
                elif evento.key == pygame.K_q:
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

    # Iniciar la música de fondo al salir del menú
    pygame.mixer.music.play(-1)  # -1 para reproducir en bucle infinito

# Función para reiniciar el juego tras la colisión
def reiniciar_juego():
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo, bala_vertical_disparada, retrocediendo

    # Detener la música al perder
    pygame.mixer.music.stop()

    menu_activo = True  # Activar de nuevo el menú
    jugador.x, jugador.y = 50, h - 100  # Reiniciar posición del jugador
    bala.x = w - 50  # Reiniciar posición de la bala
    nave.x, nave.y = w - 100, h - 100  # Reiniciar posición de la nave
    bala_disparada = False
    bala_vertical_disparada = False  # Reiniciar la bala vertical
    retrocediendo = False
    salto = False
    en_suelo = True
    # Mostrar los datos recopilados hasta el momento
    print("Datos recopilados para el modelo: ", datos_modelo)
    mostrar_menu()  # Mostrar el menú de nuevo para seleccionar modo

def main():
    global salto, en_suelo, bala_disparada, jugador, retrocediendo, tiempo_movimiento

    reloj = pygame.time.Clock()
    mostrar_menu()  # Mostrar el menú al inicio
    correr = True
    
    # Temporizador para la bala vertical
    tiempo_inicio_juego = pygame.time.get_ticks()
    retraso_bala_vertical = 5000  # 5 segundos de retraso

    while correr:
        tiempo_actual = pygame.time.get_ticks()
        accion = 0  # Acción por defecto: nada
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa:  # Detectar la tecla espacio para saltar
                    salto = True
                    en_suelo = False
                    accion = 1  # Acción: salto
                if evento.key == pygame.K_LEFT and not pausa :  # Mover izquierda
                    if jugador.x > pos_x_min:
                        jugador.x -= velocidad_x
                        accion = 2  # Acción: izquierda
                        retrocediendo = True
                        tiempo_movimiento = tiempo_actual
                if evento.key == pygame.K_RIGHT and not pausa :  # Mover derecha
                    if jugador.x < pos_x_max:
                        jugador.x += velocidad_x
                        accion = 3  # Acción: derecha
                        retrocediendo = True
                        tiempo_movimiento = tiempo_actual
                if evento.key == pygame.K_p:  # Presiona 'p' para pausar el juego
                    pausa_juego()
                if evento.key == pygame.K_q:  # Presiona 'q' para terminar el juego
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

        if not pausa:
            # Modo manual: el jugador controla el salto
            if not modo_auto:
                if salto:
                    manejar_salto()
                # Guardar los datos si estamos en modo manual
                guardar_datos(accion)

            # Actualizar el juego
            if not bala_disparada:
                disparar_bala()
                
            # Añadir retraso a la bala vertical
            permitir_bala_vertical = tiempo_actual - tiempo_inicio_juego > retraso_bala_vertical
            update(permitir_bala_vertical)

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(30)  # Limitar el juego a 30 FPS

    pygame.quit()

    # Detener la música al salir del juego
    pygame.mixer.music.stop()

if __name__ == "__main__":
    main()