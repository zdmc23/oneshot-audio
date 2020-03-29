"""""""""""""""""""""""""""""""""
User Interface for audio-visual identification.

Calling method: python3 face_audio_detect.py <audio_model.pkl> <video_model.pkl>
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

# SECONDS OF AUDIO TO CAPTURE SNIPPET
ROLLING_RECORD_SECONDS = 4
WAVE_OUTPUT_FILENAME = "temp_files/voice.wav"

p = pyaudio.PyAudio()
# This commented-out section is for reference if the hard-coded reference to 22 (USB webcam) does not work
# TODO: fix hard-coded reference to port 22 (usb webcam)
#info = p.get_host_api_info_by_index(0)
# The following code shows what devices are available
#numdevices = info.get('deviceCount')
#for i in range(0, numdevices):
#        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
#            print ("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

#print('for usbcam -- device info')
#device_info = p.get_device_info_by_index(22)
#print(device_info)

frames = []

# to enable non-blocking audio recording -- capturing audio in 'frames' global
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

# TODO - ONCE WE ENABLE THE MODELS -- WE CAN ENABLE THE FOLLOWING CODE
# Check Arguments / Proper Usage
#if (len(sys.argv) != 3):
#    print("Error! - Usage: python3 face_audio_detect.py <audio_model.pkl> <video_model.pkl>")
#    exit()
#else:
#    audio_model = sys.argv[1]
#    video_model = sys.argv[2]

#Debug mode / flag
DEBUG=True


print("**** Starting Audio Recording ****")
stream.start_stream()


cap = cv.VideoCapture(1)
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

img_num = 0
i = 0

AUTHORIZED_FACE=False
AUTHORIZED_AUDIO=False
AUTHORIZED_BOTH=False
AUTHORIZED_FACE_TIME = None
AUTHORIZED_AUDIO_TIME = None

# Get Images and audio
while(True):
    # Capture frame-by-frame from feed
    ret, frame = cap.read()

    # gray here is the gray frame from camera
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Display image, faces, and publish message
    img = cv.imshow('frame', gray)
    
    most_recent_image = None

    for (x,y,w,h) in faces:
        crop_faces = gray[y:y+h,x:x+w]
        cv.imshow("crop", crop_faces)
        # Publish coordinates (debug)
        coord_payload = str(img_num)+ ':' + ' (' + str(x) + "," + str(y) + ')'
        most_recent_image = crop_faces
        if DEBUG:
            print(f"Image: {img_num}, payload={coord_payload} sent...")
        img_num+=1

    # write audio -- only doing this every 100 iterations to not overburden TX2
    if i % 100:
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        # if there are more than 4 seconds, trim to last 4
        if RATE / CHUNK > 4:
            wf.writeframes(b''.join(frames[-int(RATE / CHUNK * 4):]))
        else:
            wf.writeframes(b''.join(frames))
        wf.close()
    
    # NOW CHECK AUTHENTICATION (every 100 loops for now)
    if i % 100:
        #if audio was good within last TBD seconds (200 loops) -- call audio good
        if AUTHORIZED_AUDIO and AUTHORIZED_AUDIO_TIME > i - 200:
            # audio is still good -- no need to run it again
            pass
        else:
            # run new audio through model
            pass

        if AUTHORIZED_FACE and AUTHORIZED_FACE_TIME > i - 200:
            # video is still good -- no need to run it again
            pass
        else: 
            # run latest through model
            pass

        # audio can use file
        # video can use most_recent_image
        # TODO -- NORMALIZE IMAGES?


    if AUTHORIZED_FACE & AUTHORIZED_AUDIO:
        AUTHORIZED_BOTH = True
        print("AUTHORIZATION SUCCESSFUL!!!!!!!!!!!!!!!")
        break
    
    i+=1
    
    # Close the connection
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

time.sleep(1)

stream.stop_stream()
stream.close()
p.terminate()
cap.release()
cv.destroyAllWindows()
