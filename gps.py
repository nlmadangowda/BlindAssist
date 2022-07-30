'''
GPS Interfacing with Raspberry Pi using Pyhton
http://www.electronicwings.com
'''
import serial               #import serial pacakge
import time
import webbrowser           #import package for opening link in browser
import sys                  #import system package
# from threading import Timer

import threading
def GPS_Info():
    global NMEA_buff
    global lat_in_degrees
    global long_in_degrees
    # nmea_time
    # nmea_latitude = []
    # nmea_longitude = []
    # nmea_time = int(NMEA_buff[0])                    #extract time from GPGGA string
    # nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
    # nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
    # print("NMEA Time: ", nmea_time,'\n')
    print ("NMEA Latitude:", NMEA_buff[1],"NMEA Longitude:", NMEA_buff[3],'\n')
    
    # lat = float(nmea_latitude)                  #convert string into float for calculation
    # longi = float(nmea_longitude)               #convertr string into float for calculation
    
    # lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
    # long_in_degrees = convert_to_degrees(longi) #get longitude in degree decimal format
    
#convert raw NMEA string into degree decimal format   
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position
    


gpgga_info = "$GPGGA,"
ser = serial.Serial ("/dev/ttyAMA0",baudrate = 9600, timeout = 10)              #Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0

# 12.9586
# 77.7402
def timeout():
    try:
        while True:
            try:
                received_data = (str)(ser.readline())                   #read NMEA string received
                # print(received_data)
                GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                 
                if (GPGGA_data_available>0):
                    GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
                    NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
                    GPS_Info()                                          #get time, latitude, longitude
                    print("lat in degrees:", lat_in_degrees," long in degree: ", long_in_degrees, '\n')
                    map_link = 'http://maps.google.com/?q=' + lat_in_degrees + ',' + long_in_degrees    #create link to plot location on Google map
                    print("<<<<<<<<press ctrl+c to plot location on google maps>>>>>>\n")               #press ctrl+c to plot on map and exit 
                    print("------------------------------------------------------------\n")
            except serial.SerialException as e:
                raise SerialException(serial.serialutil.SerialException: device reports readiness to read but returned no data (device disconnected or multiple access on port?)
                print("GPS data not found")
    except KeyboardInterrupt:
        # webbrowser.open(map_link)        #open current position information in google map
        sys.exit(0)


# timer = threading.Timer(2.0, timeout)
# timer.start()
# print("Exit\n")




# t = Timer(5, timeout)
# t.start()

gps_timer = int(time.time())
gps_timeout = 0

while True:
    if(int(time.time()) - gps_timer >= gps_timeout):
        gps_timer = int(time.time())
        try:
            while True:
                received_data = (str)(ser.readline())                   #read NMEA string received
                # print(received_data)
                GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                 
                if (GPGGA_data_available>0):
                    GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
                    NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
                    GPS_Info()                                          #get time, latitude, longitude
                    # print("lat in degrees:", lat_in_degrees," long in degree: ", long_in_degrees, '\n')
                    # map_link = 'http://maps.google.com/?q=' + lat_in_degrees + ',' + long_in_degrees    #create link to plot location on Google map
                    # print("<<<<<<<<press ctrl+c to plot location on google maps>>>>>>\n")               #press ctrl+c to plot on map and exit 
                    # print("------------------------------------------------------------\n")
                            
        except KeyboardInterrupt:
            # webbrowser.open(map_link)        #open current position information in google map
            sys.exit(0)