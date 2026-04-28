from picamera2 import Picamera2
from ultralytics import YOLO
import cv2
import time

# Initialisation
print("Chargement du modèle YOLOv8...")
model = YOLO("yolov8n.pt")
print(" Modèle chargé !")

# Initialisation caméra
picam2 = Picamera2()
picam2.start()
time.sleep(2) 

print(" Détection en cours... (Ctrl+C pour arrêter)")

while True:
    # Capture une frame
    frame = picam2.capture_array()
    
    # Convertir en BGR pour OpenCV
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
    
    # Détection YOLOv8
    results = model(frame_bgr, classes=[0], verbose=False)
    
    # Afficher les résultats
    nb_personnes = len(results[0].boxes)
    print(f" Personnes détectées : {nb_personnes}")
    
    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        print(f"   Position pixel : ({cx}, {cy}) | Confiance : {conf:.2f}")
    
    time.sleep(0.5)
