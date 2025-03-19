import cv2
import numpy as np

# Ruta de la imagen 
img = cv2.imread('liuywattsonpeluche.png')

# Check if the image was loaded successfully
if img is None:
    print("Error: No se pudo cargar la imagen.")
    exit()

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
ua = np.array([0, 40, 40])
ub = np.array([10, 255, 255])

ub1 = np.array([170,40,40])
ua1 = np.array([180,255,255])

mask1 = cv2.inRange(hsv, ua, ub)
mask2 = cv2.inRange(hsv, ua1, ub1)

mask = mask1+mask2


cv2.namedWindow('mask', cv2.WINDOW_NORMAL)
cv2.resizeWindow('mask', 600, 600)
cv2.imshow('mask', mask)
cv2.namedWindow('mask1', cv2.WINDOW_NORMAL)
cv2.resizeWindow('mask1', 600, 600)
cv2.imshow('mask1', mask1)
cv2.namedWindow('mask2', cv2.WINDOW_NORMAL)
cv2.resizeWindow('mask2', 600, 600)
cv2.imshow('mask2', mask2)

# Mostrar imagen original
#cv2.namedWindow('Salida1', cv2.WINDOW_NORMAL)
#cv2.resizeWindow('Salida1', 600, 600)
#cv2.imshow('Salida1', img)

# Quitar color
#img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#img3 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#img4 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Mostrar imágenes convertidas
#cv2.namedWindow('Salida2', cv2.WINDOW_NORMAL)
#cv2.resizeWindow('Salida2', 600, 600)
#cv2.imshow('Salida2', img2)

#cv2.namedWindow('Salida3', cv2.WINDOW_NORMAL)
#cv2.resizeWindow('Salida3', 600, 600)
#cv2.imshow('Salida3', img3)

#cv2.namedWindow('Salida4', cv2.WINDOW_NORMAL)
#cv2.resizeWindow('Salida4', 600, 600)
#cv2.imshow('Salida4', img4)

cv2.waitKey(0)
cv2.destroyAllWindows()