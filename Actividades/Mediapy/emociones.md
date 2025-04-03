# Detección de Emociones y Verificación de Vida con MediaPipe
- Para poder modelar y detectar emociones faciales para saber si un sugeto esta con vida y no es una fotografia se necesitan analizar los fotogramas, cambios de luz y los "Haar cascades" para lograr este objetivo 
  
  # 1. Detección de Emociones
   ### Puntos faciales importantes para la deteccion
  - Los puntos faciales más relevantes para detectar emociones se encuentran en las siguientes áreas:

    - Ojos: Puntos alrededor de los ojos para medir apertura, simetría y distancias.
    - Cejas: Puntos en los bordes y centro de las cejas para medir inclinación y separación.
    - Boca: Puntos en las esquinas y centro de los labios para medir   apertura, simetría y ángulos.
    - Nariz: Puntos en el puente y base de la nariz para medir proporciones faciales.
    ### Parametros para la deteccion de emociones 
    - Los parametros mas relevantes son: 
        - Distancias:
            Distancia entre los ojos.
            Distancia entre las esquinas de la boca.
            Distancia entre las cejas.
            Distancia entre la nariz y la mandíbula.
        - Ángulos:
            Inclinación de las cejas.
            Inclinación de la boca.
        - Simetría:
            Simetría de la boca (diferencia entre los lados izquierdo y derecho).
            Simetría de las cejas.
        - Proporciones Normalizadas:
            Todas las distancias se normalizan usando la distancia entre los ojos como referencia.

![alt text](image.png)

## Como podriamos entonces realizar las pruebas correspondientes?

 - Como primer paso podriamos calcular las distancias entre los puntos y medir estas distancias en los puntos de interes para saber que tipo de acciones se realizan y apartir de esos calculos poder analizar cuales podrian corresponder a una sonrisa, una cara seria o una cara triste
 - Con lo anterior podriamos agregar la capacidad de detectar emociones, por ejemplo con el uso de los gestos 

- Detecta emociones basadas en medidas faciales:
  - **Feliz**: Si la boca está significativamente abierta.
  - **Triste**: Si los ojos están cerrados (distancia entre párpados es pequeña).
  - **Serio**: Si no se cumplen las condiciones anteriores.

- Como siguiente punto podriamos analizar si el sujeto esta vivo apartir de la visualizacion mediante los siguientes conceptos:
- 
  - **Movimiento**: Calcula la diferencia entre fotogramas consecutivos.
  - **Cambios de luz**: Detecta variaciones en la intensidad de luz en la cara.

En general esto es lo que necesitamos para poder realizar una prueba de deteccion de rostros