# -*- coding: utf-8 -*-
"""
Created on Mon May 16 11:33:55 2022

@author: Daniil.Berezhnoi
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

directory = 'C:/Users/Daniil.Berezhnoi/Downloads/6-OHDA locomotion - Test 307/' 

for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        #Opening the file as a table
        name = directory + filename
        table = pd.read_csv(name)
        
        
        #Doing required operations with the table
        dx = table['Centre position X'] - table['Centre position X'].shift(1)
        dy = table['Centre position Y'] - table['Centre position Y'].shift(1)
        table['speed'] = np.sqrt(dx**2 + dy**2)
        table['SMA100'] = table['speed'].rolling(100).mean()
        table['SMS100'] = table['speed'].rolling(100).sum()
        #table.dropna(inplace=true)
        
        #Drawing and Saving the plots
        plt.figure(figsize=(8, 6), dpi=80)
        plt.subplot(2,1,1)
        table.loc[101::100,'SMS100'].plot(title = filename, kind = 'hist', bins = 20, range = (0, 600), xlabel = 'Distance/5sec', ylabel = 'Number of epochs', ax = plt.gca())
        plt.subplot(2,1,2)
        table.loc[101::100,['SMA100','SMS100']].plot(xlabel = 'Time (x 10sec)', ylabel = 'Distance', ax = plt.gca())
        
        #Saving the table back to csv
        plt.savefig(name[0:-4])
        plt.close()
        table.to_csv(name, encoding ='utf-8', index = False)