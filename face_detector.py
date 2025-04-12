import cv2
import time

def detect_face():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    detected_time = None  # Variable to store the detection time

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if len(faces) > 0:
                detected_time = time.time()
                print("Face detected at", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(detected_time)))
                break

            cv2.imshow('Webcam', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # Ensure resources are released properly
        cap.release()
        cv2.destroyAllWindows()

    return detected_time

if __name__ == "__main__":
    detect_face()