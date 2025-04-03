 # Evaluacion de Redes Neuronales Mediapipe

 ### Daniel Avila Vergara 

#### Definir el tipo de red neuronal y describir cada una de sus partes 
- Este caso es un poco curioso ya que podria decirse que el uso de una red neuronal convolucional no es tan apto debido a que no se estan trabajando con imagenes (Pues se estan usando los landmarks de mediapipe), por lo que podriamos optar por el uso de una *Red neuronal Densa* pues esta tiene la capacidad de aprender patrones de los datos, lo cual puede ser ideal para poder usar los valores de las land marks

Cada una de las partes de una red neuronal densa se especificarian de la siguiente manera, ademas de su uso:

- *Entrada*: En esta parte se pueden recibir los datos inciales, que en este caso serian las coordenadas de las landmarks de mediapipe 
  
- *Capas Ocultas:*Aqui se podrian procesar los datos de entrada extrayendo las caracteristicas significativas que van a ayudar a la red a identificar los patrones del rostro para poder relacionarlos con las emociones 
  
- *Capas de salida:* Aqui se podria proporcionar lo que seria la respuesta de la red y su prediccion que en este caso la podriamos entender como la emocion detectada
  
#### Definir los patrones a utilizar 
Como los patrones elegidos tendriamos que utilizar patrones globales apartir de los datos de entrada proporcionados, en este caso serian los siguientes

- *Relaciones entre landmarks:* Aqui podemos usar las distancias y angulos entre los puntos clave de las landmarks como lo serian los ojos, la boca y la nariz, asi como las cejas y quiza la barbilla y contorno del rostro.

- *Cambios faciales:* Los cambios faciales son un poco mas abstractos, ya que para entenderlos podriamos mencionar que, cuando alguien sonrie, esto implica que la distancia entre las esquinas de la boca y la nariz aumentan, esto seria utilizado para poder entender y identificar las emociones 

- *Simetria del rostro:* Aqui podemos decir que algunas emociones tienen simetrias, como la felicidad, y otras no como el desprecio o el enojo, por lo que seria necesario analizar este comportamiento para una identificacion mas precisa.  

#### Definir que funcion de activacion es  necesaria para este problema  
- Como funcion de activacion podriamos utilizar una funcion ReLU, debido a que esta introduce la no linealidad y tambien ayuda a mitigar los problemas de desvanecimiento, lo que nos daria resultados mas precisos.

- Como funcion de la capa de salida podemos usar una softmax, ya qye esta daria una clasificacion multiclase, perfecto para el manejo de las emociones

#### Definir el numero maximo de entradas
- Como numero maximo de entradas tenemos que saber tambien cuantas landmarks usamos, en este caso para entenderlo un poco mejor podemos decir que tiene que ver el con total de landmarks multiplicado por el tipo de cordenadas en el eje , por ejemplo si tenemos 468 landmarks en nuestro mapeo en 3 valores de coordenadas (x,y,z) sera necesario multiplicar el valor total de las landmarks x 3 para obtener las entradas totales.
  
- Puedo mencionar como extra que podriamos usar un total de 3 capas ocultas con 512,256,128 neuronas respectivamente, obteniendo como salida el total de emociones que quisieramos presentar

#### ¿Que valores a la salida de la red se podrian esperar? 
- La salida la podriamos expresar como un vector de probabilidades, donde cada valor representa una probabilidad que podria representar una emocion especifica.

- Por ejemplo, si la red neuronal está clasificando entre las emociones "alegría", "tristeza", "enojo", "miedo", "sorpresa", "disgusto" y "neutral", un vector de probabilidad podría ser:

Vector de probabilidad=[0.1,0.05,0.6,0.1,0.05,0.05,0.05]

En este caso, la red neuronal tiene una mayor confianza en que la entrada pertenece a la clase "enojo" (con una probabilidad del 60%).

#### ¿Cuales son los valores maximos que se pueden tener en el bias? 
-  En este caso se podria obtener durante el entrenamiento, pero en general seria cualquiera que tuviera la capacidad de minimizar los errores durante el entrenamiento