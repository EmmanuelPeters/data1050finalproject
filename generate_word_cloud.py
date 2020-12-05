from os import path
from PIL import Image
import numpy as np
import os
from scipy.ndimage import gaussian_gradient_magnitude
from wordcloud import WordCloud, STOPWORDS
import plotly.express as px
from skimage import io

# Replace path here by the linker to Mongdb
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
text = open(path.join(d, 'twitter.txt')).read()

def generate_word_cloud(text): 
    # read the mask image
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    twitter_image = np.array(Image.open(path.join(d, "twitter_mask.png")))
    
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


if __name__ == '__main__':
    fig = generate_word_cloud(text)
    fig.show()
