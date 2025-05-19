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
def entrenar_modelo_kirby(datos_kirby):
    if len(datos_kirby) < 10:
        print(f"[INFO] Insuficientes datos para entrenar el modelo de Kirby. Datos actuales: {len(datos_kirby)}")
        return None
    datos = np.array(datos_kirby)
    X = datos[:, :6]
    y = datos[:, 6]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo_kirby = Sequential([
        Dense(32, input_dim=6, activation='relu'),
        Dense(32, activation='relu'),
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    modelo_kirby.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    modelo_kirby.fit(X_train, y_train, epochs=100, batch_size=32, verbose=1)
    loss, accuracy = modelo_kirby.evaluate(X_test, y_test, verbose=0)
    print(f"[INFO] Modelo de Kirby entrenado con precisión: {accuracy:.4f} (loss: {loss:.4f}, muestras de test: {len(y_test)})")
    return modelo_kirby

# Esta función decide si Kirby debe saltar según la predicción de la red
def decidir_salto_kirby(kirby, proyectil_suelo, velocidad_proyectil, proyectil_aire, proyectil_aire_disparado, modelo_kirby, saltando, en_suelo):
    if modelo_kirby is None:
        print("[WARN] Modelo de Kirby no entrenado. No se puede decidir salto.")
        return False, en_suelo
    distancia_suelo = abs(kirby.x - proyectil_suelo.x)
    distancia_aire_x = abs(kirby.centerx - proyectil_aire.centerx)
    distancia_aire_y = abs(kirby.centery - proyectil_aire.centery)
    hay_proyectil_aire = 1 if proyectil_aire_disparado else 0
    entrada_kirby = np.array([[velocidad_proyectil, distancia_suelo, distancia_aire_x, distancia_aire_y, hay_proyectil_aire, kirby.x]])
    prediccion_kirby = modelo_kirby.predict(entrada_kirby, verbose=0)[0][0]
    print(f"[INFO] Decisión de salto: predicción={prediccion_kirby:.4f}, en_suelo={en_suelo}, salto_actual={saltando}, entrada={entrada_kirby.tolist()}")
    if prediccion_kirby > 0.5 and en_suelo:
        saltando = True
        en_suelo = False
        print(f"[ACTION] Kirby salta (predicción={prediccion_kirby:.4f}, distancia_suelo={distancia_suelo}, distancia_aire_x={distancia_aire_x}, distancia_aire_y={distancia_aire_y})")
    return saltando, en_suelo

# Esta función entrena una red neuronal para el movimiento lateral de Kirby
def entrenar_movimiento_kirby(datos_movimiento_kirby):
    if len(datos_movimiento_kirby) < 10:
        print(f"[INFO] No hay suficientes datos para entrenar el movimiento de Kirby. Datos actuales: {len(datos_movimiento_kirby)}")
        return None
    datos = np.array(datos_movimiento_kirby)
    X = datos[:, :8].astype('float32')
    y = datos[:, 8].astype('int')
    y_categorical = to_categorical(y, num_classes=3)
    X_train, X_test, y_train, y_test = train_test_split(X, y_categorical, test_size=0.2, random_state=42)
    modelo_movimiento_kirby = Sequential([
        Dense(64, input_dim=8, activation='relu'),
        Dense(32, activation='relu'),
        Dense(3, activation='softmax')
    ])
    modelo_movimiento_kirby.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    modelo_movimiento_kirby.fit(X_train, y_train, epochs=100, batch_size=32, verbose=1)
    loss, accuracy = modelo_movimiento_kirby.evaluate(X_test, y_test, verbose=0)
    print(f"[INFO] Precisión del modelo de movimiento de Kirby: {accuracy:.4f} (loss: {loss:.4f}, muestras de test: {len(y_test)})")
    return modelo_movimiento_kirby

# Esta función decide el movimiento lateral de Kirby (izquierda, quieto, derecha)
def decidir_movimiento_kirby(kirby, proyectil_aire, modelo_movimiento_kirby, saltando, proyectil_suelo):
    if modelo_movimiento_kirby is None:
        print("[WARN] Modelo de movimiento de Kirby no entrenado.")
        return kirby.x, 1
    distancia_proyectil_suelo = abs(kirby.x - proyectil_suelo.x)
    entrada_movimiento = np.array([[
        kirby.x,
        kirby.y,
        proyectil_aire.centerx,
        proyectil_aire.centery,
        proyectil_suelo.x,
        proyectil_suelo.y,
        distancia_proyectil_suelo,
        1 if saltando else 0
    ]], dtype='float32')
    prediccion_movimiento = modelo_movimiento_kirby.predict(entrada_movimiento, verbose=0)[0]
    accion_kirby = np.argmax(prediccion_movimiento)
    print(f"[INFO] Decisión movimiento: predicción={prediccion_movimiento}, acción={accion_kirby}, entrada={entrada_movimiento.tolist()}")
    if accion_kirby == 0 and kirby.x > 0:
        kirby.x -= 5
        print(f"[ACTION] Kirby se mueve a la izquierda (x={kirby.x})")
    elif accion_kirby == 2 and kirby.x < 200 - kirby.width:
        kirby.x += 5
        print(f"[ACTION] Kirby se mueve a la derecha (x={kirby.x})")
    else:
        print(f"[ACTION] Kirby se queda quieto (x={kirby.x})")
    return kirby.x, accion_kirby

# Inicializa pygame y la ventana principal
pygame.init()
base_path = os.path.dirname(os.path.abspath(__file__))
w, h = 800, 400
pantalla_kirby = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego de Kirby: Esquivar proyectiles")
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
kirby = None
proyectil_suelo = None
proyectil_aire = None
fondo_kirby = None
enemigo_kirby = None
menu_kirby = None
saltando = False
altura_salto_kirby = 15
gravedad_kirby = 1
en_suelo_kirby = True
subiendo_salto = True
pausa_kirby = False
fuente_kirby = pygame.font.SysFont('Arial', 24)
menu_activo_kirby = True
modo_auto_kirby = False
datos_kirby = []
modelo_kirby_entrenado = None
datos_movimiento_kirby = []
modelo_movimiento_kirby_entrenado = []
intervalo_decidir_salto_kirby = 1
contador_salto_kirby = 0

# Carga los sprites de Kirby, proyectiles y enemigos
kirby_frames = [
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
proyectil_frames = [
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/apple1.png')), (40, 40)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/apple2.png')), (40, 40)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/apple3.png')), (40, 40)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/apple4.png')), (40, 40)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/apple5.png')), (40, 40)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/apple6.png')), (40, 40))
]
enemigo_frames = [
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/enemigo1.png')), (80, 80)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/enemigo2.png')), (80, 80)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/enemigo3.png')), (80, 80)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/enemigo4.png')), (80, 80)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/enemigo5.png')), (80, 80)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets 2/enemigo6.png')), (80, 80))
]

