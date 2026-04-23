from picamera2 import Picamera2
import cv2
import time

picam2 = Picamera2()
picam2.start()

print("Caméra démarrée !")

for i in range(10):
    frame = picam2.capture_array()
    print(f"Frame {i+1} capturée : {frame.shape}")
    time.sleep(0.5)

picam2.stop()
print("✅ Test terminé !")
