import pygame
import random
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

# Esta función entrena una red neuronal para predecir cuándo saltar
def entrenar_modelo(datos_modelo):
    if len(datos_modelo) < 10:
        print("Insuficientes datos para entrenar el modelo.")
        return None
    datos = np.array(datos_modelo)
    X = datos[:, :6]
    y = datos[:, 6]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = Sequential([
        Dense(32, input_dim=6, activation='relu'),
        Dense(32, activation='relu'),
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    modelo.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    modelo.fit(X_train, y_train, epochs=100, batch_size=32, verbose=1)
    loss, accuracy = modelo.evaluate(X_test, y_test, verbose=0)
    print(f"Modelo entrenado con precisión: {accuracy:.2f}")
    return modelo

# Esta función decide si el jugador debe saltar según la predicción de la red
def decidir_salto(jugador, bala, velocidad_bala, bala_aire, bala_disparada_aire, modelo_entrenado, salto, en_suelo):
    if modelo_entrenado is None:
        print("Modelo no entrenado. No se puede decidir.")
        return False, en_suelo
    distancia_suelo = abs(jugador.x - bala.x)
    distancia_aire_x = abs(jugador.centerx - bala_aire.centerx)
    distancia_aire_y = abs(jugador.centery - bala_aire.centery)
    hay_bala_aire = 1 if bala_disparada_aire else 0
    entrada = np.array([[velocidad_bala, distancia_suelo, distancia_aire_x, distancia_aire_y, hay_bala_aire, jugador.x]])
    prediccion = modelo_entrenado.predict(entrada, verbose=0)[0][0]
    if prediccion > 0.5 and en_suelo:
        salto = True
        en_suelo = False
        print("Saltar")
    return salto, en_suelo

# Esta función entrena una red neuronal para el movimiento lateral del jugador
def entrenar_red_movimiento(datos_movimiento):
    if len(datos_movimiento) < 10:
        print("No hay suficientes datos para entrenar.")
        return None
    datos = np.array(datos_movimiento)
    X = datos[:, :8].astype('float32')
    y = datos[:, 8].astype('int')
    y_categorical = to_categorical(y, num_classes=3)
    X_train, X_test, y_train, y_test = train_test_split(X, y_categorical, test_size=0.2, random_state=42)
    model = Sequential([
        Dense(64, input_dim=8, activation='relu'),
        Dense(32, activation='relu'),
        Dense(3, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=1)
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Precisión del modelo de movimiento: {accuracy:.2f}")
    return model

# Esta función decide el movimiento lateral del jugador (izquierda, quieto, derecha)
def decidir_movimiento(jugador, bala, modelo_movimiento, salto, bala_suelo):
    if modelo_movimiento is None:
        print("Modelo no entrenado.")
        return jugador.x, 1
    distancia_bala_suelo = abs(jugador.x - bala_suelo.x)
    entrada = np.array([[
        jugador.x,
        jugador.y,
        bala.centerx,
        bala.centery,
        bala_suelo.x,
        bala_suelo.y,
        distancia_bala_suelo,
        1 if salto else 0
    ]], dtype='float32')
    prediccion = modelo_movimiento.predict(entrada, verbose=0)[0]
    accion = np.argmax(prediccion)
    if accion == 0 and jugador.x > 0:
        jugador.x -= 5
        print("Izquierda")
    elif accion == 2 and jugador.x < 200 - jugador.width:
        jugador.x += 5
        print("Derecha")
    else:
        print("Quieto")
    return jugador.x, accion

# Inicializa pygame y la ventana principal
pygame.init()
base_path = os.path.dirname(os.path.abspath(__file__))
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego: Disparo de Bala_suelo, Bala_aire, Salto, bowser y Menú")
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
jugador = None
bala_suelo = None
bala_aire = None
fondo = None
bowser = None
menu = None
salto = False
salto_altura = 15
gravedad = 1
en_suelo = True
subiendo = True
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False
datos_modelo = []
modelo_entrenado = None
datos_movimiento = []
modelo_entrenado_movimiento = []
intervalo_decidir_salto = 1
contador_decidir_salto = 0

# Carga los sprites del jugador, balas y enemigos
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
nave_frames = [
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/enemigo1.png')), (80, 80)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/enemigo2.png')), (80, 80)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/enemigo3.png')), (80, 80)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/enemigo4.png')), (80, 80)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/enemigo5.png')), (80, 80)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/enemigo6.png')), (80, 80))
]
fondo_img = pygame.image.load(os.path.join(base_path, 'assets 2/Radish Ruins 1.png'))
fondo_img = pygame.transform.scale(fondo_img, (w, h))
jugador = pygame.Rect(50, h - 100, 32, 48)
bala_suelo = pygame.Rect(w - 50, h - 90, 16, 16)
bala_aire = pygame.Rect(0, -50, 16, 16)
bowser = pygame.Rect(w - 100, h - 130, 64, 64)
shyguy = pygame.Rect(0, 0, 64, 64)
zigzag_direccion = 1
zigzag_velocidad = 5
shyguy_disparo_cooldown = 0
shyguy_disparo_intervalo = 60
velocidad_bala_aire = [0, 5]
menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)
current_frame = 0
frame_speed = 10
frame_count = 0
velocidad_bala_suelo = -10
bala_disparada_suelo = False
bala_disparada_aire = False
fondo_x1 = 0
fondo_x2 = w
ultimo_disparo_aire = 0

