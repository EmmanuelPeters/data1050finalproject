import plotly.express as px
import numpy as np

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


if __name__ == '__main__':
    fig = percentage_visualization(87.6)
    fig.show()
