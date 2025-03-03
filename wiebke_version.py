import cv2
import numpy as np
import time
import winsound  # For sound notification (Windows only)

# Initialize the camera
cap = cv2.VideoCapture(0)  # Use the default camera

if not cap.isOpened():
    print("Error opening the camera!")
    exit()

# Wait for the first frame to be captured
ret, first_frame = cap.read()
if not ret:
    print("Failed to capture the first image!")
    cap.release()
    exit()

# Convert first frame to grayscale and set as default
first_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

# Function to signal a change in the graphic
def signal_change():
    print("Graphic change detected! Alarm activated.")
    
    # Sound signal (e.g., a 1-second beep)
    winsound.Beep(1000, 1000)  # Frequency: 1000 Hz, Duration: 1000 ms

# Main program loop
while True:
    ret, frame = cap.read()  # Capture a frame from the camera
    if not ret:
        print("Failed to capture image from camera!")
        break

    # Convert the current camera frame to grayscale for comparison
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Resize images to match the camera frame size if necessary
    if first_gray.shape != gray_frame.shape:
        first_gray = cv2.resize(first_gray, (gray_frame.shape[1], gray_frame.shape[0]))

    # Compare frames (detect changes)
    diff = cv2.absdiff(gray_frame, first_gray)
    _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
    
    # Ignore black lines (treat pixels below a brightness threshold as unchanged)
    black_mask = first_gray < 50  # Adjust threshold for black detection if needed
    thresh[black_mask] = 0  # Ignore black areas in the comparison

    changes = np.count_nonzero(thresh)

    # If changes exceed the threshold, trigger an alarm
    if changes > 1000:
        cv2.rectangle(frame, (50, 50), (200, 200), (0, 255, 0), 2)
        signal_change()  # Trigger the change alarm
    
    # Display the current camera frame
    cv2.imshow('Frame', frame)

    # Exit the program when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