fondo_kirby_img = pygame.image.load(os.path.join(base_path, 'assets 2/Radish Ruins 1.png'))
fondo_kirby_img = pygame.transform.scale(fondo_kirby_img, (w, h))
kirby = pygame.Rect(50, h - 100, 32, 48)
proyectil_suelo = pygame.Rect(w - 50, h - 90, 16, 16)
proyectil_aire = pygame.Rect(0, -50, 16, 16)
enemigo_kirby = pygame.Rect(w - 100, h - 130, 64, 64)
enemigo_volador = pygame.Rect(0, 0, 64, 64)
direccion_enemigo = 1
velocidad_enemigo = 5
cooldown_disparo = 0
intervalo_disparo = 60
velocidad_proyectil_aire = [0, 5]
menu_rect_kirby = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)
frame_actual_kirby = 0
velocidad_animacion = 10
contador_frames = 0
velocidad_proyectil_suelo = -10
proyectil_suelo_disparado = False
proyectil_aire_disparado = False
fondo_x1_kirby = 0
fondo_x2_kirby = w
ultimo_disparo_aire = 0

# Controla el movimiento en zigzag del enemigo volador y su cooldown de disparo
def mover_enemigo_volador():
    global enemigo_volador, direccion_enemigo, cooldown_disparo
    enemigo_volador.x += direccion_enemigo * velocidad_enemigo
    cooldown_disparo -= 1
    if enemigo_volador.x <= 0 or enemigo_volador.x >= 200 - enemigo_volador.width:
        direccion_enemigo *= -1

# Dispara un proyectil aéreo desde la posición del enemigo volador
def disparar_proyectil_aire():
    global proyectil_aire, proyectil_aire_disparado, velocidad_proyectil_aire, ultimo_disparo_aire, cooldown_disparo
    if not proyectil_aire_disparado and cooldown_disparo <= 0 and 0 <= enemigo_volador.x <= w:
        proyectil_aire.x = enemigo_volador.x + enemigo_volador.width // 2 - proyectil_aire.width // 2
        proyectil_aire.y = enemigo_volador.y + enemigo_volador.height
        velocidad_proyectil_aire[0] = 0
        velocidad_proyectil_aire[1] = 5
        proyectil_aire_disparado = True
        cooldown_disparo = intervalo_disparo
        ultimo_disparo_aire = pygame.time.get_ticks()

