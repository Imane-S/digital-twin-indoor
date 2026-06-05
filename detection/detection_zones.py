from picamera2 import Picamera2
import cv2
import numpy as np
import paho.mqtt.client as mqtt
import time

# 1. Configuration MQTT

MQTT_BROKER = "192.168.1.4"
MQTT_TOPIC_A = "bureau/emplacementA"
MQTT_TOPIC_B = "bureau/emplacementB"

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
try:
    client.connect(MQTT_BROKER, 1883, 60)
    print("✅ Connecté au Broker MQTT !", flush=True)
except Exception as e:
    print(f"⚠️ Mode test sans MQTT : {e}", flush=True)

# 2. Définition des Zones (Calibrées sur votre image)
ZONE_A = [10, 10, 190, 280]   # Rectangle Cyan (Gauche)
ZONE_B = [210, 10, 390, 280]  # Rectangle Magenta (Droite)

# 3. Initialisation de la caméra officielle (Nappe)
picam2 = Picamera2()
picam2.start()

print("🚀 Mode Cartographie prêt. Analyse en cours...", flush=True)

dernier_A = ""
dernier_B = ""

try:
    while True:
        frame = picam2.capture_array()
        frame_resized = cv2.resize(frame, (400, 300))
        frame_bgr = cv2.cvtColor(frame_resized, cv2.COLOR_RGB2BGR)
        
        gray = cv2.cvtColor(frame_resized, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        obj_dans_A = "Vide"
        obj_dans_B = "Vide"
        
        for cnt in contours:
            if cv2.contourArea(cnt) > 800:
                x, y, w, h = cv2.boundingRect(cnt)
                cx, cy = x + w//2, y + h//2
                
                if ZONE_A[0] < cx < ZONE_A[2] and ZONE_A[1] < cy < ZONE_A[3]:
                    obj_dans_A = "Present"
                    cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                elif ZONE_B[0] < cx < ZONE_B[2] and ZONE_B[1] < cy < ZONE_B[3]:
                    obj_dans_B = "Present"
                    cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 0, 255), 2)

        cv2.rectangle(frame_bgr, (ZONE_A[0], ZONE_A[1]), (ZONE_A[2], ZONE_A[3]), (255, 255, 0), 1)
        cv2.rectangle(frame_bgr, (ZONE_B[0], ZONE_B[1]), (ZONE_B[2], ZONE_B[3]), (255, 0, 255), 1)
        
        cv2.putText(frame_bgr, f"Zone A: {obj_dans_A}", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        cv2.putText(frame_bgr, f"Zone B: {obj_dans_B}", (215, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)

        if obj_dans_A != dernier_A or obj_dans_B != dernier_B:
            print(f"📊 Statut - Zone A: {obj_dans_A} | Zone B: {obj_dans_B}", flush=True)
            dernier_A = obj_dans_A
            dernier_B = obj_dans_B
            
            try:
                client.publish(MQTT_TOPIC_A, obj_dans_A)
                client.publish(MQTT_TOPIC_B, obj_dans_B)
            except:
                pass

        cv2.imshow("Cartographie du Bureau", frame_bgr)
        
        if cv2.waitKey(1) == ord('q'):
            break

except KeyboardInterrupt:
    print("\nArrêt demandé...", flush=True)

finally:
    picam2.stop()
    cv2.destroyAllWindows()
    try: client.disconnect()
    except: pass
    print("👋 Système arrêté proprement.", flush=True)
