The folder contains all the analysis scripts and single Jupyter Notebook to run them
all sequentially. 
Files:
ReachOut-Analysis.ipynb    	- Notebook you need to run the tracking part
ReachOut-Tracking.ipynb    	- Notebook you need to run the manual analysis part 
ReachOut-Visualization.ipynb    - Notebook you need to run the visualization part
coord_correct.py	   - Scripts to correct the Anipose Dataframe to fit the specified XY axis (part of the Anipose Toolbox)	
reach_view.py		   - Class to Visualize the trajectories for the selected reaches
scalar_view.py		   - Class to Visualize the scalar parameters for the selected reaches 
tracking_split.py	   - Class to Analyze the 2d tracking data and select the parts of the track
tracking_split_automatic.py- Class to automatically detect peaks and select the parts of the track
video_split.py		   - Scripts to Prepare the video for tracking
video_split_folder.py	   - Scripts to Prepare the video for tracking (works with a whole folder)
viewer.py		   - Class to Analyze the 3d tracking data and annotate preselected reaches
clustering.py		   - Class to Cluster preselected reaches

For the scripts to work you need to install DEEPLABCUT Anaconda environment
with minor changes, that is provided in the folder one up.

DEEPLABCUT.yml		   - Anaconda Environment with all the dependencies needed + Anipose lib included
