# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 15:53:22 2021

@author: berez
"""

import numpy
import pandas
import matplotlib.pyplot as plt
import os
import csv

directory = 'C:/Users/LACS/Desktop/mice/video'
name = directory + '/tracks.txt'
header = ['filenames','tracklength','likelihood']

with open(name, 'w', newline = '') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(header)
    
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            table = pandas.read_csv(os.path.join(directory,filename), header=2,usecols=[0,1,2,3])
            table.loc[table['likelihood'] < 0.5, 'x'] = table['x'].shift(1)
            table.loc[table['likelihood'] < 0.5, 'y'] = table['y'].shift(1)
            dx = table['x'] - table['x'].shift(1)
            dy = table['y'] - table['y'].shift(1)
            table['speed'] = numpy.sqrt(dx**2 + dy**2)
            table.loc[table['speed'] > 50, 'speed'] = 0
            means = table.likelihood.mean()
            table.drop(table.index[table.likelihood<0.5], inplace=True)
            
            plt.figure(figsize=(10,10))
            plt.scatter(table['x'], table['y'], c=table['speed'])
            plt.plot(table['x'], table['y'])
            plt.xlabel('pos_x')
            plt.ylabel('pos_y')
            plt.title(table['speed'].sum())
            plt.savefig(filename[0:-4])

            data = [filename[0:-4], str(table['speed'].sum()), means]            
            wr.writerow(data)
            
        