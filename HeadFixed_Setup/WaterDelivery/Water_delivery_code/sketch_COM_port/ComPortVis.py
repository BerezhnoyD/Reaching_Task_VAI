# Jason Keller - Modified by Daniil Berezhoi
# Apr 2022
# =============================================================================
#  Program to set BlackFly S camera settings and acquire frames and write them
#  to a compressed video file. Based on FLIR Spinnaker API example code. I have 
#  also tested with a Flea3 camera, which works but requires modifying the camera
#  settings section to use non "Quickspin" functions (see FLIR examples). 
# 
#  The intent is that the DAQ program is started first, then will wait for camera
#  exposure signals to be read. DAQ should sample this at greater that 2x the frame
#  rate, preferably oversampling by ~10x.
#
#  Tkinter is used to provide a simple GUI to display the images, and skvideo 
#  is used as a wrapper to ffmpeg to write H.264 compressed video quickly, using
#  mostly default parameters (although I tried pix_fmt gray to reduce size further,
#  but default worked better).
#
#  To setup, you must download an FFMPEG executable and set an environment 
#  variable path to it (as well as setFFmpegPath function below). Other nonstandard
#  dependencies are the FLIR Spinnaker camera driver and PySpin package (see 
#  Spinnaker downloads), and the skvideo package. 
#
#  * Added also the logger for behavioral box in a separate thread.
#    It finds the COMport with Arduino Nano, links to it and starts collecting data,
#    Saving it in a text file in the same folder as the video from the FLIR
# =============================================================================

import PySpin, time, threading, queue, os, serial, csv
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1'
import serial.tools.list_ports
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import numpy as np
import collections
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


BAUD = 115200
SAVE_FOLDER_ROOT = 'C:/FLIR/Videos'
FILENAME_ROOT = 'mj_' # optional identifier


# Loading the serial device
port = list(serial.tools.list_ports.grep("1A86"))
if not port:
	raise IOError("Serial device not found! Connect the behavioral box to computer")
else:
	dev = port[0][0]

# INITIALIZE COM_PORT #######################################################################################################
ser = serial.Serial(dev, BAUD)
ser.flushInput()

# INITIALIZE PLOTTING INTERFACE 

# Initialize data storage
x = np.linspace(-30, 0, 1000) # make 1,000 points evenly distributed from -30 to 0
y = collections.deque([0]*1000, maxlen=1000)



fig, ax = plt.subplots()
line, = ax.plot(x, y, lw=2)
ax.set_xlim(0, 100)  # Adjust as needed
ax.set_ylim(0, 200)  # Adjust based on your data range
ax.set_title("Real-Time Serial Data")
ax.set_xlabel("Time")
ax.set_ylabel("Value")


# generate output video directory and filename and make sure not overwriting
now = datetime.now()
mouseStr = input("Enter mouse ID: ") 
dateStr = now.strftime("%Y_%m_%d") #save folder ex: 2020_01_01
timeStr = now.strftime("%H_%M_%S") 
saveFolder = SAVE_FOLDER_ROOT + '/' + dateStr
if not os.path.exists(saveFolder):
    os.mkdir(saveFolder)
os.chdir(saveFolder)
logName = FILENAME_ROOT + timeStr + '_' + mouseStr + '.txt'
fullFilePath = [saveFolder + '/' + logName]
print('Log will be saved to: {}'.format(fullFilePath))

            
def update_ser():
    global ser, logName, i, data, x, y
    t = threading.currentThread()
    logfile = open(logName, "w")
    while getattr(t, "running", True):
        ser_in = None
        while ser_in is None:
            try:
                ser_bytes = ser.readline()
                ser_in = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")
                data = ser.readline().decode('utf-8').strip().strip()[1]
                x.append(time.time())
                y.appedn(data)
                print(data)
            except ValueError:
                pass
        logfile.write(str(ser_in)+"\n")
    logfile.close()
            
            
            # Update function for animation
def animate(i):
    line.set_ydata(y)
    plt.ylim(min(y), max(y))



#############################################################################
# start main program loop ###################################################
#############################################################################    

try:
    print('Press Ctrl-C to exit early and save video')
    tStart = time.time()
    log_thread = threading.Thread(target=update_ser)
    
    log_thread.running = True
    log_thread.start()
    
    while True:
        tIntAcq = time.time()
       # Animate the plot
        ani = FuncAnimation(fig, animate, blit=True, interval=100)

    # Show the plot
        plt.show()
        

    

        

     
except KeyboardInterrupt: #if user hits Ctrl-C, everything should end gracefully
    tIntAcq = time.time()
    print('Interrupted by user')
    pass        

finally:        
# NOTE that from the penultimate image grab until EndAcquisition to stop Line 1 will take a few milliseconds,
# so the last AcquisitionActive edges can be discarded by the DAQ system
    log_thread.running = False
    log_thread.join()
    ser.close()
    plt.close()
    print('Capture ends')

    print('Done!')

exit(1)
