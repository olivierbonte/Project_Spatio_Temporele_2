#making the hypothetical grid

#gaat uit van: 2 cellen op de crest even hoog, 2 cellen bij de pond even laag
import numpy as np
import matplotlib.pyplot as plt

nx = 30
ny = 20
grid = np.zeros((ny,nx))
slopex = 0.2/20 #slopes 5 keer steiler gemaakt! zo zelfde hoogteverschillen
slopey = 0.1/20
deltax = 10 #m
deltay = 10 #m
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

#add the heights of the buildings: 10 m
y_geen_gebouw = np.arange(4,21,5)
x_geen_gebouw = np.arange(7,30,8)
for j in range(ny):
    for i in range(nx):
        if not(i in x_geen_gebouw or j in y_geen_gebouw):
            grid[j,i] = grid[j,i] + 10 #so buildings of 10 m

#plt.figure(figsize= (7.5,7.5))
#plt.contourf(xs,ys,grid)
#plt.colorbar()
#plt.title('Contourplot of hypothetical surface')
#plt.xlabel('x [m]')
#plt.ylabel('y [m]')


#plt.figure(figsize= (10,7.5))
#X, Y = np.meshgrid(xs, ys)
#ax = plt.axes(projection='3d')
#im = ax.plot_surface(X, Y, grid, cmap = 'viridis')
#plt.colorbar(im)
#plt.xlabel('x [m]')
#plt.ylabel('y [m]')
#ax.set_zlabel('height [m]')
#plt.title('3D representation of hypothtetical surface')

plt.figure(figsize= (12,8))
plt.imshow(np.flipud(grid), extent = [np.min(xs)-deltax/2, np.max(xs)+deltax/2,
np.min(ys)-deltay/2,np.max(ys)+deltay/2])
plt.colorbar()
#plt.title('Contourplot of hypothetical surface')
plt.xlabel('x [m]')
plt.ylabel('y [m]')
#plt.savefig('Afbeeldingen/DEM_stad',dpi = 300)
plt.savefig('AfbeeldingenPDF/DEM_stad.pdf')