# Controla el movimiento en zigzag del enemigo shyguy y su cooldown de disparo
def mover_shyguy():
    global shyguy, zigzag_direccion, shyguy_disparo_cooldown
    shyguy.x += zigzag_direccion * zigzag_velocidad
    shyguy_disparo_cooldown -= 1
    if shyguy.x <= 0 or shyguy.x >= 200 - shyguy.width:
        zigzag_direccion *= -1

# Dispara una bala aérea desde la posición del enemigo shyguy
def disparar_bala_aire():
    global bala_aire, bala_disparada_aire, velocidad_bala_aire, ultimo_disparo_aire, shyguy_disparo_cooldown
    if not bala_disparada_aire and shyguy_disparo_cooldown <= 0 and 0 <= shyguy.x <= w:
        bala_aire.x = shyguy.x + shyguy.width // 2 - bala_aire.width // 2
        bala_aire.y = shyguy.y + shyguy.height
        velocidad_bala_aire[0] = 0
        velocidad_bala_aire[1] = 5
        bala_disparada_aire = True
        shyguy_disparo_cooldown = shyguy_disparo_intervalo
        ultimo_disparo_aire = pygame.time.get_ticks()

# Dispara una bala por el suelo desde la derecha de la pantalla
def disparar_bala():
    global bala_disparada_suelo, velocidad_bala_suelo
    if not bala_disparada_suelo:
        velocidad_bala_suelo = random.randint(-8, -3)
        bala_disparada_suelo = True

# Controla el movimiento del jugador con las teclas y calcula la posición relativa a la bala aérea
def mover_jugador():
    global jugador, en_suelo, salto, pos_actual
    keys = pygame.key.get_pressed()
    pos_actual = 1
    if keys[pygame.K_LEFT] and jugador.x > 0:
        jugador.x -= 5
        pos_actual = 0
    if keys[pygame.K_RIGHT] and jugador.x < 200 - jugador.width:
        jugador.x += 5
        pos_actual = 2
    if keys[pygame.K_UP] and en_suelo:
        salto = True
        en_suelo = False
    distancia_x = (jugador.centerx - bala_aire.centerx)
    distancia_y = (jugador.centery - bala_aire.centery)
    distancia_total = (distancia_x**2 + distancia_y**2) ** 0.5
    print(f"Posicion Actual : {jugador.x} |  Posicion de la bala {bala_aire.centerx} | Distancia horizontal aire(x): {distancia_x} | Distancia vertical aire(y): {distancia_y} | Velocidad Bala Aire: {velocidad_bala_aire} ", end="\r")

# Guarda los datos de movimiento para entrenamiento y análisis
def mover_jugador_automatico(modelo_movimiento):
    global jugador, pos_actual
    jugador.x, pos_actual = decidir_movimiento(jugador, bala_aire, modelo_movimiento, salto)
    distancia_x = jugador.centerx - bala_aire.centerx
    distancia_y = jugador.centery - bala_aire.centery
    datos_movimiento.append((distancia_x, distancia_y, jugador.x, bala_aire.centerx, pos_actual))

