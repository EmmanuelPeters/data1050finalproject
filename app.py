'''This Module contains the web application'''

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import plotly.express as px
from os import path
from PIL import Image
import numpy as np
import os
from scipy.ndimage import gaussian_gradient_magnitude
from wordcloud import WordCloud, STOPWORDS
from skimage import io
from generate_word_cloud import generate_word_cloud
from predict_percent_visualization import percentage_visualization


# Definitions of page style constants. Any external CSS stylesheets can go here as well.
COLORS = ['rgb(255, 255, 255)', 'rgb(29, 161, 242)', 'rgb(27, 40, 54)', 'rgb(255, 255, 54)']
external_stylesheets = ['/assets/style.css']

# Define DASH app
app = dash.Dash(__name__)


# Define componet functions.


def page_header():
    '''
    The page header is returned as a DASH 'html.div'
    '''
    return html.Div(id='header',
                    children=[html.Div([html.H3('Visualization with datashader and Plotly')], className="ten columns"),
                              html.A([html.Img(id='logo',
                                               src=app.get_asset_url('twitter_logo.png'),
                                               style={'height': '35px', 'paddingTop': '10%'})],
                                     className="two columns row",
                                     href='https://github.com/EmmanuelPeters/data1050finalproject')], 
                    className="row")        

# Primary text area.
def description():
    '''
    Project description is returned in markdown
    '''
    return html.Div(children=[dcc.Markdown('''
        # Tweet Storm
        Capturing the “taste” of the population has both scientific and commercial value. Knowing what idea 
        or product will be popular in the future can give people important information 
        for decision making. Tweeter is a very good place to learn about people’s preferences 
        because it has a huge amount of users and each user’s tweet will reflect what they like and don’t like
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")

# Allowed input types for site user limited to text and numbers only.                              
# ALLOWED_TYPES = ("text", "number")
                              
# DASH function for user input.
# app.layout = html.Div([html.H6("Enter your Tweet!"),
#                        html.Div(["Input: ", dcc.Input(id='keyword', value='input keyword', type='text')]),
#                        html.Br(), html.Div(id='text')])

# Sequentially add page components to the app's layout
def dynamic_layout():
    return html.Div([
        page_header(),
        html.Hr(),
        description(),
    ], className='row', id='content')

# set layout to a function which updates upon reloading
app.layout = dynamic_layout

# @app.callback(Output(component_id='text', component_property='children'),
#               Input(component_id='keyword', component_property='value'))



if __name__ == '__main__':
    app.run_server(debug=True, port=1050, host='0.0.0.0')