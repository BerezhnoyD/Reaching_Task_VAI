# PROGRAM FOR OPENING PARTS OF THE VIDEO AND LOOKING ON THE ACTUAL REACHING TRAJECTORY
# Input - the h5 file generated with the tracking_split Script + the corresponding Video file for the same session
# Output - _scalars.h5 file containing list of reaches, cleared data table, list of mean and std values for all the parameters/all reaches

import time
import cv2
import ipywidgets as widgets
from IPython.display import display, clear_output
import h5py
import matplotlib.pyplot as plt
from matplotlib import gridspec
import pandas as pd
import numpy as np


class ReachesViewer:
    
    def __init__(self, file1: str, file2: str, options: list):               #Open the h5 file and make a table with scalar parameters for all reaches
        
        self.file = file1
        self.file2 = file2 
        self.f = h5py.File(self.file2,"r")
                
        self.columns_data = ['paw_x', 'paw_y', 'paw_z', 'paw_error', 'paw_score', 'dx', 'dy', 'dz',
               'dE', 'time', 'time_diff', 'velocity', 'acceleration', 'jerk']

        self.columns_df= [
                    'group', 'duration_sec', 'dx_mm',  'dy_mm', 'dz_mm', 'dE_mm', 'maxX_mm', 'minX_mm', 'abs_minX_mm', 'maxY_mm', 'minY_mm',  
                    'abs_minY_mm', 'maxZ_mm', 'minZ_mm', 'abs_minZ_mm', 'velocity_mm/sec', 'acceleration_mm/sec^2', 'jerk_mm/sec^3', 
                    'max_velocity_mm/sec', 'max_acceleration_mm/sec^2', 'max_jerk_mm/sec^3', 'max_velocity_time','peak_time_x','peak_time_y','peak_time_z']
        
        self.options = options

        self.table = pd.DataFrame(np.array(self.f['data']), columns = self.columns_data)
        self.reach_list = list(self.f['reach_index'])
        self.reach_List = list(str(k)+'-'+str(self.reach_list[k][0])+'-'+str(self.reach_list[k][1]) for k in range(len(self.reach_list)))       
        
        # make the copy of data, cleared
        self.reach_all = []
        self.reach_table = self.table.copy()
        self.reach_table[:][:] = np.nan

        for part in self.reach_list:                #choose the reaches based on the start and end coordinates found on previous stage 
            start, end = part
            self.reach_all.append(self.table[start:end])
            self.reach_table[start:end] = self.table[start:end]
            
        self.mean_df = pd.DataFrame(columns = self.columns_df)
        self.std_df = pd.DataFrame(columns = self.columns_df)
        self.reach_list_df = pd.DataFrame(data=self.reach_list, columns=['start','stop'])

        for k in range(len(self.reach_all)):        #calculate the scalar parameters
            gr = 1
            dur = self.reach_all[k]['time'].max() - self.reach_all[k]['time'].min()
            dur_std = self.reach_all[k]['time_diff'].std()
            dx = self.reach_all[k]['dx'].abs().sum()                             
            dx_std = self.reach_all[k]['dx'].std()
            dy = self.reach_all[k]['dy'].abs().sum()
            dy_std = self.reach_all[k]['dy'].std()
            dz = self.reach_all[k]['dz'].abs().sum()
            dz_std = self.reach_all[k]['dz'].std()
            de = self.reach_all[k]['dE'].abs().sum()
            de_std = self.reach_all[k]['dE'].std()
            dx2 = self.reach_all[k]['paw_x'].max() 
            dx2_std = self.reach_all[k]['paw_x'].std()
            dx3 = self.reach_all[k]['paw_x'].min() 
            dx3_std = self.reach_all[k]['paw_x'].std()
            dx4 = self.reach_all[k]['paw_x'].abs().min() 
            dx4_std = self.reach_all[k]['paw_x'].std()
            dy2 = self.reach_all[k]['paw_y'].max() 
            dy2_std = self.reach_all[k]['paw_y'].std()
            dy3 = self.reach_all[k]['paw_y'].min() 
            dy3_std = self.reach_all[k]['paw_y'].std()
            dy4 = self.reach_all[k]['paw_y'].abs().min() 
            dy4_std = self.reach_all[k]['paw_y'].std()
            dz2 = self.reach_all[k]['paw_z'].max()
            dz2_std = self.reach_all[k]['paw_z'].std()
            dz3 = self.reach_all[k]['paw_z'].min()
            dz3_std = self.reach_all[k]['paw_z'].std()
            dz4 = self.reach_all[k]['paw_z'].abs().min()
            dz4_std = self.reach_all[k]['paw_z'].std()
            vel = self.reach_all[k]['velocity'].mean()
            vel_std = self.reach_all[k]['velocity'].std()
            acc = self.reach_all[k]['acceleration'].mean()
            acc_std = self.reach_all[k]['acceleration'].std()
            jrk = self.reach_all[k]['jerk'].mean()
            jrk_std = self.reach_all[k]['jerk'].std()
            vel_max = self.reach_all[k]['velocity'].max()
            vel_max_std = self.reach_all[k]['velocity'].std()
            acc_max = self.reach_all[k]['acceleration'].max()
            acc_max_std = self.reach_all[k]['acceleration'].std()
            jrk_max = self.reach_all[k]['jerk'].max()
            jrk_max_std = self.reach_all[k]['jerk'].std()
            vel_max_pos = self.reach_all[k]['velocity'].argmax()
            vel_max_pos_std = self.reach_all[k]['velocity'].std() # That's not the real std for this parameter, just the placeholder
            dx2_time = self.reach_all[k]['paw_x'].argmax() 
            dx2_time_std = self.reach_all[k]['time_diff'].std() # That's not the real std for this parameter, just the placeholder
            dy2_time = self.reach_all[k]['paw_y'].argmin() 
            dy2_time_std = self.reach_all[k]['time_diff'].std() # That's not the real std for this parameter, just the placeholder
            dz2_time = self.reach_all[k]['paw_z'].argmax()
            dz2_time_std = self.reach_all[k]['time_diff'].std() # That's not the real std for this parameter, just the placeholder
            list1 = [gr, dur, dx, dy, dz, de, dx2, dx3, dx4, dy2, dy3, dy4, dz2, dz3, dz4, vel, acc, jrk, vel_max,
                     acc_max, jrk_max, vel_max_pos, dx2_time, dy2_time, dz2_time]
            list2 = [gr, dur_std, dx_std, dy_std, dz_std, de_std, dx2_std, dx3_std, dx4_std, dy2_std, dy3_std, dy4_std, dz2_std, dz3_std, dz4_std,
                     vel_std, acc_std, jrk_std, vel_max_std, acc_max_std, jrk_max_std, vel_max_pos_std, dx2_time_std, dy2_time_std, dz2_time_std]
            self.mean_df=pd.concat([self.mean_df, pd.DataFrame([list1], columns=self.columns_df)], ignore_index=True, axis =0)
            self.std_df=pd.concat([self.std_df, pd.DataFrame([list2], columns=self.columns_df)], ignore_index=True, axis =0)

        
        #display(dropdown)

        self.mean_df.loc[:,'group']=self.options[0]
        self.std_df.loc[:,'group']=self.options[0]


        # make the widgets
        

        self.dropdown = widgets.Select(
                            options=[' ']+self.reach_List,
                            #value=reach_List[0],
                            description='Reach:',
                            #rows = 20,
        )
        
        
        self.radiobuttons = widgets.RadioButtons(
            value=self.options[0], 
            options=self.options, 
            description='Label:'
        )
        

        self.b1 = widgets.Button(description='Save All')
        self.box=widgets.HBox([self.dropdown, self.radiobuttons, self.b1])
        self.fig = plt.figure(figsize=(10,10))
        self.gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1])
        self.ax1 = self.fig.add_subplot(self.gs[0,0], projection='3d')
        self.ax2 = self.fig.add_subplot(self.gs[0,1])
        self.ax3 = self.fig.add_subplot(self.gs[1,0])
        self.ax4 = self.fig.add_subplot(self.gs[1,1])

        self.b1.on_click(self.on_click)
        self.dropdown.observe(self.dropdown_eventhandler, names='value')
        self.radiobuttons.observe(self.radio_click, names='value')
        display(self.box) 

        
    def Plot(self):
    
        #Showing the plots
        x = self.table.loc[self.start:self.stop]['paw_x'].reset_index(drop=True)
        z = self.table.loc[self.start:self.stop]['paw_z'].reset_index(drop=True)
        y = self.table.loc[self.start:self.stop]['paw_y'].reset_index(drop=True)
        
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax4.clear()
        self.ax1.set_xlabel('X, mm')
        self.ax1.set_ylabel('Y, mm')
        self.ax1.set_zlabel('Z, mm')
        self.ax2.set_ylabel('X, mm')
        self.ax3.set_ylabel('Y, mm')
        self.ax4.set_ylabel('Z, mm')  
        
        self.plt1 = self.ax1.plot(x,y,z, linewidth=1, color='grey', label='open')
        self.plt2 = self.ax2.plot(x)
        self.plt3 = self.ax3.plot(y) 
        self.plt4 = self.ax4.plot(z)

        self.ax2.yaxis.tick_right()
        self.ax2.yaxis.set_label_position("right")
        self.ax4.yaxis.tick_right()
        self.ax4.yaxis.set_label_position("right")
        clear_output(wait=True)
        display(self.box)
        display(self.fig)    
        
        

    def Vopen(self):
        # Opening video fragments corresponding to the plot
        
        cap = cv2.VideoCapture(self.file)
        # Get the frames per second
        fps = cap.get(cv2.CAP_PROP_FPS) 

        # Get the total numer of frames in the video.
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        ret,frame = cap.read()    
        frame_number = self.start
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        while ret:  

            if frame_number <= self.stop:
                frame_number += 1
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

                ret,frame = cap.read()   
                frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) # because Bokeh expects a RGBA image

                cv2.imshow(str(self.start)+'-'+str(self.stop)+'   press Q to out', frame)
                key = cv2.waitKey(10) & 0xFF
            
                # check for 'q' key-press
                if key == ord("q"):
                  #if 'q' key-pressed break out
                  break
            elif frame_number > self.stop:
                frame_number = self.start

        cap.release()
        cv2.destroyAllWindows()
        
    def dropdown_eventhandler(self, change):
        
        reach = change.new
        reach = reach.split('-')
        self.current_reach = int(reach[0])
        self.start = int(reach[1])
        self.stop = int(reach[2])
        self.Plot()
        self.Vopen()
        
        self.label_reach = self.radiobuttons.value
        self.mean_df.loc[self.current_reach,'group'] = self.label_reach
        self.std_df.loc[self.current_reach,'group'] = self.label_reach


    def radio_click(self, change):
        
        self.label_reach = self.radiobuttons.value
        self.mean_df.loc[self.current_reach,'group'] = self.label_reach
        self.std_df.loc[self.current_reach,'group'] = self.label_reach
        
   
    
    def on_click(self, sender):
        
        self.reach_list_df['category'] = self.mean_df['group']
        self.reach_list_df['peak_position'] = self.reach_list_df['start'] + self.mean_df['peak_time_x']
        self.mean_df.to_hdf(self.file2[:-3]+'_scalars.h5', key='mean')    
        self.std_df.to_hdf(self.file2[:-3]+'_scalars.h5', key='std')
        self.reach_table.to_hdf(self.file2[:-3]+'_scalars.h5', key='cleared_data')      
        self.reach_list_df.to_hdf(self.file2[:-3]+'_scalars.h5', key='reaches')
        clear_output()
        del self
        print('Data is Saved. Now you can finally plot different movement categories!')