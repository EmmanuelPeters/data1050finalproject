'''This Module contains the web application'''

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objects as go


# Definitions of page style constants. Any external CSS stylesheets can go here as well.
COLORS = ['rgb(255, 255, 255)', 'rgb(29, 161, 242)', 'rgb(27, 40, 54)', 'rgb(255, 255, 54)']


# Define DASH app



# Define componet functions.

def page_header():
    '''
    The page header is returned as a DASH 'html.div'
    '''
    
    return html.Div(id='header', children = [
        html.Div([html, H4('Tweet Storm')],
                 
        html.A([html.Img(id='twitter_logo', src=app.get_asset_url('twitter_logo.png'),
                         style={'height': '35px', 'paddingTop': '10%'})],
               

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
        ''',)
                              
# Word cloud visualization function
                              
def word_cloud():
                             
                              
                              