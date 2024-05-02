from MyQR import myqr
import os
import base64
import cv2
import pyzbar.pyzbar as pyzbar
import time
import tkinter as tk
from threading import Thread

# Create a tkinter window
root = tk.Tk()
root.title("QR Code Attendance")

# Read student names from a file
with open('students.txt', 'r') as file:
    student_names = file.read().splitlines()

# Generate QR codes for students
for name in student_names:
    data = name.encode()
    name_encoded = base64.b64encode(data)
    version, level, qr_name = myqr.run(
        str(name_encoded),
        level='H',
        version=1,
        colorized=True,
        contrast=1.0,
        brightness=1.0,
        save_name=str(name + '.bmp'),
        save_dir=os.getcwd()
    )

# Function to start the webcam
def start_webcam():
    global attendees, capt
    attendees = set()
    
    # Start the webcam
    capt = cv2.VideoCapture(0)

    if not capt.isOpened():
        print("Error: Could not open the webcam.")
        exit()

    start_button.config(state="disabled")  # Disable the start button

    def close_webcam():
        capt.release()
        cv2.destroyAllWindows()
        message_label.config(text="Webcam closed. Attendance marked.")

    # Function to enter data
    def enterData(data):
        data_str = decode_base64(data)
        if data_str and data_str not in attendees:
            attendees.add(data_str)
            fob.write(data_str + '\n')
            return attendees

    # Function to decode base64 data
    def decode_base64(data):
        cleaned_data = data[2:-1]
        try:
            decoded_bytes = base64.b64decode(cleaned_data)
            decoded_str = decoded_bytes.decode('utf-8')
            return decoded_str
        except Exception as e:
            return None

    while True:
        _, frame = capt.read()
        decodedObjects = pyzbar.decode(frame)
        for obj in decodedObjects:
            attendee_data = obj.data
            print("QR Code Data:", attendee_data)
            enterData(attendee_data)

        cv2.imshow('Frame', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            close_webcam()
            break

# Function to start the webcam in a separate thread
def start_webcam_thread():
    webcam_thread = Thread(target=start_webcam)
    webcam_thread.start()

# Create Attendees file
with open('attendees.txt', 'a+') as fob:
    attendees = set()

    message_label = tk.Label(root, text="Click 'Start' to begin attendance.", padx=20, pady=10)
    message_label.pack()

    start_button = tk.Button(root, text="Start", command=start_webcam_thread, padx=20, pady=10)
    start_button.pack()

    close_button = tk.Button(root, text="Close", command=root.destroy, padx=20, pady=10)
    close_button.pack()

    root.mainloop()

# Release the webcam and close the tkinter window when done
capt.release()
cv2.destroyAllWindows()
