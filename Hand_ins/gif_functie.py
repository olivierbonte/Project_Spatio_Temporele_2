import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def gif_maken_bis(layers, tijdstappen, fps, naam_file):
    fig, ax = plt.subplots(figsize = (8,8))
    a = layers[0]
    im = plt.imshow(np.flipud(a), interpolation='none', vmin=0, vmax=np.max(layers[:]), cmap = 'binary', 
    extent= [np.min(xs)-deltax/2, np.max(xs)+deltax/2, 
    np.min(ys)-deltay/2,np.max(ys)+deltay/2])
    plt.colorbar(im)
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')


    def animate_func(i):
        if i % fps == 0:
            print( '.', end ='' )

        im.set_array(np.flipud(layers[i]))
        ax.set_title('time = '+str(np.round(tijdstappen[i]/60,2)) + 'min')
    
        return [im]

    anim = animation.FuncAnimation(fig, animate_func, frames = len(layers), interval = 1000 / fps) # in ms)
    anim.save(naam_file+'.gif', writer= 'pillow', fps=fps)# extra_args=['-vcodec', 'libx264'])        
    print("Gif opgeslaan als "+naam_file)