# Reinicia la bala del suelo a la posición inicial
def reset_bala():
    global bala_suelo, bala_disparada_suelo
    bala_suelo.x = w - 50
    bala_disparada_suelo = False

# Reinicia la bala aérea a la posición inicial
def reset_bala_aire():
    global bala_aire, bala_disparada_aire
    bala_aire.y = -50
    bala_disparada_aire = False

# Controla la física del salto del jugador
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo, subiendo
    if salto:
        if subiendo:
            jugador.y -= salto_altura
            salto_altura -= gravedad
            if salto_altura <= 0:
                subiendo = False
        else:
            jugador.y += salto_altura
            salto_altura += gravedad
            if jugador.y >= h - 100:
                jugador.y = h - 100
                salto = False
                salto_altura = 15
                subiendo = True
                en_suelo = True

# Actualiza la pantalla, mueve los elementos y detecta colisiones
def update():
    global bala_suelo, bala_aire, current_frame, frame_count, fondo_x1, fondo_x2
    mover_shyguy()
    fondo_x1 -= 3
    fondo_x2 -= 3
    if fondo_x1 <= -w:
        fondo_x1 = w
    if fondo_x2 <= -w:
        fondo_x2 = w
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))
    if salto:
        if subiendo:
            pantalla.blit(jugador_frames[0], (jugador.x, jugador.y))
        else:
            pantalla.blit(jugador_frames[1], (jugador.x, jugador.y))
    else:
        frame_count += 10
        if frame_count >= frame_speed:
            current_frame = (current_frame + 1) % len(jugador_frames)
            frame_count = 0
        pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))
    pantalla.blit(nave_frames[current_frame % len(nave_frames)], (bowser.x, bowser.y))
    pantalla.blit(nave_frames[current_frame % len(nave_frames)], (shyguy.x, shyguy.y+75))
    if bala_disparada_suelo:
        bala_suelo.x += velocidad_bala_suelo
        pantalla.blit(bala_frames[current_frame % len(bala_frames)], (bala_suelo.x, bala_suelo.y))
    if bala_disparada_aire:
        bala_aire.x += velocidad_bala_aire[0]
        bala_aire.y += velocidad_bala_aire[1]
        pantalla.blit(bala_frames[current_frame % len(bala_frames)], (bala_aire.x, bala_aire.y))
    if bala_suelo.x < 0:
        reset_bala()
    if bala_aire.y > h or bala_aire.x < 0 or bala_aire.x > w:
        reset_bala_aire()
    if jugador.colliderect(bala_suelo) or jugador.colliderect(bala_aire):
        print("Colisión detectada!")
        reiniciar_juego()

# Guarda los datos de cada frame para entrenamiento y análisis
def guardar_datos():
    global jugador, bala_suelo, velocidad_bala_suelo, salto
    distancia_suelo = abs(jugador.x - bala_suelo.x)
    salto_hecho = 1 if salto else 0
    distancia_aire_x = abs(jugador.centerx - bala_aire.centerx)
    distancia_aire_y = abs(jugador.centery - bala_aire.centery)
    hay_bala_aire = 1 if bala_disparada_aire else 0
    datos_modelo.append((
        velocidad_bala_suelo,
        distancia_suelo,
        distancia_aire_x,
        distancia_aire_y,
        hay_bala_aire,
        jugador.x,
        salto_hecho
    ))
    distancia_bala_suelo = abs(jugador.x - bala_suelo.x)
    datos_movimiento.append((
        jugador.x,
        jugador.y,
        bala_aire.centerx,
        bala_aire.centery,
        bala_suelo.x,
        bala_suelo.y,
        distancia_bala_suelo,
        1 if salto else 0,
        pos_actual
    ))

# Pausa el juego y muestra los datos recolectados
def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        imprimir_datos()
    else:
        print("Juego reanudado.")

# Dibuja un botón rectangular con texto centrado
def draw_button(rect, text, color, text_color=NEGRO):
    pygame.draw.rect(pantalla, color, rect)
    pygame.draw.rect(pantalla, NEGRO, rect, 2)
    texto = fuente.render(text, True, text_color)
    text_rect = texto.get_rect(center=rect.center)
    pantalla.blit(texto, text_rect)

