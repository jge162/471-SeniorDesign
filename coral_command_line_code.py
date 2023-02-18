
# python3
import serial

ser = serial.Serial('/dev/ttyACM0',9600) 
ser.write(b'trash')
ser.close() 


# mdt push (file path here)
# mdt shell (connect to coral)
# ls -1
# mkdir (create folder) used to move file to folder
# mv files
# cd filename
# edgetpu_detect_server --model (.tflite file) --source (dev1 for camera) --labels (txt file)



