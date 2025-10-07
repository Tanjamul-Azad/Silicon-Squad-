import cv2

cap = cv2.VideoCapture(0)   # or try 1 if 0 fails
print(cap.isOpened())
cap.release()


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to grab frame.")
        break

    cv2.imshow('Camera Feed', frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):
        photo_filename = '/home/user/Desktop/care_companion/photo.jpg'
        cv2.imwrite(photo_filename, frame)
        print(f"📸 Photo captured and saved as '{photo_filename}'!")

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
