import numpy as np
import pandas as pd
from scipy import signal
import plotly
import plotly.graph_objs as go
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = '14'


def rndmtx():
    """Generate random 2d-array as a digital elevation model."""

    nx = 120
    ny = 120
    np.random.seed(55) #zo geen variatie meer!! 
    dem1 = np.random.rand(nx, ny)
    # Save array to csv file befor Gaussian filter.
    # Comment the next two lines if reading from the csv file.
    dafr = pd.DataFrame(dem1)
    dafr.to_csv('G_dem1.csv', header=False, index=False)

    # Uncomment the next two lines to read from csv file.
    # dafr = pd.read_csv('G_dem1.csv', header=None)
    # dem1 = dafr.values

    # Apply the first Gaussian filter.
    sizex = 7  # The less sizex and sizey the more highlands.
    sizey = 7  # The more sizex and sizey the more water.
    x, y = np.mgrid[-sizex:sizex+1, -sizey:sizey+1]
    scale = 0.33  # The more scale the bigger the difference in elevation.
    g = np.exp(-scale*(x**2/sizex+y**2/sizey))
    filter1 = g/g.sum()  # Normalise the Gaussian function.

    dem_smooth = signal.convolve(dem1, filter1, mode='valid')
    # Rescale so it lies between 0 and 1.
    dem_smooth = 5*((dem_smooth - dem_smooth.min())
                  / (dem_smooth.max() - dem_smooth.min()))

    # Apply the second Gaussian filter to make the boundaries smoother.
    sizex = 7
    sizey = 7
    x, y = np.mgrid[-sizex:sizex+1, -sizey:sizey+1]
    g = np.exp(-0.33*(x**2/sizex+y**2/sizey))
    filter2 = g/g.sum()

    dem_smooth1 = signal.convolve(dem_smooth, filter2, mode='valid')
    dem_smooth1 = 5*((dem_smooth1 - dem_smooth1.min())
                   / (dem_smooth1.max() - dem_smooth1.min()))

    return dem_smooth1

# Get the raw random array of the digital elevation model
#   and assign it to the variable.
contour_xy = rndmtx()

# Save the array into CSV file in the working directory.
df = pd.DataFrame(contour_xy)
df.to_csv('last_data.csv', header=False, index=False)

data = [
    go.Contour(
        z=contour_xy,
        colorscale=[
            [0, 'rgb(0, 161, 233)'], [0.28, 'rgb(0, 161, 233)'],
            [0.28, 'rgb(29, 210, 108)'], [0.50, 'rgb(29, 210, 108)'],
            [0.50, 'rgb(141, 232, 130)'], [0.65, 'rgb(141, 232, 130)'],
            [0.65, 'rgb(254, 254, 152)'], [0.75, 'rgb(254, 254, 152)'],
            [0.75, 'rgb(192, 182, 122)'], [0.82, 'rgb(192, 182, 122)'],
            [0.82, 'rgb(142, 110, 92)'], [0.88, 'rgb(142, 110, 92)'],
            [0.88, 'rgb(171, 147, 142)'], [0.93, 'rgb(171, 147, 142)'],
            [0.93, 'rgb(227, 219, 217)'], [0.97, 'rgb(227, 219, 217)'],
            [0.97, 'rgb(255, 255, 255)'], [1, 'rgb(255, 255, 255)']
        ],
    ),
]

layout = go.Layout(
    yaxis=dict(
        autorange='reversed'
    )
)

figure = go.Figure(data=data, layout=layout)
plotly.offline.plot(figure, filename='dem.html')

ny,nx = np.shape(contour_xy)
grid_imag = np.zeros((ny+2,nx+2))
grid_imag[1:-1,1:-1] = contour_xy

# Randen op zeeniveau (hoogte 0) om eiland te simuleren
grid_imag[:,0] = 0
grid_imag[:,-1] = 0
grid_imag[0,:] = 0
grid_imag[-1,:] = 0

plt.figure(figsize= (12,8))
plt.contourf(np.flipud(contour_xy))
plt.colorbar()
plt.xlabel('x [m]')
plt.ylabel('y [m]')
#plt.savefig('AfbeeldingenPDF/DEM_random.pdf')  #zo opslaan als PDF (beter voor overleaf!)