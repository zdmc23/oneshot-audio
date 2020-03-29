"""""""""""""""""""""""""""""""""
Detect faces in USB video input and display

Calling method: python3 voice_faces_detect.py
"""""""""""""""""""""""""""""""""

import numpy as np
import cv2 as cv
import pyaudio
import wave
import threading
import time
import subprocess
import os







CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 32000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
#numdevices = info.get('deviceCount')
#for i in range(0, numdevices):
#        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
#            print ("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

#print('for usbcam -- device info')
#device_info = p.get_device_info_by_index(22)
#print(device_info)

frames = []

def callback(in_data, frame_count, time_info, status):
    global frames
    frames.append(in_data)
    return (in_data, pyaudio.paContinue)

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                input_device_index=22,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=callback)


frames = []

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)



print("**** Starting Audio Recording ****")
stream.start_stream()
#for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#    data = stream.read(CHUNK)
#    frames.append(data)
#time.sleep(5)
#print("After First Sleep")
#wf.writeframes(b''.join(frames))
#print('starting 2nd sleep')
#time.sleep(5)
#print("After Second Sleep")


#print("**** Finished Audio Recording ****")

#stream.stop_stream()
#stream.close()
#p.terminate()

#wf.writeframes(b''.join(frames))
#wf.close()



# Check Arguments / Proper Usage
#if (len(sys.argv) != 3):
#    print("Error! - Usage: python3 face_audio_detect.py <audio_model.pkl> <video_model.pkl>")
#    exit()
#else:
#    audio_model = sys.argv[1]
#    video_model = sys.argv[2]

#Debug mode / flag
DEBUG=True


cap = cv.VideoCapture(1)
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

img_num = 0

# Get Images and audio
while(True):
    # Capture frame-by-frame from feed
    ret, frame = cap.read()

    # gray here is the gray frame from camera
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Display image, faces, and publish message
    img = cv.imshow('frame', gray)
    for (x,y,w,h) in faces:
        crop_faces = gray[y:y+h,x:x+w]
        cv.imshow("crop", crop_faces)
        # Publish coordinates (debug)
        coord_payload = str(img_num)+ ':' + ' (' + str(x) + "," + str(y) + ')'
        if DEBUG:
            print(f"Image: {img_num}, payload={coord_payload} sent...")
        img_num+=1

    # write audio
    # need to limit to just the last X seconds
    # frames[-1* int(RATE / CHUNK * RECORD_SECONDS):] (if there are this many seconds recorded)
    wf.writeframes(b''.join(frames))


    # Close the connection
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

time.sleep(1)

print("**** Finished Audio Recording ****")

stream.stop_stream()
stream.close()
p.terminate()

#wf.writeframes(b''.join(frames))
wf.close()
cap.release()
cv.destroyAllWindows()
