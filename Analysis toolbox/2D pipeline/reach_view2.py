'''

Interactive tool for Viewing the timeseries for the chosen categories of reaches tracked with Anipose and reviewed with the Reach_Out package. 
This module contains the functionality to select groups of reaches (rows) and timeseries (parameters) to plot.

'''
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.ticker import FormatStrFormatter
from ipywidgets import VBox, HBox
import ipywidgets as widgets
from IPython.display import display, clear_output
from tkinter import *
from tkinter.filedialog import askopenfilename
from scipy.signal import find_peaks

class TimeSeriesViewer:
    
    def __init__(self):
    
        # open file 
        root = Tk()
        root.update()
        file = askopenfilename(filetypes =[('DataTable Files', '*_scalars.h5')])
        root.destroy() 
        
        
        # initiate layout
        style = {'description_width': 'initial'}
        self.label_layout = widgets.Layout(display='flex-grow', flex_flow='column', align_items='center', width='100%')
        self.layout_hidden = widgets.Layout(visibility='hidden', display='none')
        self.layout_visible = widgets.Layout(visibility='visible', display='inline-flex')
        self.box_layout = widgets.Layout(display='inline-flex',
                                         justify_content='center',
                                         height='100%',
                                         align_items='center')


        # interactive widgets
        self.clear_button = widgets.Button(description='Clear Output', disabled=False, tooltip='Close Cell Output')

        self.checked_list = widgets.Select(options=[], description='Group to Plot', style=style,
                                                   continuous_update=False, disabled=False, layout=self.label_layout)
        self.checked_list2 = widgets.Select(options=['All projections', 'dX, dY, dZ', 'Speed, Acceleration, Jerk'], description='Parameters to plot', style=style,
                                                   continuous_update=False, disabled=False, layout=self.label_layout)
        self.lists = HBox([self.checked_list, self.checked_list2], layout=self.box_layout)
        

        self.ui_tools = VBox([self.clear_button, self.lists], layout=self.box_layout)

        # initialize event listeners
        self.checked_list.observe(self.on_column_select, names='value')
        self.clear_button.on_click(self.on_clear)
        
        # load dataframes
        self.mean_df=pd.read_hdf(file, key='mean')    
        self.std_df=pd.read_hdf(file, key='std')
        self.table=pd.read_hdf(file, key='cleared_data')
        self.reach_list_df=pd.read_hdf(file, key='reaches')
        self.reach_all=[]

        # selecting and aligning reaches based on positions entered during tracking_split and saved in the h5 file 
        for row in self.reach_list_df.iterrows():
            start = row[1]['start']
            end = row[1]['stop']
            temp_table = self.table[start:end]
            self.reach_all.append(temp_table)
            #peaks,_ = find_peaks(temp_table.jerk, height=0)             # the following two lines align the reaches using the jerk peaks
            #self.reach_all.append(temp_table.iloc[peaks[0]:])
    
        # list the options for the plot
        self.checked_list.options = self.mean_df.group.unique()

    
    def plot_series(self):
        # select data to plot
        selected_cols = self.checked_list.value
        unique_groups = self.checked_list2.value
        nums=list(self.mean_df[self.mean_df['group']==selected_cols].index)
        reach_chosen = [self.reach_all[i] for i in nums]
        
        # plot series depending on the choice
        
        if unique_groups == 'Speed, Acceleration, Jerk':                #plot layout to see the displacement and its 3 derivatives
            fig = plt.figure(figsize=(10,10))
            gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1])
            ax = fig.add_subplot(gs[0,0])
            ax2 = fig.add_subplot(gs[0,1])
            ax3 = fig.add_subplot(gs[1,0])
            ax4 = fig.add_subplot(gs[1,1])
            ax.set_ylabel('dE, mm')
            ax2.set_ylabel('velocity, mm/sec')
            ax3.set_ylabel('acceleration, mm/sec2')
            ax4.set_ylabel('jerk, mm/sec3')

            sizes=[reach_chosen[a].shape[0] for a in range(len(reach_chosen))]  #
            max_index =  sizes.index(max(sizes))        # sizes table contains the length of all reaches

            dE = pd.DataFrame(reach_chosen[max_index]['dE'].reset_index(drop=True).rename(max_index))              #make dataframes for every parameter to plot/analyze
            vel = pd.DataFrame(reach_chosen[max_index]['velocity'].reset_index(drop=True).rename(max_index))        # if you need to work with the data - export these tables
            acc = pd.DataFrame(reach_chosen[max_index]['acceleration'].reset_index(drop=True).rename(max_index))
            jrk = pd.DataFrame(reach_chosen[max_index]['jerk'].reset_index(drop=True).rename(max_index))

            for i in range(len(reach_chosen)):                                  # iteratively plot data for every reach and then the mean data in red
                
                e = reach_chosen[i]['dE'].reset_index(drop=True).rename(i)
                v = reach_chosen[i]['velocity'].reset_index(drop=True).rename(i)
                a = reach_chosen[i]['acceleration'].reset_index(drop=True).rename(i)
                j = reach_chosen[i]['jerk'].reset_index(drop=True).rename(i)
                
                if not i == max_index: 
                    
                    dE=pd.merge(dE,e, how='left', left_index=True, right_index=True)
                    vel=pd.merge(vel,v, how='left', left_index=True, right_index=True)
                    acc=pd.merge(acc,a, how='left', left_index=True, right_index=True)
                    jrk=pd.merge(jrk,j, how='left', left_index=True, right_index=True)
                
                plt1 = ax.plot(e, color='grey')
                plt2 = ax2.plot(v, color='grey')
                plt3 = ax3.plot(a, color='grey') 
                plt4 = ax4.plot(j, color='grey')    

            plt1 = ax.plot(dE.mean(axis=1), color='red', linewidth=4)
            plt2 = ax2.plot(vel.mean(axis=1), color='red', linewidth=4)
            plt3 = ax3.plot(acc.mean(axis=1), color='red', linewidth=4) 
            plt4 = ax4.plot(jrk.mean(axis=1), color='red', linewidth=4)

            ax2.yaxis.tick_right()
            ax2.yaxis.set_label_position("right")
            ax4.yaxis.tick_right()
            ax4.yaxis.set_label_position("right")
            
        elif unique_groups == 'All projections':                        #plot layout to see the coordinate change in all projections + 3d
            number = len(reach_chosen)                                  # type in the number of reaches, for maximum type len(reach_chosen)
            n_list = [0, 10, 20, 30, 40]
            n_list_2 =['0', '100', '200', '300', '400ms']
            fig = plt.figure(figsize=(10,10))
            gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1])
            ax = fig.add_subplot(gs[0,0], projection='3d')
            ax2 = fig.add_subplot(gs[0,1])
            ax3 = fig.add_subplot(gs[1,0])
            ax4 = fig.add_subplot(gs[1,1])
            ax.set_xlabel('X, mm')
            ax.set_ylabel('Y, mm')
            ax.set_zlabel('Z, mm')
            ax2.set_ylabel('X, mm')
            ax3.set_ylabel('Y, mm')
            ax4.set_ylabel('Z, mm')
            ax.set_title('3D view')         
            ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
            #ax.invert_zaxis()
            #ax2.invert_yaxis()
            ax3.invert_yaxis()
            #ax4.invert_yaxis()
            ax2.set_title('Forward motion')
            ax3.set_title('Sideward motion')
            ax4.set_title('Upward motion')
            #ax2.set_xlim([0,40])
            #ax2.set_xticks(ticks=n_list)
            #ax2.set_xticklabels(labels=n_list_2)
            sizes=[reach_chosen[a].shape[0] for a in range(number)]
            max_index =  sizes.index(max(sizes))    # sizes table contains the length of all reaches
            dX = pd.DataFrame(reach_chosen[max_index]['finger1_x'].reset_index(drop=True).rename(max_index))        #make dataframes for every parameter to plot/analyze
            dY = pd.DataFrame(reach_chosen[max_index]['finger1_y'].reset_index(drop=True).rename(max_index))
            dZ = pd.DataFrame(reach_chosen[max_index]['finger1_z'].reset_index(drop=True).rename(max_index))


            for i in range(number):                                      # iteratively plot data for every reach and then the mean data in red
                
                x = reach_chosen[i]['finger1_x'].reset_index(drop=True).rename(i)
                y = reach_chosen[i]['finger1_y'].reset_index(drop=True).rename(i)
                z = reach_chosen[i]['finger1_z'].reset_index(drop=True).rename(i)                
                
                
                plt1 = ax.plot(x,y,z, linewidth=1, color='grey', label='open')
                plt2 = ax2.plot(x, color='grey')
                plt3 = ax3.plot(y, color='grey') 
                plt4 = ax4.plot(z, color='grey')
                

                if not i == max_index: 
                    
                    dX=pd.merge(dX,x, how='left', left_index=True, right_index=True)
                    dY=pd.merge(dY,y, how='left', left_index=True, right_index=True)
                    dZ=pd.merge(dZ,z, how='left', left_index=True, right_index=True)
                

            plt1 = ax.plot(dX.mean(axis=1),dY.mean(axis=1),dZ.mean(axis=1), color='black', label='open', linewidth=4)
            plt2 = ax2.plot(dX.mean(axis=1), color='black', linewidth=4)
            plt3 = ax3.plot(dY.mean(axis=1), color='black', linewidth=4) 
            plt4 = ax4.plot(dZ.mean(axis=1), color='black', linewidth=4)
            
            
            #ax2.yaxis.tick_right()
            #ax2.yaxis.set_label_position("right")
            #ax4.yaxis.tick_right()
            #ax4.yaxis.set_label_position("right")

            
        elif unique_groups == 'dX, dY, dZ':                         #plot layout to see the frame by frame displacement in all projections 
            fig = plt.figure(figsize=(10,10))
            gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1])
            ax = fig.add_subplot(gs[0,0])
            ax2 = fig.add_subplot(gs[0,1])
            ax3 = fig.add_subplot(gs[1,0])
            ax4 = fig.add_subplot(gs[1,1])
            ax.set_ylabel('dE, mm')
            ax2.set_ylabel('dx, mm')
            ax3.set_ylabel('dy, mm')
            ax4.set_ylabel('dz, mm')
            sizes=[reach_chosen[a].shape[0] for a in range(len(reach_chosen))]
            max_index =  sizes.index(max(sizes))        # sizes table contains the length of all reaches
            dE = pd.DataFrame(reach_chosen[max_index]['dE'].reset_index(drop=True).rename(max_index))       #make dataframes for every parameter to plot/analyze
            dX = pd.DataFrame(reach_chosen[max_index]['dx'].reset_index(drop=True).rename(max_index))
            dZ = pd.DataFrame(reach_chosen[max_index]['dz'].reset_index(drop=True).rename(max_index))
            dY = pd.DataFrame(reach_chosen[max_index]['dy'].reset_index(drop=True).rename(max_index))

            for i in range(len(reach_chosen)):                                   # iteratively plot data for every reach and then the mean data in red
                e = reach_chosen[i]['dE'].reset_index(drop=True).rename(i)
                x = reach_chosen[i]['dx'].reset_index(drop=True).rename(i)
                z = reach_chosen[i]['dz'].reset_index(drop=True).rename(i)
                y = reach_chosen[i]['dy'].reset_index(drop=True).rename(i)
                if not i == max_index: 
                    dE=pd.merge(dE,e, how='left', left_index=True, right_index=True)
                    dX=pd.merge(dX,x, how='left', left_index=True, right_index=True)
                    dZ=pd.merge(dZ,z, how='left', left_index=True, right_index=True)
                    dY=pd.merge(dY,y, how='left', left_index=True, right_index=True)
                
                plt1 = ax.plot(e, color='grey')
                plt2 = ax2.plot(x, color='grey')
                plt3 = ax3.plot(y, color='grey') 
                plt4 = ax4.plot(z, color='grey')    

            plt1 = ax.plot(dE.mean(axis=1), color='red', linewidth=4)
            plt2 = ax2.plot(dX.mean(axis=1), color='red', linewidth=4)
            plt3 = ax3.plot(dY.mean(axis=1), color='red', linewidth=4) 
            plt4 = ax4.plot(dZ.mean(axis=1), color='red', linewidth=4)

            ax2.yaxis.tick_right()
            ax2.yaxis.set_label_position("right")
            ax4.yaxis.tick_right()
            ax4.yaxis.set_label_position("right")
            
        else:
            print('No projection to plot chosen!')
            fig = plt.figure(figsize=(10,10))
            gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1])
            ax = fig.add_subplot(gs[0,0], projection='3d')
            ax2 = fig.add_subplot(gs[0,1])
            ax3 = fig.add_subplot(gs[1,0])
            ax4 = fig.add_subplot(gs[1,1])
    
    def on_clear(self, b=None):
        '''
        Clears the display and memory.

        Parameters
        ----------
        b (button Event): Ipywidgets.Button click event.

        Returns
        -------
        '''

        clear_output()
        del self

    def on_column_select(self, event=None):
        '''
        Updates the view once the user selects a new group of reaches to plot.

        Parameters
        ----------
        event

        Returns
        -------
        '''

        clear_output()
        display(self.ui_tools)
        self.plot_series()