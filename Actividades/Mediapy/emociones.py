import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=2, 
                                  min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Captura de video
cap = cv2.VideoCapture(0)

# Lista ampliada de índices de landmarks específicos con puntos en el contorno de la cara
selected_points = [
    33, 133, 362, 263, 61, 291, 4, 55, 65, 52, 282, 295, 285, 199, 234, 454, 10, 152, 13, 14, 78, 308, 
    67, 103, 109, 338, 297, 332, 50, 280, 88, 178, 402, 318, 324, 93, 132, 58, 172, 17, 18, 200, 421, 
    210, 429, 287, 432, 276, 424, 57, 287, 164, 0, 127, 234, 93, 132, 58, 172, 136, 150, 149, 176, 148, 
    152, 377, 400, 378, 379, 365, 397, 288, 361, 323, 454, 356, 389, 251, 284, 332
]  # Incluye puntos adicionales en el contorno de la cara

def distancia(p1, p2):
    """Calcula la distancia euclidiana entre dos puntos."""
    return np.linalg.norm(np.array(p1) - np.array(p2))

def detectar_emocion(medidas):
    """Detecta emociones basadas en las medidas faciales normalizadas y más valores."""
    # Sonrisa: boca más abierta y simetría en los labios
    if medidas["Distancia_Boca"] > medidas["Distancia_Ojos1"] * 0.8 and medidas["Angulo_Boca"] > 15 and medidas["Simetria_Boca"] < 0.1:
        return "Sonriendo"
    # Enojo: cejas más juntas y ángulo pronunciado
    elif medidas["Distancia_Cejas"] < medidas["Distancia_Ojos1"] * 0.2 and medidas["Angulo_Cejas"] > 10:
        return "Enojado"
    # Tristeza: boca menos abierta y ángulo hacia abajo
    elif medidas["Distancia_Boca"] < medidas["Distancia_Ojos1"] * 0.3 and medidas["Angulo_Boca"] < 10:
        return "Triste"
    # Sorpresa: nariz más elevada y mandíbula más abierta
    elif medidas["Distancia_Nariz"] > medidas["Distancia_Mandibula"] * 0.7 and medidas["Apertura_Mandibula"] > 0.5:
        return "Sorprendido"
    # Confusión: cejas más levantadas y asimetría en cejas
    elif medidas["Distancia_Cejas"] > medidas["Distancia_Ojos1"] * 0.5 and medidas["Simetria_Cejas"] > 0.2:
        return "Confundido"
    else:
        return "Neutral"

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
            
            # Calcular distancias adicionales y normalizarlas
            if all(k in puntos for k in [33, 133, 362, 263, 61, 291, 4, 55, 65, 10, 152]):
                d_ojos = distancia(puntos[33], puntos[133])
                d_ojos2 = distancia(puntos[362], puntos[263])
                d_boca = distancia(puntos[61], puntos[291])
                d_nariz = distancia(puntos[4], puntos[10])
                d_cejas = (distancia(puntos[55], puntos[65]) + distancia(puntos[52], puntos[282])) / 2  # Promedio de cejas
                d_mandibula = distancia(puntos[10], puntos[152])

                # Calcular ángulos adicionales
                angulo_boca = np.degrees(np.arctan2(puntos[291][1] - puntos[61][1], puntos[291][0] - puntos[61][0]))
                angulo_cejas = np.degrees(np.arctan2(puntos[65][1] - puntos[55][1], puntos[65][0] - puntos[55][0]))

                # Calcular simetría
                simetria_boca = abs(puntos[61][0] - puntos[291][0]) / d_boca
                simetria_cejas = abs(puntos[55][1] - puntos[65][1]) / d_cejas

                # Calcular apertura de la mandíbula
                apertura_mandibula = d_mandibula / d_ojos

                # Normalizar distancias usando la distancia entre los ojos como referencia
                referencia = d_ojos
                medidas_actuales = {
                    "Distancia_Ojos1": d_ojos / referencia,
                    "Distancia_Ojos2": d_ojos2 / referencia,
                    "Distancia_Boca": d_boca / referencia,
                    "Distancia_Nariz": d_nariz / referencia,
                    "Distancia_Cejas": d_cejas / referencia,
                    "Distancia_Mandibula": d_mandibula / referencia,
                    "Angulo_Boca": abs(angulo_boca),
                    "Angulo_Cejas": abs(angulo_cejas),
                    "Simetria_Boca": simetria_boca,
                    "Simetria_Cejas": simetria_cejas,
                    "Apertura_Mandibula": apertura_mandibula,
                }

                # Detectar emoción en tiempo real
                emocion = detectar_emocion(medidas_actuales)
                cv2.putText(frame, f"Emocion: {emocion}", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                # Mostrar distancias en pantalla
                cv2.putText(frame, f"D ojos: {int(d_ojos)}", (puntos[33][0], puntos[33][1] - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                cv2.putText(frame, f"D boca: {int(d_boca)}", (puntos[61][0], puntos[61][1] - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                cv2.putText(frame, f"D cejas: {int(d_cejas)}", (puntos[55][0], puntos[55][1] - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                cv2.putText(frame, f"D nariz: {int(d_nariz)}", (puntos[4][0], puntos[4][1] - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imshow('PuntosFacialesMediaPipe', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()