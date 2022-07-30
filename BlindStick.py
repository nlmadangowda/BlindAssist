import RPi.GPIO as GPIO
import time
from google.cloud import vision
import io
import cv2
import sys
import os
from subprocess import call
import serial               #import serial pacakge
from threading import Timer
from pushbullet import Pushbullet


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER_L = 23
GPIO_ECHO_L = 24
GPIO_TRIGGER_R = 20
GPIO_ECHO_R = 21

GPIO.setup(GPIO_TRIGGER_L, GPIO.OUT)
GPIO.setup(GPIO_ECHO_L, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_R, GPIO.OUT)
GPIO.setup(GPIO_ECHO_R, GPIO.IN)

RELAIS_1_GPIO = 12
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
GPIO.output(RELAIS_1_GPIO, True) # out


cmd_beg= 'espeak '
cmd_end= ' | aplay /home/pi/Desktop/Text.wav  2>/dev/null' # To play back the stored .wav file and to dump the std errors to /dev/null
cmd_out= '--stdout > /home/pi/Desktop/Text.wav ' # To store the voice file

cam = cv2.VideoCapture(0)

pb = Pushbullet("o.nYtPq8f3uqyOZqDyTH4OdhQHBJ6gDPx7")

# cv2.namedWindow("press space to take a photo", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("press space to take a photo", 500, 300)
# ret, frame = cam.read()
# cv2.imshow("press space to take a photo", frame)


# client = vision.ImageAnnotatorClient()





def detect_faces(image):
    """Detects faces in an image."""
    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


def detect_labels(image):
    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


def detect_crop_hints(image):
    """Detects crop hints in an image."""
    crop_hints_params = vision.CropHintsParams(aspect_ratios=[1.77])
    image_context = vision.ImageContext(
        crop_hints_params=crop_hints_params)

    response = client.crop_hints(image=image, image_context=image_context)
    hints = response.crop_hints_annotation.crop_hints

    for n, hint in enumerate(hints):
        print('\nCrop Hint: {}'.format(n))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in hint.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


def detect_landmarks(image):
    """Detects landmarks in the file."""
    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    print('Landmarks:')

    for landmark in landmarks:
        print(landmark.description)
        for location in landmark.locations:
            lat_lng = location.lat_lng
            print('Latitude {}'.format(lat_lng.latitude))
            print('Longitude {}'.format(lat_lng.longitude))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


def detect_logos(image):
    """Detects logos in the file."""
    response = client.logo_detection(image=image)
    logos = response.logo_annotations
    print('Logos:')

    for logo in logos:
        print(logo.description)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


def localize_objects(image):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))


def pic_to_text(image):
    response = client.document_text_detection(image=image)
    text = response.full_text_annotation.text
    print("Detected text: {}".format(text))
    return text

def distance(trig,echo):
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    while GPIO.input(echo) == 0:
        StartTime = time.time()
 
    while GPIO.input(echo) == 1:
        StopTime = time.time()
 
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    return distance



obj_range = 10
obj_found = 0

gpgga_info = "$GPGGA,"
ser = serial.Serial ("/dev/ttyAMA0",baudrate = 9600, timeout = 10)              #Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0


name = "madan"

def GPS_Info():
    global NMEA_buff
    global lat_in_degrees
    global long_in_degrees
    nmea_time = []
    nmea_latitude = []
    nmea_longitude = []
    nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
    nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
    nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
    
    print("NMEA Time: ", nmea_time,'\n')
    print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')
    
    lat = float(nmea_latitude)                  #convert string into float for calculation
    longi = float(nmea_longitude)               #convertr string into float for calculation
    
    lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
    long_in_degrees = convert_to_degrees(longi) #get longitude in degree decimal format
    dev = pb.devices[0]

    push = dev.push_note("lat", lat_in_degrees)
    push = dev.push_note("lon", long_in_degrees)

    
#convert raw NMEA string into degree decimal format   
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position
    
gps_timer = time.time()
gps_timeout = 2
if __name__ == '__main__':
    try:
        while True:
            k = cv2.waitKey(1)
            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing…")
                break

            if(int(time.time()) - gps_timer >= gps_timeout):
                gps_timer = int(time.time())
                try:
                    received_data = (str)(ser.readline())                   #read NMEA string received           
                    GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                 
                    if (GPGGA_data_available>0):
                        GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
                        NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
                        GPS_Info() 
                except serial.serialutil.SerialException:
                    print("GPS data not found")

           
            ret, frame = cam.read()
            # cv2.imshow("press space to take a photo", frame)

            L_dist = distance(GPIO_TRIGGER_L,GPIO_ECHO_L)
            R_dist = distance(GPIO_TRIGGER_R,GPIO_ECHO_R)
            # print ("L= %.1f cm" % L_dist)
            # print ("R= %.1f cm" % R_dist)
            if(L_dist < R_dist):
                if(L_dist < obj_range):
                    obj_found = 1
                    text = "obf found in Left move right"
            elif(R_dist<L_dist):
                if(R_dist < obj_range):
                    obj_found = 2
                    text = "obj found in Right move left"
            elif(R_dist < obj_range or L_dist < obj_range):
                obj_found = 3
                text = "Stop"
            else:
                print("no obj found")

            if(obj_found!=0):
                obj_found=0
                text = text.replace(' ', '_')
                call([cmd_beg+cmd_out+text+cmd_end], shell=True)
                GPIO.output(RELAIS_1_GPIO, False)
                img_name = "res/img1.jpg"
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                with io.open(img_name, 'rb') as image_file:
                    content = image_file.read()
                # image = vision.Image(content=content)
                # detect_faces(image)
                # detect_labels(image)
                # detect_crop_hints(image)
                # detect_landmarks(image)
                # detect_logos(image)
                # localize_objects(image)
                # text = pic_to_text(image)
                # call([cmd_beg+cmd_out+text+cmd_end], shell=True)
            else:
                GPIO.output(RELAIS_1_GPIO, True) # out
     
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
        cam.release()
        cv2.destroyAllWindows()
        sys.exit(0)