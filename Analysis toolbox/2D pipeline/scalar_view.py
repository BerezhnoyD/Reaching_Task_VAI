'''

Interactive tool for Viewing Main Scalar parameters for all the reaches tracked with Anipose and reviewed with the Reach_Out package. This module contains the functionality to select groups of reaches (rows) and scalar parameters (columns) to plot the mean and variation for all groups.

'''
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from ipywidgets import VBox, HBox
import ipywidgets as widgets
from IPython.display import display, clear_output
from tkinter import *
from tkinter.filedialog import askopenfilename


class InteractiveScalarViewer:

    def __init__(self):
        '''
        Initialization function that will compute the scalar dataframe, the mean and standard deviation
         in preparation to plot the default interactive plotly scalar summary.
        
        '''
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

        self.checked_list = widgets.SelectMultiple(options=[], description='Scalar Columns to Plot', style=style,
                                                   continuous_update=False, disabled=False, layout=self.label_layout)
        self.checked_list2 = widgets.SelectMultiple(options=[], description='Groups to Plot', style=style,
                                                   continuous_update=False, disabled=False, layout=self.label_layout)
        self.lists = HBox([self.checked_list, self.checked_list2], layout=self.box_layout)
        

        self.ui_tools = VBox([self.clear_button, self.lists], layout=self.box_layout)

        # initialize event listeners
        self.checked_list.observe(self.on_column_select, names='value')
        self.clear_button.on_click(self.on_clear)
        
        
        # get scalar dataframes
        self.mean_df = pd.read_hdf(file, key='mean')
        self.std_df = pd.read_hdf(file, key='std')
        self.colors = px.colors.qualitative.Alphabet

        # populate column selector
        self.checked_list.options = list(self.mean_df.columns)
        self.checked_list2.options = self.mean_df.group.unique()
        
        
        # set default values
        self.checked_list.value = ['duration_sec', 'dx_mm']
        self.checked_list2.value = [self.checked_list2.options[0], self.checked_list2.options[1]] 
        
    def make_graphs(self):
        '''
        Creates a 2 column plotly figure where the left column corresponds to the mean of the selected scalar,
         and the right column corresponds to the standard deviation of the scalars.

         Each selected scalar will be plotted in a new row containing violin + swarm plots for all the groups
          found in the scalar dataframe. Users can click on the legend items to hide selected groups from the display.

        Returns
        -------
        '''

        selected_cols = self.checked_list.value
        unique_groups = self.checked_list2.value
        

        self.fig = make_subplots(rows=len(selected_cols), cols=2)

        for j, c in enumerate(selected_cols):
            for i, g in enumerate(sorted(unique_groups)):
                y = self.mean_df[self.mean_df['group'] == g][c]
                std_y = self.std_df[self.std_df['group'] == g][c]

                session_name = self.mean_df[self.mean_df['group'] == g].index.values.tolist()
                

                texts = [f'SessionName: {sn}' for sn in
                         list(session_name)]

                show = j < 1

                v1 = go.Violin(y=y,
                               name=g,
                               jitter=0.5,
                               line_color=self.colors[i],
                               marker=dict(size=5),
                               line=dict(width=1),
                               points='all',
                               text=texts,
                               legendgroup=g,
                               showlegend=show,
                               hovertemplate=f'Mean {c}: ' + "%{y}<br>%{text}"
                               )

                self.fig.add_trace(v1, row=j + 1, col=1)

                self.fig.update_yaxes(title_text=f"{c}", row=j + 1, col=1)

                v2 = go.Violin(y=std_y,
                               name=g,
                               jitter=0.5,
                               line_color=self.colors[i],
                               marker=dict(size=5),
                               line=dict(width=1),
                               points='all',
                               text=texts,
                               legendgroup=g,
                               showlegend=False,
                               hovertemplate=f'Variance {c}: ' + "%{y}<br>%{text}"
                               )

                self.fig.add_trace(v2, row=j + 1, col=2)

        self.fig.update_xaxes(title_text=f"Mean", row=len(selected_cols), col=1)
        self.fig.update_xaxes(title_text=f"STD", row=len(selected_cols), col=2)
        self.fig.update_xaxes(tickangle=45)

        self.fig.update_layout(height=300*len(selected_cols), width=1000, title_text="Scalar Summary")
        self.fig.update_traces(box_visible=True, meanline_visible=True)

        return self.fig

    def interactive_view(self):
        '''
        Displays the interactive plotly graph. Regularly called from self.on_column_select().

        Returns
        -------
        '''
        
        # https://plotly.com/python/configuration-options/#customizing-download-plot-options
        plotly_config = {
            'toImageButtonOptions': {
                'format': 'svg', # one of png, svg, jpeg, webp
                'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
                }
            }
        fig = self.make_graphs()
        fig.show(config=plotly_config)
        
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
        Updates the view once the user selects a new set of scalars to plot.

        Parameters
        ----------
        event

        Returns
        -------
        '''

        clear_output()
        display(self.ui_tools)
        self.interactive_view()