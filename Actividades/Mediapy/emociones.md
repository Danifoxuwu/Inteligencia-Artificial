# Detección de Emociones y Verificación de Vida con MediaPipe
- Para poder modelar y detectar emociones faciales para saber si un sugeto esta con vida y no es una fotografia se necesitan analizar los fotogramas, cambios de luz y los "Haar cascades" para lograr este objetivo 
  
  # 1. Detección de Emociones
   ### Puntos faciales importantes para la deteccion
  - Los puntos faciales más relevantes para detectar emociones se encuentran en las siguientes áreas:

    - Ojos: Puntos alrededor de los ojos para medir apertura, simetría y distancias.
    - Cejas: Puntos en los bordes y centro de las cejas para medir inclinación y separación.
    - Boca: Puntos en las esquinas y centro de los labios para medir - apertura, simetría y ángulos.
    - Nariz: Puntos en el puente y base de la nariz para medir proporciones faciales.
    - Mandíbula: Puntos en el contorno de la cara para medir apertura de la mandíbula.
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