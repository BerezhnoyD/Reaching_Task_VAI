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
import skvideo
skvideo.setFFmpegPath('C:/FLIRcamera/ffmpeg-master-latest-win64-gpl/bin/') #set path to ffmpeg installation before importing io
import skvideo.io


#constants
BAUD = 115200
SAVE_FOLDER_ROOT = 'C:/FLIRcamera/Videos'
FILENAME_ROOT = 'mj_' # optional identifier
EXPOSURE_TIME = 4000 # in microseconds
FRAME_RATE = 100 # frames per second
GAIN_VALUE = 15 #in dB, 0-40;
GAMMA_VALUE = 0.5 #0.25-1
SEC_TO_RECORD = 1200 #approximate # seconds to record for; can also use Ctrl-C to interupt in middle of capture
IMAGE_HEIGHT = 420  #540 pixels default
IMAGE_WIDTH = 1432 #720 pixels default
HEIGHT_OFFSET = 370 # Y, to keep in middle of sensor
WIDTH_OFFSET = 0 # X, to keep in middle of sensor


# Loading the serial device
port = list(serial.tools.list_ports.grep("1A86"))
if not port:
	raise IOError("Serial device not found! Connect the behavioral box to computer")
else:
	dev = port[0][0]

# INITIALIZE COM_PORT #######################################################################################################
ser = serial.Serial(dev, BAUD)
ser.flushInput()

# generate output video directory and filename and make sure not overwriting
now = datetime.now()
mouseStr = input("Enter mouse ID: ") 
dateStr = now.strftime("%Y_%m_%d") #save folder ex: 2020_01_01
timeStr = now.strftime("%H_%M_%S") 
saveFolder = SAVE_FOLDER_ROOT + '/' + dateStr
if not os.path.exists(saveFolder):
    os.mkdir(saveFolder)
os.chdir(saveFolder)
movieName = FILENAME_ROOT + timeStr + '_' + mouseStr + '.mp4'
logName = FILENAME_ROOT + timeStr + '_' + mouseStr + '.txt'
fullFilePath = [saveFolder + '/' + movieName]
print('Video will be saved to: {}'.format(fullFilePath))

# SETUP FUNCTIONS #############################################################################################################
def initCam(cam): #function to initialize camera parameters for synchronized capture
    cam.Init()
    # load default configuration
    cam.UserSetSelector.SetValue(PySpin.UserSetSelector_Default)
    cam.UserSetLoad()
    # set acquisition. Continues acquisition. Auto exposure off. Set frame rate using FPS. 
    cam.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)
    cam.ExposureAuto.SetValue(PySpin.ExposureAuto_Off)
    cam.ExposureMode.SetValue(PySpin.ExposureMode_Timed) #Timed or TriggerWidth (must comment out trigger parameters other that Line)
    cam.ExposureTime.SetValue(EXPOSURE_TIME)
    cam.AcquisitionFrameRateEnable.SetValue(True)
    cam.AcquisitionFrameRate.SetValue(FRAME_RATE)
    # set analog. Set Gain + Gamma. 
    cam.GainAuto.SetValue(PySpin.GainAuto_Off)
    cam.Gain.SetValue(GAIN_VALUE)
    cam.GammaEnable.SetValue(True)
    cam.Gamma.SetValue(GAMMA_VALUE)
    # set ADC bit depth and image pixel depth, size
    cam.AdcBitDepth.SetValue(PySpin.AdcBitDepth_Bit10)
    cam.PixelFormat.SetValue(PySpin.PixelFormat_Mono8)
    cam.Width.SetValue(IMAGE_WIDTH)
    cam.Height.SetValue(IMAGE_HEIGHT)
    cam.OffsetX.SetValue(WIDTH_OFFSET)
    cam.OffsetY.SetValue(HEIGHT_OFFSET)
    # setup FIFO buffer
    camTransferLayerStream = cam.GetTLStreamNodeMap()
    handling_mode1 = PySpin.CEnumerationPtr(camTransferLayerStream.GetNode('StreamBufferHandlingMode'))
    handling_mode_entry = handling_mode1.GetEntryByName('OldestFirst')
    handling_mode1.SetIntValue(handling_mode_entry.GetValue())
    # set trigger input to Line3 if desired - default is Trigger OFF to free-run as fast as possible
    cam.TriggerMode.SetValue(PySpin.TriggerMode_On)
    cam.TriggerOverlap.SetValue(PySpin.TriggerOverlap_ReadOut) #Off or ReadOut to speed up
    cam.TriggerSource.SetValue(PySpin.TriggerSource_Line3)
    cam.TriggerActivation.SetValue(PySpin.TriggerActivation_LevelHigh) #LevelHigh or RisingEdge
    cam.TriggerSelector.SetValue(PySpin.TriggerSelector_FrameStart) # require trigger for each frame
    # optionally send exposure active signal on Line 2 
    cam.LineSelector.SetValue(PySpin.LineSelector_Line2)
    cam.LineMode.SetValue(PySpin.LineMode_Output) 
    cam.LineSource.SetValue(PySpin.LineSource_ExposureActive) #route desired output to Line 2 (try Counter0Active or ExposureActive)
    #cam.LineSelector.SetValue(PySpin.LineSelector_Line2)
    #cam.V3_3Enable.SetValue(True) #enable 3.3V rail on Line 2 (red wire) to act as a pull up for ExposureActive - this does not seem to be necessary as long as a pull up resistor is installed between the physical lines, and actually degrades signal quality
    
def save_img(image_queue, writer, i): #function to save video frames from the queue in a separate thread
    while True:
        dequeuedImage = image_queue.get() 
        if dequeuedImage is None:
            print('It is None')
            break
        else:
            writer.writeFrame(dequeuedImage)
            print(str(image_queue.qsize()))
            image_queue.task_done()

            
