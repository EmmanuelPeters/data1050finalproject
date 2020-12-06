from os import path
from PIL import Image
import numpy as np
import os
from scipy.ndimage import gaussian_gradient_magnitude
from wordcloud import WordCloud, STOPWORDS
from plotly import express as px, graph_objects as go
from skimage import io
from database import fetch_all_as_time_series
COLORS = ['rgb(50, 255, 50)', 'rgb(29, 161, 242)', 'rgb(230, 230, 230)', 'rgb(255, 255, 54)']


# Generate a small animation based on the prediction result `perc`
# The detailed layout should be tuned based on the choose DASH app
def percentage_visualization(perc):
    '''the `perc` is the result of previous likelihood prediction based on user's input Tweets'''
    interval = 20
    Nframe = int(perc / interval)
    increase_list = np.linspace(0, perc, Nframe + 1)
    x_list = []
    likelihood = []
    for i in range(Nframe):
        x_list.append("Tweets")
        likelihood.append(i * interval)
    x_list.append("Tweets")
    likelihood.append(perc)
    fig = px.bar(x = x_list, y = likelihood, animation_frame=increase_list, range_y = [0, 100]) 
    return fig


def generate_word_cloud(text): 
    # read the mask image
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    twitter_image = np.array(Image.open(path.join(d, "assets", "twitter_mask.png")))
    # create mask  white is "masked out"
    twitter_mask = twitter_image.copy()
    twitter_mask[twitter_mask.sum(axis=2) == 0] = 255
    # some finesse: we enforce boundaries between colors so they get less washed out.
    # For that we do some edge detection in the image
    edges = np.mean([gaussian_gradient_magnitude(twitter_mask[:, :, i] / 255., 2) for i in range(3)], axis=0)
    twitter_mask[edges > .08] = 255
    # the build-in STOPWORDS list will be used, we could more STOPWORDS here.
    stopwords = set(STOPWORDS)
    wc = WordCloud(background_color="white", max_words=2000, mask=twitter_mask,
               stopwords=stopwords, contour_width=3, contour_color='steelblue')
    # generate word cloud
    twitter_wc = wc.generate(text)
    fig = px.imshow(twitter_wc)
    fig.update_yaxes(visible=False)
    fig.update_xaxes(visible=False)
    return fig
    
    
def keywords_frequencies_graph(stack=False):
    """
    Returns scatter line plot the frequencies of all keywords.
    If `stack` is `True`, all frequencies are stacked together.
    """
    kw_freq = fetch_all_as_time_series(allow_cached=False)
    if kw_freq is None:
        return go.Figure()
    keywords = list(kw_freq.keys())
    fig = go.Figure()
    for i, k in enumerate(keywords):
        fig.add_trace(go.Scatter(x=kw_freq[k]['timestamps'],
                                 y=kw_freq[k]['frequencies'], mode='lines', name=k,
                                 line={'width': 2, 'color': COLORS[i]},
                                 stackgroup='stack' if stack else None))
    title = 'Keywords Frequencies from Twitter'
    if stack:
        title += ' [Stacked]'
    fig.update_layout(template='plotly_dark',
                      title=title,
                      plot_bgcolor='#23272c',
                      paper_bgcolor='#23272c',
                      yaxis_title='count/thousand',
                      xaxis_title='Date/Time')
    return fig
    
    
if __name__ == '__main__':
    fig = keywords_frequencies_graph()
    fig.show()