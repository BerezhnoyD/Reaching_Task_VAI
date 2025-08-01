# Function to split single video into three camera views for rurther analysis and 3d reconstruction

import cv2
from tkinter import *
from tkinter.filedialog import askopenfilename

def video_split():                      
    
    # Opening the video
    root = Tk()
    root.update()
    filename = askopenfilename()
    root.destroy() 

    cap = cv2.VideoCapture(filename)
    fps = 25
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    
    
    # Splitting the video in parts
    parts = [(0,frame_count)] # That can be changed if you want to extract the important parts from the video based on timing
    
    x=0                       # Those are cutting parameters dependent on your particular video dimensions and how you want to cut it
    y=0                       # Left Camera
    w=300
    h=408

    x2=300                    # Central Camera
    y2=0
    w2=1124
    h2=408

    x3=1123                   # Right Camera
    y3=0
    w3=1424
    h3=408


    out1 = cv2.VideoWriter(filename[:-4]+'-camA.mp4', fourcc, fps, ((w-x),(h-y)))
    out2 = cv2.VideoWriter(filename[:-4]+'-camB.mp4', fourcc, fps, ((w2-x2),(h2-y2)))
    out3 = cv2.VideoWriter(filename[:-4]+'-camC.mp4', fourcc, fps, ((w3-x3),(h3-y3)))


    # Reading and saving the frames
    f = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            f +=1
            for i, part in enumerate(parts):
                start, end = part
                if start <= f <= end:
                    cam1 = frame[x:h, y:w]
                    cam1 = cv2.flip(cam1,1)

                    cam2 = frame[y2:h2, x2:w2]

                    cam3 = frame[y3:h3, x3:w3]
                    cam3 = cv2.flip(cam3,1)

                    #cv2.imshow('camera-1', cam1)    #If you want to look at the resulting videos, may slow the process
                    #cv2.imshow('camera-2', cam2)
                    #cv2.imshow('camera-3', cam3)

                    cam1 = cv2.resize(cam1,((w-x),(h-y)))
                    cam2 = cv2.resize(cam2,((w2-x2),(h2-y2)))
                    cam3 = cv2.resize(cam3,((w3-x3),(h3-y3)))

                    out1.write(cam1)
                    out2.write(cam2)
                    out3.write(cam3)
                

            #k = cv2.waitKey(1) & 0xFF              #This line of code should be included if you want to look at the resulting videos
            #if k == 27:
            #    break
        else:
            break

    cap.release()
    out1.release()
    out2.release()
    out3.release()

    cv2.destroyAllWindows()
    print('Done! Your videos are there ' +filename[:-4]+'-camA.mp4')