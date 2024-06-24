# PROGRAM FOR CLUSTERING THE REACHES AND ASSIGNING NEW LABELS BASED ON CLUSTERING
# Input - _scalars.h5 file containing list of reaches, cleared data table, list of mean and std values for all the parameters/all reaches
# Output - modified  _scalars.h5 file with new labels assigned based on clustering
# columns = ['maxX_mm','minY_mm','maxZ_mm']

from tkinter import *
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import math
from sklearn.cluster import DBSCAN, MeanShift, estimate_bandwidth, KMeans, AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from matplotlib import colors as mcolors
from sklearn import metrics
import ipywidgets as widgets
pd.options.mode.chained_assignment = None  # default='warn'

class Cluster_Analysis:

    def __init__(self, columns: list, eps = 1.0, clusters = 4, samples = 500, distance = 40):
        
        #open file
        root = Tk()
        root.update()
        self.name = askopenfilename(filetypes =[('Scalar Dataframe Files', '*.h5')])
        root.destroy()
        
        self.mean_df = pd.read_hdf(self.name, key='mean')
        self.std_df = pd.read_hdf(self.name, key='std')
        self.reach_table = pd.read_hdf(self.name, key='cleared_data')
        self.reach_list_df = pd.read_hdf(self.name, key='reaches')
        
        self.mean_df1 = self.mean_df[columns]
        self.mean_df_scaled = StandardScaler().fit_transform(self.mean_df[columns])
        self.options = list(['Manual','DBSCAN','MeanShift','K-Means','Agglomerative'])
        
        #put the default options in
        self.eps = eps
        self.clusters = clusters
        self.samples = samples
        self.distance = distance
        
        
        
        self.dropdown = widgets.Select(
                                options=[' ']+self.options,
                                description='Method:',
                                
            )
            
        self.button = widgets.Button(description="Save with new labeling"
        )
        
        self.box=widgets.HBox([self.dropdown, self.button])
        self.button.on_click(self.on_click)
        self.dropdown.observe(self.dropdown_eventhandler, names='value')
        display(self.box) 
            
        self.fig = plt.figure(figsize=(10,10))
        self.fig2 = plt.figure(figsize=(10,10))


        
            
    def make_plots(self, method: str):

        self.method = method
        
        if self.method=='Manual':
            clusters=self.mean_df['group'].nunique()
            dic = {self.mean_df['group'].unique()[0]:0,
                   self.mean_df['group'].unique()[1]:1,
                   self.mean_df['group'].unique()[2]:2,
                   self.mean_df['group'].unique()[3]:3,
                   self.mean_df['group'].unique()[4]:4,
                   }
            self.mean_df['group'] = self.mean_df['group'].map(dic)  
            self.mean_df1['group'] = self.mean_df['group'].copy()               
            noise = 0
        
        elif self.method=='DBSCAN':
            db = DBSCAN(eps=self.eps, min_samples=20).fit(self.mean_df_scaled)                  #This parameters should be changed to fit your sample see https://scikit-learn.org/
            labels = db.labels_
            self.mean_df['group'] = labels
            self.std_df['group'] = labels
            self.mean_df1.loc[:,'group'] = self.mean_df['group'].copy()    
            
            # Number of clusters in labels, ignoring noise if present.
            clusters = len(set(labels)) - (1 if -1 in labels else 0)
            noise = list(labels).count(-1)
        
        
        elif self.method=='MeanShift':
            bandwidth = estimate_bandwidth(self.mean_df_scaled, quantile=0.3, n_samples=self.samples)  #This parameters should be changed to fit your sample see https://scikit-learn.org/
            ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
            ms.fit(self.mean_df_scaled)
            labels = ms.labels_
            self.mean_df['group'] = labels
            self.std_df['group'] = labels
            self.mean_df1.loc[:,'group'] = self.mean_df['group'].copy()    
            
            # Number of clusters in labels, ignoring noise if present.
            clusters = len(set(labels)) - (1 if -1 in labels else 0)
            noise = list(labels).count(-1)
        
        elif self.method=='K-Means':                                                            #This parameters should be changed to fit your sample see https://scikit-learn.org/
            km = KMeans(n_clusters=self.clusters)
            km.fit(self.mean_df_scaled)
            labels = km.labels_
            self.mean_df['group'] = labels
            self.std_df['group'] = labels
            self.mean_df1.loc[:,'group'] = self.mean_df['group'].copy()  
            
            # Number of clusters in labels, ignoring noise if present.
            clusters = len(set(labels)) - (1 if -1 in labels else 0)
            noise = list(labels).count(-1)
        
        elif self.method=='Agglomerative':
            ac = AgglomerativeClustering(linkage='ward', n_clusters=None, 
                                 compute_full_tree=True, distance_threshold=self.distance, compute_distances=True)  #This parameters should be changed to fit your sample see https://scikit-learn.org/
            ac.fit(self.mean_df_scaled)
            labels = ac.labels_
            self.mean_df['group'] = labels
            self.std_df['group'] = labels
            self.mean_df1.loc[:,'group'] = self.mean_df['group'].copy()    
            
            # Number of clusters in labels, ignoring noise if present.
            clusters = len(set(labels)) - (1 if -1 in labels else 0)
            noise = list(labels).count(-1)
        
        else:
            pass
     
     
     
        sil_metr = metrics.silhouette_score(self.mean_df_scaled, self.mean_df['group'], metric='euclidean')
        ch_metr = metrics.calinski_harabasz_score(self.mean_df_scaled, self.mean_df['group'])
        
        
        colors = list(zip(*sorted((
                        tuple(mcolors.rgb_to_hsv(
                              mcolors.to_rgba(color)[:3])), name)
                         for name, color in dict(
                                mcolors.BASE_COLORS, **mcolors.CSS4_COLORS
                                                          ).items())))[1]
        skips = math.floor(len(colors[5 : -5])/clusters)
        cluster_colors = colors[5 : -5 : skips]
        
        l = self.mean_df1.columns.values
        number_of_columns = 3
        number_of_rows = math.floor(len(l)/number_of_columns)
        
        
        self.fig.clf()
        self.fig.suptitle('Method: ' + self.method + '   Clusters: %.0f   Noise: %.0f   Silhouette score: %.2f    Variance Ratio: %.2f' % (clusters, noise, sil_metr, ch_metr), fontsize=16)
        self.ax1 = self.fig.add_subplot(projection='3d')
        self.ax1.scatter(self.mean_df_scaled[:,0], self.mean_df_scaled[:,1], self.mean_df_scaled[:,2], c = list(map(lambda label : cluster_colors[label],
                                                self.mean_df['group'])))
                                                
        
        self.fig2.clf()
                
        for i in range(0,len(l)-1):
            self.fig2.add_subplot(number_of_rows+1,number_of_columns, i+1)
            sns.set_style('whitegrid')
            data=self.mean_df1[[l[i],l[3]]]
            data.loc[:,'key']=l[i]
            ax=sns.stripplot(data=data, x='key', y=l[i], hue=l[3], dodge=True, orient='v')
            ax.set(xlabel='', ylabel='')
            plt.legend([],[], frameon=False)
            plt.subplots_adjust(wspace=1.0)
        
    
    def dropdown_eventhandler(self, change):
        
        method = change.new
        self.make_plots(method)

   
    
    def on_click(self, sender):
    
        self.mean_df.to_hdf(self.name[:-3]+'_clustered.h5', key='mean')    
        self.std_df.to_hdf(self.name[:-3]+'_clustered.h5', key='std')
        self.reach_table.to_hdf(self.name[:-3]+'_clustered.h5', key='cleared_data') 
        self.reach_list_df.to_hdf(self.name[:-3]+'_clustered.h5', key='reaches')