def update_ser():
    global ser, logName, i
    t = threading.currentThread()
    logfile = open(logName, "w")
    while getattr(t, "running", True):
        ser_in = None
        while ser_in is None:
            try:
                ser_bytes = ser.readline()
                ser_in = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")
                print(ser_in)
            except ValueError:
                pass
        logfile.write(str(ser_in)+' '+str(i)+"\n")
    logfile.close()
            
            
# INITIALIZE CAMERA & COMPRESSION ###########################################################################################
system = PySpin.System.GetInstance() # Get camera system
cam_list = system.GetCameras() # Get camera list
cam1 = cam_list[0]
initCam(cam1) 



# get frame rate and query for video length based on this
frameRate = cam1.AcquisitionResultingFrameRate()
print('frame rate = {:.2f} FPS'.format(frameRate))
numImages = round(frameRate*SEC_TO_RECORD)
print('# frames = {:d}'.format(numImages))

# setup output video file parameters (can try H265 in future for better compression):  
# for some reason FFMPEG takes exponentially longer to write at nonstandard frame rates, so just use default 25fps and change elsewhere if needed
crfOut = 21 #controls tradeoff between quality and storage, see https://trac.ffmpeg.org/wiki/Encode/H.264 
ffmpegThreads = 10 #this controls tradeoff between CPU usage and memory usage; video writes can take a long time if this value is low
#crfOut = 18 #this should look nearly lossless
#writer = skvideo.io.FFmpegWriter(movieName, outputdict={'-r': str(FRAME_RATE), '-vcodec': 'libx264', '-crf': str(crfOut)}) # with frame rate
writer = skvideo.io.FFmpegWriter(movieName, outputdict={'-vcodec': 'libx264', '-crf': str(crfOut), '-threads': str(ffmpegThreads)})

#setup tkinter GUI (non-blocking, i.e. without mainloop) to output images to screen quickly
window = tk.Tk()
window.title("camera acquisition")
geomStrWidth = str(IMAGE_WIDTH + 25)
geomStrHeight = str(IMAGE_HEIGHT + 35)
window.geometry(geomStrWidth + 'x' + geomStrHeight) # width+25 x height+35; large enough for frame + text
textlbl = tk.Label(window, text="elapsed time: ")
textlbl.grid(column=0, row=0)
canvas = tk.Canvas(window, width=IMAGE_WIDTH, height=IMAGE_HEIGHT)  # if we gonna draw we need a canvas
canvas.place(x=10, y=20) # Stretch canvas to root window size.
window.update() #update TCL tasks to make window appear

#############################################################################
# start main program loop ###################################################
#############################################################################    

try:
    print('Press Ctrl-C to exit early and save video')
    cam1.BeginAcquisition()
    tStart = time.time()
    i = 0
    image_queue = queue.Queue() #create queue in memory to store images while asynchronously written to disk
    
    # setup another thread to accelerate saving, and start immediately:
    save_thread = threading.Thread(target=save_img, args=(image_queue, writer, i,))
    save_thread.start()  
    
    log_thread = threading.Thread(target=update_ser)
    log_thread.running = True
    log_thread.start()
    

    
    # reading data from FLIR Camera and saving it to mp4
    
    for i in range(numImages):

        image = cam1.GetNextImage() #get pointer to next image in camera buffer; blocks until image arrives via USB; timeout=INF
        enqueuedImage = np.array(image.GetData(), dtype="uint8").reshape( (image.GetHeight(), image.GetWidth()) ); #convert PySpin ImagePtr into numpy array
        
        img = Image.fromarray(enqueuedImage)
        d = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 16)
        d.text((500,5), '{:.2f}'.format(time.time() - tStart)+'    '+str(i), fill=255, font=font)

        
        processedImage = np.asarray(img)
        image_queue.put(processedImage) #put next image in queue
        
        if i%15 == 0: #update screen every 10 frames 
            timeElapsed = str(time.time() - tStart)
            timeElapsedStr = "elapsed time: " + timeElapsed[0:5] + " sec"
            textlbl.configure(text=timeElapsedStr)
            I = ImageTk.PhotoImage(Image.fromarray(enqueuedImage))    #draw the current image on the canvas   
            canvas.create_image(0, 0, anchor = 'nw', image=I)           
            canvas.create_rectangle(300,0,1124,300, width=3)          #draw the rectangle on the canvas   
            window.update() #update on screen (this must be called from main thread)
            
        image.Release() #release from camera buffer

        

     
except KeyboardInterrupt: #if user hits Ctrl-C, everything should end gracefully
    tIntAcq = time.time()
    print('Interrupted by user at: {:.2f}sec'.format(tIntAcq - tStart) + ' frame#'+ str(i))
    pass        

finally:        
# NOTE that from the penultimate image grab until EndAcquisition to stop Line 1 will take a few milliseconds,
# so the last AcquisitionActive edges can be discarded by the DAQ system
    cam1.EndAcquisition() 
    tEndAcq = time.time()
    log_thread.running = False
    log_thread.join()
    ser.close()
    print('Capture ends at: {:.2f}sec'.format(tEndAcq - tStart) +' frame#'+str(i))
    #save_thread.join()
    image_queue.join() #wait until queue is done writing to disk
    tEndWrite = time.time()
    print('File written at: {:.2f}sec'.format(tEndWrite - tStart))
    writer.close()
    window.destroy()

    
del image
cam1.DeInit()
del cam1
cam_list.Clear()
del cam_list
system.ReleaseInstance()
del system
print('Done!')

exit(1)
