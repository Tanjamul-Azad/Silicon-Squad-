import cv2
import numpy as np
import time
from pyzbar.pyzbar import decode
import RPi.GPIO as GPIO

# -------- GPIO Setup for Buzzer --------
BUZZER_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# -------- Camera Init --------
print("📷 Initializing camera...")
cap = cv2.VideoCapture(0)
time.sleep(2.0)   # Allow camera to warm up
if not cap.isOpened():
    print("❌ Camera not opened! Check connection.")
    exit()
else:
    print("✅ Camera initialized successfully")

# -------- Load Human Detection Model --------
print("🤖 Loading MobileNetSSD model...")
net = cv2.dnn.readNetFromCaffe(
    "MobileNetSSD_deploy.prototxt",
    "MobileNetSSD_deploy.caffemodel"
)
CLASSES = ["background","aeroplane","bicycle","bird","boat",
           "bottle","bus","car","cat","chair","cow","diningtable",
           "dog","horse","motorbike","person","pottedplant",
           "sheep","sofa","train","tvmonitor"]
PERSON_CLASS_ID = 15
CONF_THRESHOLD = 0.3
print("✅ Model loaded successfully")

# -------- Functions --------
def detect_human(frame):
    """Return True if human found in frame"""
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        class_id = int(detections[0, 0, i, 1])
        if confidence > CONF_THRESHOLD and class_id == PERSON_CLASS_ID:
            # Draw bounding box for visualization
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            cv2.putText(frame, "Person", (startX, startY - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            return True
    return False

def detect_qr(frame):
    """Return QR code data if found, else None"""
    codes = decode(frame)
    if codes:
        for code in codes:
            qr_data = code.data.decode("utf-8")
            (x, y, w, h) = code.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, qr_data, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            return qr_data
    return None

# -------- Main Loop --------
try:
    print("🚀 Starting detection loop. Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame")
            break

        # ----- Step 1: Human Detection Priority -----
        if detect_human(frame):
            print("👤 Human detected → BUZZER ALERT ON")
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            # TODO: Add theme/task execution here
            continue  # Skip QR detection this frame

        # ----- Step 2: QR Code Detection Only if No Human -----
        qr_data = detect_qr(frame)
        if qr_data:
            print(f"📷 QR Code detected → Data: {qr_data}")
            # Example QR actions: replace with your motor commands
            if qr_data.upper() == "STOP":
                print("➡️ Action: Stop the robot")
            elif qr_data.upper() == "LEFT":
                print("➡️ Action: Turn Left")
            elif qr_data.upper() == "RIGHT":
                print("➡️ Action: Turn Right")
            else:
                print("➡️ Unknown QR instruction, ignoring.")
            continue  # After QR action, next frame checks human again

        # ----- Step 3: Nothing Found -----
        print("No human, no QR → searching...")

        # Show frame (optional for debugging)
        cv2.imshow("Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    print("🛑 Exiting...")
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