# Dispara un proyectil por el suelo desde la derecha de la pantalla
def disparar_proyectil_suelo():
    global proyectil_suelo_disparado, velocidad_proyectil_suelo
    if not proyectil_suelo_disparado:
        velocidad_proyectil_suelo = random.randint(-8, -3)
        proyectil_suelo_disparado = True

# Controla el movimiento de Kirby con las teclas y calcula la posición relativa al proyectil aéreo
def mover_kirby_manual():
    global kirby, en_suelo_kirby, saltando, pos_actual_kirby
    keys = pygame.key.get_pressed()
    pos_actual_kirby = 1
    if keys[pygame.K_LEFT] and kirby.x > 0:
        kirby.x -= 5
        pos_actual_kirby = 0
    if keys[pygame.K_RIGHT] and kirby.x < 200 - kirby.width:
        kirby.x += 5
        pos_actual_kirby = 2
    if keys[pygame.K_UP] and en_suelo_kirby:
        saltando = True
        en_suelo_kirby = False
    distancia_x = (kirby.centerx - proyectil_aire.centerx)
    distancia_y = (kirby.centery - proyectil_aire.centery)
    distancia_total = (distancia_x**2 + distancia_y**2) ** 0.5
    print(f"[INFO] Kirby(x={kirby.x}, y={kirby.y}) | ProyectilAire(x={proyectil_aire.centerx}, y={proyectil_aire.centery}) | DistanciaX={distancia_x} | DistanciaY={distancia_y} | DistanciaTotal={distancia_total:.2f} | VelocidadProyectilAire={velocidad_proyectil_aire} | Saltando={saltando} | EnSuelo={en_suelo_kirby}", end="\r")

# Guarda los datos de movimiento para entrenamiento y análisis
def mover_kirby_automatico(modelo_movimiento_kirby):
    global kirby, pos_actual_kirby
    kirby.x, pos_actual_kirby = decidir_movimiento_kirby(kirby, proyectil_aire, modelo_movimiento_kirby, saltando)
    distancia_x = kirby.centerx - proyectil_aire.centerx
    distancia_y = kirby.centery - proyectil_aire.centery
    datos_movimiento_kirby.append((distancia_x, distancia_y, kirby.x, proyectil_aire.centerx, pos_actual_kirby))

# Reinicia el proyectil del suelo a la posición inicial
def reset_proyectil_suelo():
    global proyectil_suelo, proyectil_suelo_disparado
    proyectil_suelo.x = w - 50
    proyectil_suelo_disparado = False

# Reinicia el proyectil aéreo a la posición inicial
def reset_proyectil_aire():
    global proyectil_aire, proyectil_aire_disparado
    proyectil_aire.y = -50
    proyectil_aire_disparado = False

# Controla la física del salto de Kirby
def manejar_salto_kirby():
    global kirby, saltando, altura_salto_kirby, gravedad_kirby, en_suelo_kirby, subiendo_salto
    if saltando:
        if subiendo_salto:
            kirby.y -= altura_salto_kirby
            altura_salto_kirby -= gravedad_kirby
            if altura_salto_kirby <= 0:
                subiendo_salto = False
        else:
            kirby.y += altura_salto_kirby
            altura_salto_kirby += gravedad_kirby
            if kirby.y >= h - 100:
                kirby.y = h - 100
                saltando = False
                altura_salto_kirby = 15
                subiendo_salto = True
                en_suelo_kirby = True

