#PROGRAM FOR MANUALLY CHOOSING THE VALID REACHES FOR ANALYSIS
# Input - csv file from Anipose
# Output - h5 file containing the Table with the parameters needed for tracking (X,Y,Z) and added parameters like velocity and acceleration + list of all reaches chosen 

import numpy as np
import pandas as pd
import h5py
import math
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.filedialog import askopenfilename
from matplotlib.widgets import Slider, Button, SpanSelector
from matplotlib import gridspec
from scipy.signal import find_peaks, peak_widths


class TrackingViewer:
    def __init__(self, usecols: list, fps: int, length: int, start: int, thres: int, peak_width: list):
    
        #open file
        root = Tk()
        root.update()
        self.name = askopenfilename(filetypes =[('Dataself.table Files', '*.csv')])
        root.destroy()


        #parameters
        self.fps = fps
        self.length = length
        self.usecols = usecols
        self.start_point = start
        self.thres_point = thres
        self_peak_width = peak_width


        # make the table with all parameters
        self.table = pd.read_csv(self.name, header=0, usecols=self.usecols)                        # choose particular columns from the original dataframe
        self.table['dx'] = self.table[self.usecols[0]].diff()                                      # substracting absolute values
        self.table['dy'] = self.table[self.usecols[1]].diff()    
        self.table['dz'] = self.table[self.usecols[2]].diff()    
        self.table['dE'] = np.linalg.norm(self.table[['dx','dy','dz']].values, axis=1)
        self.table['time'] = np.linspace(0.0, self.table.shape[0]/self.fps, num=self.table.shape[0])  # based on fps, probably need to get real timestamps
        self.table['time_diff'] = self.table['time'] - self.table['time'].shift(1)
        self.table['velocity'] = (self.table['dE']/self.table['time_diff'])
        self.table['acceleration'] = (self.table['velocity'].diff()/self.table['time_diff'])
        self.table['jerk'] = (self.table['acceleration'].diff()/self.table['time_diff'])
        
        
        # automatic peak detection and alignment
        self.reach_table = self.table.copy()
        self.reach_table.loc[self.table['paw_x'] < self.start_point,'paw_x'] = self.start_point           # Step 1 - finding only the movement forward from the starting point
        peaks, _ = find_peaks(self.reach_table['paw_x'], height=self.thres_point, width=self_peak_width)                   # Step 2 - finding the peaks automatically based on the threshold_point
        results_full = peak_widths(self.reach_table['paw_x'], peaks, rel_height=1)
        
        self.reach_list_preliminary = []

        for i in zip(results_full[2], results_full[3]):
            self.reach_list_preliminary.append((int(i[0]),int(i[1])))



        for k in enumerate(self.reach_list_preliminary):                                                             # Step 3 - deinterleaving the detected reaches
            for l in enumerate(self.reach_list_preliminary):
                if l[1][0] < k[1][0] < l[1][1]:
                    self.reach_list_preliminary[k[0]] = (l[1][0],self.reach_list_preliminary[k[0]][1])
                if l[1][0] < k[1][1] < l[1][1]:
                    self.reach_list_preliminary[l[0]] = (k[1][1],self.reach_list_preliminary[l[0]][1])
              
        self.reach_table[:][:] = np.nan
        for part in self.reach_list_preliminary:                                                                     # choose the reaches based on the start and end coordinates found automatically 
            start, end = part
            self.reach_table[start:end] = self.table[start:end]
        

        # Make all the axis and plots
        last_epoch = math.floor(self.table.shape[0]/self.length)
        plt.rcParams.update({'font.size': 14})
        fig = plt.figure(figsize=(10,10))
        gs = gridspec.GridSpec(2, 2, height_ratios=[4, 1])
        self.ax = fig.add_subplot(gs[0,:], projection='3d')
        self.ax2 = fig.add_subplot(gs[1,0])
        self.ax3 = fig.add_subplot(gs[1,1])
        ax_sl = plt.axes([0.1, .04, 0.82, 0.04])
        ax_bt = plt.axes([0.81, 0.31, 0.1, 0.075])
        ax_bt2 = plt.axes([0.13, 0.31, 0.1, 0.075])
        self.ax.set_xlabel('X, mm')
        self.ax.set_ylabel('Y, mm')
        self.ax.set_zlabel('Z, mm')
        self.ax.set_title(self.name[-10:-4] + ' frames: 0-' + str(self.length-1))
        self.ax2.set_title('X, mm')
        self.ax3.set_title('Y, mm')
        self.ax3.yaxis.tick_right()
        #self.ax.invert_zaxis()
        #ax.set_xlim(1.5,8)
        #ax.set_ylim(210,215)
        #ax.set_zlim(-2,6)


        # Plot everything for the first time
        self.start, self.stop= 0, self.length
        self.table_plot = self.table[self.start:self.stop]
        self.reach_table_plot = self.reach_table[self.start:self.stop]
        
        x = self.table_plot[self.usecols[0]]
        z = self.table_plot[self.usecols[2]]
        y = self.table_plot[self.usecols[1]]
        x2 = self.table_plot[self.usecols[0]]
        y2 = self.table_plot[self.usecols[1]]
        x3 = self.reach_table_plot[self.usecols[0]]
        y3 = self.reach_table_plot[self.usecols[1]]

        plt1 = self.ax.scatter(x,y,z, s=50 , c=self.table_plot['velocity'])
        plt2 = self.ax.plot(x,y,z, linewidth=2, color='blue', label='open')
        dot_start = self.ax.scatter(-7,0,0, s=200, c='b', alpha=0.5)                        #this dot represents the start point (corner of the slit)
        dot_pellet = self.ax.scatter(0,0,0, s=600, c='r', alpha=0.5)                        #this dot represents the end point (the food pellet)
        plt3 = self.ax2.plot(x2)
        plt4 = self.ax3.plot(y2)
        plt5 = self.ax2.plot(x3, color='r')
        plt6 = self.ax3.plot(y3, color='r')         

        self.slide = Slider(ax_sl, 'frames', 0, last_epoch, valinit=0, valfmt='%.0f')
        self.button = Button(ax_bt, 'Save_all',color="green")
        self.button2 = Button(ax_bt2, 'Save', color="green")
        self.span = SpanSelector(self.ax2, self.on_select, 'horizontal', useblit=True,
                        rectprops=dict(alpha=0.5, facecolor='red'))
        self.span.set_visible(True)
        self.span2 = SpanSelector(self.ax3, self.on_select, 'horizontal', useblit=True,
                        rectprops=dict(alpha=0.5, facecolor='red'))
        self.span2.set_visible(True)
        self.slide.on_changed(self.update)
        self.button.on_clicked(self.save)
        self.button2.on_clicked(self.save_select)
        plt.show()

    def save(self, event):  #eventhandler for the save all button

        with h5py.File(self.name[:-4]+'.h5', 'w') as f:
            f['data'] = self.table
            f['reach_index'] = sorted(self.reach_list_preliminary, key=lambda x: x[0])
        
        print('saving everything to'+self.name[:-4]+'.h5')


    def update(self, val):  #eventhandler to update the plot when moving the progress bar

        frame = math.floor(val)
        self.start, self.stop = frame*self.length, frame*self.length + self.length  
        
        # Plot everything for the n time
        self.table_plot = self.table[int(self.start):int(self.stop)]
        self.reach_table_plot = self.reach_table[self.start:self.stop]
        
        x = self.table_plot[self.usecols[0]]
        z = self.table_plot[self.usecols[2]]
        y = self.table_plot[self.usecols[1]]
        x2 = self.table_plot[self.usecols[0]]
        y2 = self.table_plot[self.usecols[1]]
        x3 = self.reach_table_plot[self.usecols[0]]
        y3 = self.reach_table_plot[self.usecols[1]]
        
        self.ax.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax.set_xlabel('X, mm')
        self.ax.set_ylabel('Y, mm')
        self.ax.set_zlabel('Z, mm') 
        self.ax.set_title(self.name[-10:-4] + ' frames: ' + str(self.start) + '-' + str(self.stop))
        self.ax2.set_title('X, mm')
        self.ax3.set_title('Y, mm')
        #self.ax.invert_zaxis()
        plt1 = self.ax.scatter(x,y,z, s=50 , c=self.table_plot['velocity'])
        plt2 = self.ax.plot(x,y,z, linewidth=2, color='blue', label='open')
        dot_start = self.ax.scatter(-7,0,0, s=200, c='b', alpha=0.5)
        dot_pellet = self.ax.scatter(0,0,0, s=600, c='r', alpha=0.5)
        plt3 = self.ax2.plot(x2)   
        plt4 = self.ax3.plot(y2)
        plt5 = self.ax2.plot(x3, color='r')
        plt6 = self.ax3.plot(y3, color='r')         
        
        self.span = SpanSelector(self.ax2, self.on_select, 'horizontal', useblit=True,
                        rectprops=dict(alpha=0.5, facecolor='red'))
        self.span.set_visible(True)
        self.span2 = SpanSelector(self.ax3, self.on_select, 'horizontal', useblit=True,
                        rectprops=dict(alpha=0.5, facecolor='red'))
        self.span2.set_visible(True)

        
    def on_select(self, min: float, max: float):   #eventhandler to select single reach for display

        self.start, self.stop = int(min), int(max)
        self.table_plot = self.table[int(min):int(max)]
        x = self.table_plot[self.usecols[0]]
        z = self.table_plot[self.usecols[2]]
        y = self.table_plot[self.usecols[1]]
        self.ax.clear()
        
        self.ax.set_xlabel('X, mm')
        self.ax.set_ylabel('Y, mm')
        self.ax.set_zlabel('Z, mm')
        #self.ax.invert_zaxis()
        plt1 = self.ax.scatter(x,y,z, s=50 , c=self.table_plot['time'])
        plt2 = self.ax.plot(x,y,z, linewidth=2, color='blue', label='open')
        dot_start = self.ax.scatter(-7,0,0, s=200, c='b', alpha=0.5)
        dot_pellet = self.ax.scatter(0,0,0, s=600, c='r', alpha=0.5)
        
    def save_select(self, event):           #eventhandler to save one button

        save=0
            # Step 4 - Updating the automatic reach list with manually adjusted value
        for l in enumerate(self.reach_list_preliminary):
            if l[1][0] < self.start < l[1][1]:
                self.reach_list_preliminary[l[0]] = (self.start, self.stop)
                save=1
            elif l[1][0] < self.stop < l[1][1]:
                self.reach_list_preliminary[l[0]] = (self.start, self.stop)
                save=1
            elif  self.start < l[1][0] < self.stop:
                self.reach_list_preliminary[l[0]] = (self.start, self.stop)
                save=1
            elif  self.start < l[1][1] < self.stop:
                self.reach_list_preliminary[l[0]] = (self.start, self.stop)
                save=1
            
                
        if save==0:
            self.reach_list_preliminary.append((self.start, self.stop))
        
        print('Updated!')
    