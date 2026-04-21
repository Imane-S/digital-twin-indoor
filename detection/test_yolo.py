from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")
print(" YOLOv8 installé t prêt")

cap = cv2.VideoCapture(0)
while True :     
    ret, frame = cap.read()
    if not ret : 
        break
    results = model(frame, classes=[0], verbose=False)
    annotated = results[0].plot()
    cv2.imshow("Test YOLO - personnes", annotated)
    if cv2.waitKey(1) == ord('q'):
        break
    cap.release()
