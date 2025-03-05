# Actividad 1 

### Modelar una red neuronal que pueda jugar al 5 en línea sin gravedad en un tablero de 20*20
- Definir el tipo de red neuronal y describir cada una de sus partes 
- Definir los patrones a utilizar 
- Definir la función de activación es necesaria para este problema 
- Definir el número máximo de entradas
- ¿Que valores a la salida de la red se podrían esperar?
- ¿Cuáles son los valores máximos que puede tener el bias?

#### Definir el tipo de red neuronal y describir cada una de sus partes
- Existen muchas opciones de tipos de redes neuronales que podríamos usar para resolver el problema, como en este caso el problema se puede basar más que nada en patrones debido a la complejidad del juego podríamos hacer uno de una red neuronal del tipo Convolucional(CNN), debido a que estas son usadas comúnmente para procesar datos que tienen una estructura de cuadrícula (Y en este caso estaríamos trabando con un tablero de 20*20).

**Anexo sobre Redes Neuronales del tipo Convolucional**
![alt text](image.png)

Con esto en claro, podemos definir cada una de sus partes basadas en la problematica
 
Primero, tenemos que recordar que esta red neuronal tiene como principales componentes lo siguiente:

![alt text](image-1.png)

Adaptada al problema podemos decir lo siguiente:
**Capas de entrada:** En este caso la capa de entrada seria el tablero de 20*20
**Capas de Convolución:** Se pueden detectar en este caso los patrones de lineas dentro del tablero
**Capas de Pooling:**  Para evitar el sobre ajuste se puede en este caso destacar lo mas importante (Como la cercania a una linea de 5 fichas)
**Capas de Conexión Completa:** Tomar una decision basada en lo anterior, lo que permitira hacer una jugada



