#making the hypothetical grid

#gaat uit van: 2 cellen op de crest even hoog, 2 cellen bij de pond even laag
import numpy as np
import matplotlib.pyplot as plt

nx = 30
ny = 20
grid = np.zeros((ny,nx))
slopex = 0.2/100
slopey = 0.1/100
deltax = 50 #m
deltay = 50 #m
xs = np.arange(deltax/2,(nx+1/2)*deltax,deltax)
ys = np.arange(deltay/2,(ny+1/2)*deltay,deltay)
#take 10 m as the lowest point
grid[-1,-1] = 10

#start by calculating the heights at the right edge
right_edge = np.arange(grid[-1,-1],grid[-1,-1]+(slopey*deltay)*ny,slopey*deltay)
grid[:,-1] = np.flip(right_edge) 


#calculate the otherpoints starting from the right edge
for j in range(ny):
    sequence1 = np.arange(grid[j,-1],grid[j,-1]+(slopex*deltax)*(8),slopex*deltax)
    sequence2 = np.arange(grid[j,-1]+(slopex*deltax)*(8),grid[j,-1]+(slopex*deltax)*(8-3),-slopex*deltax)
    sequence3 = np.arange(grid[j,-1]+(slopex*deltax)*(8-3),grid[j,-1]+(slopex*deltax)*(8-3+17),slopex*deltax)
    sequence = np.hstack([sequence1,sequence2,sequence3])
    grid[j,:] = np.flip(sequence)
plt.figure(figsize= (7.5,7.5))
plt.contourf(xs,ys,grid)
plt.colorbar()
plt.title('Contourplot of hypothetical surface')
plt.xlabel('x [m]')
plt.ylabel('y [m]')


plt.figure(figsize= (15,10))
X, Y = np.meshgrid(xs, ys)
ax = plt.axes(projection='3d')
im = ax.plot_surface(X, Y, grid, cmap = 'viridis')
plt.colorbar(im)
plt.xlabel('x [m]')
plt.ylabel('y [m]')
ax.set_zlabel('height [m]')
#plt.title('3D representation of hypothtetical surface')
plt.savefig('Afbeeldingen/3D_hypoth_terrain.png', dpi = 300)
plt.savefig('AfbeeldingenPDF/3D_hypoth_terrain..pdf')

plt.figure(figsize= (11,7))
plt.imshow(np.flipud(grid), extent = [np.min(xs)-deltax/2, np.max(xs)+deltax/2,
np.min(ys)-deltay/2,np.max(ys)+deltay/2])
plt.colorbar()
plt.annotate("Pond", xy=(875, 975), xytext=(750, 800),
            arrowprops=dict(arrowstyle="->"))
plt.annotate("CrestL", xy=(1025, 975), xytext=(950, 800),
arrowprops=dict(arrowstyle="->"))
plt.annotate("CrestR", xy=(1075, 975), xytext=(1150, 800),
arrowprops=dict(arrowstyle="->"))
#plt.title('Contourplot of hypothetical surface')
plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.savefig('Afbeeldingen/hydrogrpah_locations.png', dpi = 300)
plt.savefig('AfbeeldingenPDF/hydrograph_locations.pdf')