# Actualiza la pantalla, mueve los elementos y detecta colisiones
def actualizar_juego_kirby():
    global proyectil_suelo, proyectil_aire, frame_actual_kirby, contador_frames, fondo_x1_kirby, fondo_x2_kirby
    mover_enemigo_volador()
    fondo_x1_kirby -= 3
    fondo_x2_kirby -= 3
    if fondo_x1_kirby <= -w:
        fondo_x1_kirby = w
    if fondo_x2_kirby <= -w:
        fondo_x2_kirby = w
    pantalla_kirby.blit(fondo_kirby_img, (fondo_x1_kirby, 0))
    pantalla_kirby.blit(fondo_kirby_img, (fondo_x2_kirby, 0))
    if saltando:
        if subiendo_salto:
            pantalla_kirby.blit(kirby_frames[0], (kirby.x, kirby.y))
        else:
            pantalla_kirby.blit(kirby_frames[1], (kirby.x, kirby.y))
    else:
        contador_frames += 10
        if contador_frames >= velocidad_animacion:
            frame_actual_kirby = (frame_actual_kirby + 1) % len(kirby_frames)
            contador_frames = 0
        pantalla_kirby.blit(kirby_frames[frame_actual_kirby], (kirby.x, kirby.y))
    pantalla_kirby.blit(enemigo_frames[frame_actual_kirby % len(enemigo_frames)], (enemigo_kirby.x, enemigo_kirby.y))
    if proyectil_suelo_disparado:
        proyectil_suelo.x += velocidad_proyectil_suelo
        pantalla_kirby.blit(proyectil_frames[frame_actual_kirby % len(proyectil_frames)], (proyectil_suelo.x, proyectil_suelo.y))
    if proyectil_aire_disparado:
        proyectil_aire.x += velocidad_proyectil_aire[0]
        proyectil_aire.y += velocidad_proyectil_aire[1]
        pantalla_kirby.blit(proyectil_frames[frame_actual_kirby % len(proyectil_frames)], (proyectil_aire.x, proyectil_aire.y))
    if proyectil_suelo.x < 0:
        reset_proyectil_suelo()
    if proyectil_aire.y > h or proyectil_aire.x < 0 or proyectil_aire.x > w:
        reset_proyectil_aire()
    if kirby.colliderect(proyectil_suelo) or kirby.colliderect(proyectil_aire):
        print(f"[GAME OVER] Kirby golpeado! Posición Kirby: (x={kirby.x}, y={kirby.y}), Proyectil suelo: (x={proyectil_suelo.x}, y={proyectil_suelo.y}), Proyectil aire: (x={proyectil_aire.x}, y={proyectil_aire.y})")
        reiniciar_juego_kirby()

# Guarda los datos de cada frame para entrenamiento y análisis
def guardar_datos_kirby():
    global kirby, proyectil_suelo, velocidad_proyectil_suelo, saltando
    distancia_suelo = abs(kirby.x - proyectil_suelo.x)
    salto_realizado = 1 if saltando else 0
    distancia_aire_x = abs(kirby.centerx - proyectil_aire.centerx)
    distancia_aire_y = abs(kirby.centery - proyectil_aire.centery)
    hay_proyectil_aire = 1 if proyectil_aire_disparado else 0
    datos_kirby.append((
        velocidad_proyectil_suelo,
        distancia_suelo,
        distancia_aire_x,
        distancia_aire_y,
        hay_proyectil_aire,
        kirby.x,
        salto_realizado
    ))
    distancia_proyectil_suelo = abs(kirby.x - proyectil_suelo.x)
    datos_movimiento_kirby.append((
        kirby.x,
        kirby.y,
        proyectil_aire.centerx,
        proyectil_aire.centery,
        proyectil_suelo.x,
        proyectil_suelo.y,
        distancia_proyectil_suelo,
        1 if saltando else 0,
        pos_actual_kirby
    ))

# Pausa el juego y muestra los datos recolectados
def pausar_juego_kirby():
    global pausa_kirby
    pausa_kirby = not pausa_kirby
    if pausa_kirby:
        imprimir_datos_kirby()
    else:
        print("Juego de Kirby reanudado.")

# Dibuja un botón rectangular con texto centrado
def dibujar_boton_kirby(rect, texto, color, color_texto=NEGRO):
    pygame.draw.rect(pantalla_kirby, color, rect)
    pygame.draw.rect(pantalla_kirby, NEGRO, rect, 2)
    texto_kirby = fuente_kirby.render(texto, True, color_texto)
    rect_texto = texto_kirby.get_rect(center=rect.center)
    pantalla_kirby.blit(texto_kirby, rect_texto)