# Menú principal con botones para modo manual, automático, entrenamiento y salir
def mostrar_menu():
    global menu_activo, modo_auto, datos_modelo, modelo_entrenado, modelo_entrenado_movimiento
    pantalla.fill(NEGRO)
    btn_manual = pygame.Rect(w // 2 - 120, h // 2 - 70, 240, 40)
    btn_auto = pygame.Rect(w // 2 - 120, h // 2 - 20, 240, 40)
    btn_train = pygame.Rect(w // 2 - 120, h // 2 + 30, 240, 40)
    btn_salir = pygame.Rect(w // 2 - 120, h // 2 + 80, 240, 40)
    while menu_activo:
        pantalla.fill(NEGRO)
        draw_button(btn_manual, "Modo Manual", (200, 200, 255))
        draw_button(btn_auto, "Modo Automático", (200, 255, 200))
        draw_button(btn_train, "Entrenar Automático", (255, 255, 200))
        draw_button(btn_salir, "Salir", (255, 200, 200))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    modo_auto = True
                    menu_activo = False
                elif evento.key == pygame.K_m:
                    modo_auto = False
                    menu_activo = False
                elif evento.key == pygame.K_t:
                    modelo_entrenado = entrenar_modelo(datos_modelo)
                    modelo_entrenado_movimiento = entrenar_red_movimiento(datos_movimiento)
                elif evento.key == pygame.K_q:
                    imprimir_datos()
                    pygame.quit()
                    exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_pos = evento.pos
                if btn_manual.collidepoint(mouse_pos):
                    modo_auto = False
                    menu_activo = False
                elif btn_auto.collidepoint(mouse_pos):
                    modo_auto = True
                    menu_activo = False
                elif btn_train.collidepoint(mouse_pos):
                    modelo_entrenado = entrenar_modelo(datos_modelo)
                    modelo_entrenado_movimiento = entrenar_red_movimiento(datos_movimiento)
                elif btn_salir.collidepoint(mouse_pos):
                    imprimir_datos()
                    pygame.quit()
                    exit()

# Reinicia el estado del juego y muestra el menú
def reiniciar_juego():
    global menu_activo, jugador, bala_suelo, bala_aire, bowser, bala_disparada_suelo, bala_disparada_aire, salto, en_suelo
    menu_activo = True
    jugador.x, jugador.y = 50, h - 100
    bala_suelo.x = w - 50
    bala_aire.y = -50
    bowser.x, bowser.y = w - 100, h - 100
    bala_disparada_suelo = False
    bala_disparada_aire = False
    salto = False
    en_suelo = True
    imprimir_datos()
    mostrar_menu()

# Imprime los datos de movimiento recolectados
def imprimir_datos():
    for dato in datos_movimiento:
        print(dato)

# Bucle principal del juego
def main():
    global salto, en_suelo, bala_disparada_suelo, bala_disparada_aire, contador_decidir_salto
    reloj = pygame.time.Clock()
    mostrar_menu()
    correr = True
    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa:
                    salto = True
                    en_suelo = False
                if evento.key == pygame.K_p:
                    pausa_juego()
                if evento.key == pygame.K_q:
                    imprimir_datos()
                    pygame.quit()
                    exit()
        if not pausa:
            if not modo_auto:
                mover_jugador()
                if salto:
                    manejar_salto()
                guardar_datos()
            if modo_auto:
                if contador_decidir_salto >= intervalo_decidir_salto:
                    salto, en_suelo = decidir_salto(jugador, bala_suelo, velocidad_bala_suelo, bala_aire, bala_disparada_aire, modelo_entrenado, salto, en_suelo)
                    contador_decidir_salto = 0
                else:
                    contador_decidir_salto += 1
                if salto:
                    manejar_salto()
                jugador.x, pos_actual = decidir_movimiento(jugador, bala_aire, modelo_entrenado_movimiento, salto, bala_suelo)
            if not bala_disparada_suelo:
                disparar_bala()
            disparar_bala_aire()
            update()
        pygame.display.flip()
        reloj.tick(30)
    pygame.quit()

if __name__ == "__main__":
    main()