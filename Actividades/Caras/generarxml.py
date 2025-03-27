import cv2 as cv
import numpy as np
import os

# Ruta al directorio principal que contiene las subcarpetas de clases
dataSet = r'C:\Users\avila\OneDrive\Documentos\GitHub\Inteligencia-Artificial\Actividades\Caras\Caras'

labels = []
facesData = []
label = 0

# Recorre las subcarpetas (cada subcarpeta es una clase)
for subdir in os.listdir(dataSet):
    subdirPath = os.path.join(dataSet, subdir)
    if os.path.isdir(subdirPath):  # Verifica que sea una carpeta
        for faceName in os.listdir(subdirPath):
            facePath = os.path.join(subdirPath, faceName)
            if os.path.isfile(facePath):  # Verifica que sea un archivo
                labels.append(label)
                facesData.append(cv.imread(facePath, 0))  # Lee la imagen en escala de grises
        label += 1  # Cambia de clase

# Verifica que haya al menos dos clases
if label < 2:
    raise ValueError("Se necesitan al menos dos clases para entrenar el modelo.")

# Entrena el modelo y guarda el archivo XML
faceRecognizer = cv.face.FisherFaceRecognizer_create()
faceRecognizer.train(facesData, np.array(labels))
faceRecognizer.write('FaceModel.xml')