import cv2
import pyzbar.pyzbar as pyzbar
import time
import base64

# Starting the webcam
capt = cv2.VideoCapture(0)

# Creating Attendees file
with open('attendees.txt', 'a+') as fob:
    attendees = set()  # Use a set to store unique attendees

    print('Reading code...')

    def enterData(data):
        data_str = decode_base64(data)  # Decode Base64 data
        if data_str and data_str not in attendees:
            attendees.add(data_str)
            fob.write(data_str + '\n')
            return attendees

    def decode_base64(data):
        # Remove the leading 'b' and single quotes
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
            time.sleep(1)

        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.destroyAllWindows()
            break