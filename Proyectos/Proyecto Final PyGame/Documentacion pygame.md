# Cambios en el codigo base 
En este caso el código ha sido modificado para incluir nuevas funcionalidades relacionadas con el modo automático, el entrenamiento de un modelo de red neuronal y la predicción de acciones para generar le modo automatico apartir de un entrenamiento en el modo manual.

- Como primer punto podemos hablar de la parte del entrenamiento del modelo en el que se agrego la funcion entrenar_modelo, que utiliza una red neuronal convolucional para ser entrenada y poder usar los datos recopilados en el modo manual, esto permite que usando la red neuronal el juego prediga automaticamente cuando debe saltar.

```Python 
def entrenar_modelo():
    """
    Entrena una red neuronal convolucional con los datos recopilados en modo manual.
    """
    global modelo, entrenado, datos_modelo

    if len(datos_modelo) < 10:  # Asegurarse de tener suficientes datos
        print("No hay suficientes datos para entrenar el modelo.")
        return

    # Preparar los datos
    datos = np.array(datos_modelo)
    X = datos[:, :2]  # Velocidad de la bala y distancia
    y = datos[:, 2]   # Acción (salto o no salto)

    # Expandir dimensiones para usar Conv1D
    X = np.expand_dims(X, axis=-1)

    # Crear el modelo
    modelo = Sequential([
        Conv1D(16, kernel_size=2, activation='relu', input_shape=(2, 1)),
        Flatten(),
        Dense(8, activation='relu'),
        Dense(1, activation='sigmoid')  # Salida binaria (0 o 1)
    ])
    modelo.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

    # Entrenar el modelo
    modelo.fit(X, y, epochs=50, batch_size=4, verbose=1)
    entrenado = True
    print("Modelo entrenado exitosamente.")
```
- Este punto en general lo que hace es crear y entrenar un modelo de red neuronal convolucional con los datos recopilados en el modo manual.

- Como segundo paso se añadio la funcion predecir_accion que utiliza el modelo entrenado para predecir si el jugador debe saltar en modo automatico.

```Python
def predecir_accion(velocidad, distancia):
    """
    Usa el modelo entrenado para predecir si el jugador debe saltar.
    """
    global modelo, entrenado

    if not entrenado:
        print("El modelo no está entrenado.")
        return 0  # No saltar por defecto

    # Preparar los datos de entrada
    entrada = np.array([[velocidad, distancia]])
    entrada = np.expand_dims(entrada, axis=-1)  # Expandir dimensiones para Conv1D

    # Hacer la predicción
    prediccion = modelo.predict(entrada)
    print(f"Predicción: {prediccion[0][0]}, Velocidad: {velocidad}, Distancia: {distancia}")  # Depuración
    return 1 if prediccion[0][0] > 0.57 else 0  # Cambiar el umbral a 0.57
```

- Por ultima parte se agrego dentro del bucle principal el modo automatico, con la opcion de poder entrenar el modelo presionando la tecla T.
```Python
def main():
    global salto, en_suelo, bala_disparada, modo_auto

    reloj = pygame.time.Clock()
    mostrar_menu()  # Mostrar el menú al inicio
    correr = True

    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa and not modo_auto:  # Salto manual
                    salto = True
                    en_suelo = False
                if evento.key == pygame.K_p:  # Pausar el juego
                    pausa_juego()
                if evento.key == pygame.K_q:  # Terminar el juego
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()
                if evento.key == pygame.K_t:  # Entrenar el modelo
                    entrenar_modelo()

        if not pausa:
            if modo_auto:  # Modo automático
                distancia = abs(jugador.x - bala.x)
                accion = predecir_accion(velocidad_bala, distancia)
                if accion == 1 and en_suelo:  # Si la predicción es 1 y está en el suelo
                    salto = True
                    en_suelo = False
                if salto:  # Manejar el salto en modo automático
                    manejar_salto()
            else:  # Modo manual
                if salto:
                    manejar_salto()
                guardar_datos()  # Guardar datos en modo manual

            # Actualizar el juego
            if not bala_disparada:
                disparar_bala()
            update()

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(30)  # Limitar el juego a 30 FPS

    pygame.quit()
```

- Como extra se agrego la fucion para entrenar el modelo automaticamente si el jugador pierde en el modo manual, saliendo presionando A a continuacion para ejecutar el modo automatico.


