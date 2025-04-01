import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
from tkinter import Tk, simpledialog

# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_meshq
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=2, 
                                  min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Captura de video
cap = cv2.VideoCapture(0)

# Lista de índices de landmarks específicos (ojos y boca)
selected_points = [33, 133, 362, 263, 61, 291, 4]

# DataFrame para almacenar los datos
data = pd.DataFrame(columns=["Nombre", "Distancia_Ojos1", "Distancia_Ojos2", "Distancia_Boca", "Distancia_Nariz"])

def distancia(p1, p2):
    """Calcula la distancia euclidiana entre dos puntos."""
    return np.linalg.norm(np.array(p1) - np.array(p2))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Espejo para mayor naturalidad
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            puntos = {}
            
            for idx in selected_points:
                x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                puntos[idx] = (x, y)
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)  # Dibuja el punto en verde
            
            # Calcular distancias
            if 33 in puntos and 133 in puntos:
                d_ojos = distancia(puntos[33], puntos[133])
                d_ojos2 = distancia(puntos[362], puntos[263])
                d_boca = distancia(puntos[61], puntos[291])
                d_boca_mitad = distancia(puntos[61], puntos[291]) / 2
                d_nariz = distancia(puntos[4], (puntos[61][0] + d_boca_mitad, puntos[61][1]))
                
                # Mostrar distancias en pantalla
                cv2.putText(frame, f"D: {int(d_ojos)}", (puntos[33][0], puntos[33][1] - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                cv2.putText(frame, f"D: {int(d_ojos2)}", (puntos[362][0], puntos[362][1] - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                cv2.putText(frame, f"D: {int(d_boca)}", (puntos[61][0], puntos[61][1] - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                cv2.putText(frame, f"D: {int(d_nariz)}", (puntos[4][0], puntos[4][1] - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                
                # Guardar datos al presionar 's'
                if cv2.waitKey(1) & 0xFF == ord('s'):
                    # Crear un cuadro de diálogo para ingresar el nombre
                    root = Tk()
                    root.withdraw()  # Ocultar la ventana principal de Tkinter
                    nombre = simpledialog.askstring("Nombre", "Ingrese el nombre del dueño de las distancias:")
                    root.destroy()

                    if nombre:
                        # Agregar datos al DataFrame
                        data = pd.concat([data, pd.DataFrame([{
                            "Nombre": nombre,
                            "Distancia_Ojos1": d_ojos,
                            "Distancia_Ojos2": d_ojos2,
                            "Distancia_Boca": d_boca,
                            "Distancia_Nariz": d_nariz
                        }])], ignore_index=True)

                        # Guardar en un archivo Excel
                        data.to_excel("distancias_caras.xlsx", index=False)
                        print(f"Datos guardados para {nombre}")

    cv2.imshow('PuntosFacialesMediaPipe', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()