# Menú principal con botones para modo manual, automático, entrenamiento y salir
def mostrar_menu_kirby():
    global menu_activo_kirby, modo_auto_kirby, datos_kirby, modelo_kirby_entrenado, modelo_movimiento_kirby_entrenado
    pantalla_kirby.fill(NEGRO)
    btn_manual_kirby = pygame.Rect(w // 2 - 120, h // 2 - 70, 240, 40)
    btn_auto_kirby = pygame.Rect(w // 2 - 120, h // 2 - 20, 240, 40)
    btn_entrenar_kirby = pygame.Rect(w // 2 - 120, h // 2 + 30, 240, 40)
    btn_salir_kirby = pygame.Rect(w // 2 - 120, h // 2 + 80, 240, 40)
    while menu_activo_kirby:
        pantalla_kirby.fill(NEGRO)
        dibujar_boton_kirby(btn_manual_kirby, "Modo Manual Kirby", (200, 200, 255))
        dibujar_boton_kirby(btn_auto_kirby, "Modo Automático Kirby", (200, 255, 200))
        dibujar_boton_kirby(btn_entrenar_kirby, "Entrenar Kirby", (255, 255, 200))
        dibujar_boton_kirby(btn_salir_kirby, "Salir", (255, 200, 200))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    modo_auto_kirby = True
                    menu_activo_kirby = False
                elif evento.key == pygame.K_m:
                    modo_auto_kirby = False
                    menu_activo_kirby = False
                elif evento.key == pygame.K_t:
                    modelo_kirby_entrenado = entrenar_modelo_kirby(datos_kirby)
                    modelo_movimiento_kirby_entrenado = entrenar_movimiento_kirby(datos_movimiento_kirby)
                elif evento.key == pygame.K_q:
                    imprimir_datos_kirby()
                    pygame.quit()
                    exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_pos = evento.pos
                if btn_manual_kirby.collidepoint(mouse_pos):
                    modo_auto_kirby = False
                    menu_activo_kirby = False
                elif btn_auto_kirby.collidepoint(mouse_pos):
                    modo_auto_kirby = True
                    menu_activo_kirby = False
                elif btn_entrenar_kirby.collidepoint(mouse_pos):
                    modelo_kirby_entrenado = entrenar_modelo_kirby(datos_kirby)
                    modelo_movimiento_kirby_entrenado = entrenar_movimiento_kirby(datos_movimiento_kirby)
                elif btn_salir_kirby.collidepoint(mouse_pos):
                    imprimir_datos_kirby()
                    pygame.quit()
                    exit()

# Reinicia el estado del juego y muestra el menú
def reiniciar_juego_kirby():
    global menu_activo_kirby, kirby, proyectil_suelo, proyectil_aire, enemigo_kirby, proyectil_suelo_disparado, proyectil_aire_disparado, saltando, en_suelo_kirby
    menu_activo_kirby = True
    kirby.x, kirby.y = 50, h - 100
    proyectil_suelo.x = w - 50
    proyectil_aire.y = -50
    enemigo_kirby.x, enemigo_kirby.y = w - 100, h - 100
    proyectil_suelo_disparado = False
    proyectil_aire_disparado = False
    saltando = False
    en_suelo_kirby = True
    imprimir_datos_kirby()
    mostrar_menu_kirby()

# Imprime los datos de movimiento recolectados
def imprimir_datos_kirby():
    print("[DATA] Datos de movimiento recolectados:")
    for i, dato in enumerate(datos_movimiento_kirby):
        print(f"  [{i}] {dato}")

# Bucle principal del juego
def main_kirby():
    global saltando, en_suelo_kirby, proyectil_suelo_disparado, proyectil_aire_disparado, contador_salto_kirby
    reloj_kirby = pygame.time.Clock()
    mostrar_menu_kirby()
    juego_activo = True
    while juego_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                juego_activo = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo_kirby and not pausa_kirby:
                    saltando = True
                    en_suelo_kirby = False
                if evento.key == pygame.K_p:
                    pausar_juego_kirby()
                if evento.key == pygame.K_q:
                    imprimir_datos_kirby()
                    pygame.quit()
                    exit()
        if not pausa_kirby:
            if not modo_auto_kirby:
                mover_kirby_manual()
                if saltando:
                    manejar_salto_kirby()
                guardar_datos_kirby()
            if modo_auto_kirby:
                if contador_salto_kirby >= intervalo_decidir_salto_kirby:
                    saltando, en_suelo_kirby = decidir_salto_kirby(kirby, proyectil_suelo, velocidad_proyectil_suelo, proyectil_aire, proyectil_aire_disparado, modelo_kirby_entrenado, saltando, en_suelo_kirby)
                    contador_salto_kirby = 0
                else:
                    contador_salto_kirby += 1
                if saltando:
                    manejar_salto_kirby()
                kirby.x, pos_actual_kirby = decidir_movimiento_kirby(kirby, proyectil_aire, modelo_movimiento_kirby_entrenado, saltando, proyectil_suelo)
            if not proyectil_suelo_disparado:
                disparar_proyectil_suelo()
            disparar_proyectil_aire()
            actualizar_juego_kirby()
        pygame.display.flip()
        reloj_kirby.tick(30)
    pygame.quit()

if __name__ == "__main__":
    main_kirby()