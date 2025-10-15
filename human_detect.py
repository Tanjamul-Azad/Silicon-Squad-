import cv2
import numpy as np
import time
from pyzbar.pyzbar import decode
import RPi.GPIO as GPIO
import motor_control as mc   # motor driver module

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

# -------- QR Detection Function --------
def detect_qr(frame):
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
    print("🚗 Starting Care Companion mobility system...")
    search_speed = 55  # Movement speed

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Frame error")
            break

        # Step 1: Default - move forward while scanning
        mc.forward(search_speed)
        time.sleep(0.1)

        # Step 2: Human Detection with Distance Estimation
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        found_person = False

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            class_id = int(detections[0, 0, i, 1])
            if confidence > CONF_THRESHOLD and class_id == PERSON_CLASS_ID:
                found_person = True

                # --- Extract bounding box ---
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                box_height = endY - startY
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                cv2.putText(frame, f"Person ({box_height}px)", (startX, startY - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                print(f"👤 Detected person — box height: {box_height}")

                # --- Decide approach time based on box height (distance) ---
                if box_height < 100:
                    approach_duration = 2.0   # Far → move longer
                elif box_height < 200:
                    approach_duration = 1.0   # Medium → moderate move
                else:
                    approach_duration = 0.5   # Close → short move

                print(f"🚗 Approaching for {approach_duration} seconds...")
                mc.forward(search_speed)
                time.sleep(approach_duration)
                mc.stop()

                # --- Delivery stage ---
                print("🧍 Reached human — stopping completely for delivery")
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                print("💊 Rover stopped — waiting for next instruction...")

                # Stop system after delivery (no resume)
                found_person = True
                break

        if found_person:
            break  # exit main loop after delivery

        # Step 3: QR Detection (Navigation)
        qr_data = detect_qr(frame)
        if qr_data:
            mc.stop()
            qr = qr_data.upper()
            print(f"📷 QR Detected → {qr}")
            if qr == "LEFT":
                mc.turn_left(search_speed)
                time.sleep(1)
                mc.stop()
            elif qr == "RIGHT":
                mc.turn_right(search_speed)
                time.sleep(1)
                mc.stop()
            elif qr == "STOP":
                mc.stop()
            else:
                print("⚠️ Unknown QR instruction, ignoring.")
            continue

        # Step 4: Nothing detected
        print("🔍 Searching for human or QR...")

        # Optional live preview window
        cv2.imshow("Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    print("🛑 Cleaning up...")
    mc.cleanup()
    cap.release()
    cv2.destroyAllWindows()
