import serial
import time
import csv 

#Open file connection
#Temporary-- will configure DB connection later
f = open("output_readings.csv", "w")
f.truncate()

#Will need to match port and rate from ardunio program
serialCom = serial.Serial('COM3', 9600)

#Reset serial com
serialCom.setDTR(False)
time.sleep(1)
serialCom.flushInput()
serialCom.setDTR(True)

#Num of data points to record
kmax = 10
for k in range(kmax):
    try:
        s_bytes = serialCom.readline()
        decoded_bytes = s_bytes.decode('utf-8').strip('\r\n')

        #Parse lines
        values = [float(x) for x in decoded_bytes.split()]
        
        print(values)

        #write to file for now
        writer = csv.writer(f, delimiter=",")
        writer.writerow(values)

    except:
        ##TODO: throw error
        print("Error. Line not recorded")

f.close()