## Aplicacion Cascaron
- En este caso el codigo es un juego basico de pygame en el que el jugador puede controlar a un personake, saltando con la barra espaciadora, el juego es simple y cuenta con un menu inicial, un modo manual y el sistema de perder, por lo que el objetivo de la practica es lograr activar el modo automatico con un entrenamiento de una red neuronal convulucional, de tal forma que el entrenamiento sea hecho por el modo manual y despues se pueda ejecutar el modo automatico.

- El cascaron del proyecto contaba con lo siguiente: 
  
#### Configuración inicial
Este bloque configura el entorno de Pygame, define las dimensiones de la pantalla, los colores y las variables globales necesarias para el juego.

```Python 
import pygame
import random

# Inicializar Pygame
pygame.init()

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
```

#### Variables del juego
En esta parte se definen variables para manejar el salto, la pausa, el menú, y el modo de juego (manual o automático).

```Python 
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

# Cargar las imágenes
jugador_frames = [
    pygame.image.load('assets/sprites/mono_frame_1.png'),
    pygame.image.load('assets/sprites/mono_frame_2.png'),
    pygame.image.load('assets/sprites/mono_frame_3.png'),
    pygame.image.load('assets/sprites/mono_frame_4.png')
]

bala_img = pygame.image.load('assets/sprites/purple_ball.png')
fondo_img = pygame.image.load('assets/game/fondo2.png')
nave_img = pygame.image.load('assets/game/ufo.png')
menu_img = pygame.image.load('assets/game/menu.png')

# Escalar la imagen de fondo para que coincida con el tamaño de la pantalla
fondo_img = pygame.transform.scale(fondo_img, (w, h))
```

#### Funciones principales
Aqui hay diferentes funciones pero las que mas destacan son las siguiente: 

-  Disparo de la bala
Esta función inicia el disparo de la bala con una velocidad aleatoria.

```Python 
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-8, -3)  # Velocidad aleatoria negativa para la bala
        bala_disparada = True
```

-  Manejo del salto
Controla el movimiento del jugador hacia arriba y aplica la gravedad para que vuelva al suelo.

```Python 
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
```

- Actualización del juego
Actualiza el fondo, la posición de la bala, la animación del jugador y detecta colisiones.

```Python 
def update():
    global bala, velocidad_bala, current_frame, frame_count, fondo_x1, fondo_x2

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

    # Mover y dibujar la bala
    if bala_disparada:
        bala.x += velocidad_bala

    # Si la bala sale de la pantalla, reiniciar su posición
    if bala.x < 0:
        reset_bala()

    pantalla.blit(bala_img, (bala.x, bala.y))

    # Colisión entre la bala y el jugador
    if jugador.colliderect(bala):
        print("Colisión detectada!")
        reiniciar_juego()  # Terminar el juego y mostrar el menú
```

#### Menú y reinicio
El menú permite al jugador seleccionar entre modo automático o manual, y reiniciar el juego tras una colisión.

```Python 
def mostrar_menu():
    global menu_activo, modo_auto
    pantalla.fill(NEGRO)
    texto = fuente.render("Presiona 'A' para Auto, 'M' para Manual, o 'Q' para Salir", True, BLANCO)
    pantalla.blit(texto, (w // 4, h // 2))
    pygame.display.flip()

    while menu_activo:
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
                elif evento.key == pygame.K_q:
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()
```

#### Bucle principal
El bucle principal controla el flujo del juego, maneja eventos de teclado y actualiza el estado del juego.
```Python 
def main():
    global salto, en_suelo, bala_disparada

    reloj = pygame.time.Clock()
    mostrar_menu()  # Mostrar el menú al inicio
    correr = True

    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa:  # Detectar la tecla espacio para saltar
                    salto = True
                    en_suelo = False
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
                guardar_datos()

            # Actualizar el juego
            if not bala_disparada:
                disparar_bala()
            update()

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(30)  # Limitar el juego a 30 FPS

    pygame.quit()
```

# Errores dentro del codigo y su ejecucion que eh encontrado 
- Dentro del codigo los assets no se cargaban de manera correcta, lo que causaba que el codigo no se pudiera ejecutar de manera correcta, por lo que opte por ejecutar el codigo de manera directa, lo que evito los errores de los assets.

# Problematicas a resolver 