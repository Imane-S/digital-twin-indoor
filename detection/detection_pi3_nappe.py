from picamera2 import Picamera2
import cv2
import numpy as np
import paho.mqtt.client as mqtt
import time

# 1. Configuration MQTT (Mettez l'IP de votre Mac/Broker à la place du X)
MQTT_BROKER = "192.168.1.X"  
MQTT_TOPIC = "bureau/presence"

client = mqtt.Client()
try:
    client.connect(MQTT_BROKER, 1883, 60)
    print("✅ Connecté au Broker MQTT !")
except Exception as e:
    print(f"⚠️ Mode sans MQTT (Broker non trouvé) : {e}")

# 2. Configuration du modèle léger de détection de personnes
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# 3. Initialisation de la caméra officielle (Nappe) via Picamera2
picam2 = Picamera2()
picam2.start()

print("🚀 Système prêt sur Raspberry Pi 3 (Nappe). Détection en cours...")
dernier_compte = -1

try:
    while True:
        # Capture de l'image depuis la nappe
        frame = picam2.capture_array()
        
        # Le Pi 3 calcule beaucoup plus vite si l'image est un peu plus petite
        frame_resized = cv2.resize(frame, (400, 300))
        
        # Conversion en Noir et Blanc pour l'algorithme
        gray = cv2.cvtColor(frame_resized, cv2.COLOR_RGB2GRAY)
        
        # Détection des personnes
        boxes, weights = hog.detectMultiScale(gray, winStride=(8, 8), padding=(8, 8), scale=1.05)
        nb_personnes = len(boxes)
        
        # Envoi MQTT uniquement si le nombre de personnes change
        if nb_personnes != dernier_compte:
            print(f"Nombre de personnes détectées : {nb_personnes}")
            try:
                client.publish(MQTT_TOPIC, str(nb_personnes))
            except:
                pass
            dernier_compte = nb_personnes
            
        # Conversion pour l'affichage OpenCV (RGB vers BGR)
        frame_bgr = cv2.cvtColor(frame_resized, cv2.COLOR_RGB2BGR)
        
        # Dessiner les rectangles verts autour des personnes
        for (x, y, w, h) in boxes:
            cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
        # Affichage en direct sur l'écran du Mac
        cv2.imshow("Jumeau Numerique - Camere Pi 3 (Nappe)", frame_bgr)
        
        if cv2.waitKey(1) == ord('q'):
            break

except KeyboardInterrupt:
    print("\nArrêt demandé par l'utilisateur...")

finally:
    picam2.stop()
    cv2.destroyAllWindows()
    try:
        client.disconnect()
    except:
        pass
    print("✅ Système arrêté proprement.")
