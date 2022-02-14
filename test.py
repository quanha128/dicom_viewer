#%%
import pydicom
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits
from mpl_toolkits.mplot3d import Axes3D
import sys
import glob
import surf2stl
# import pyvista as pv

points = np.random.rand(100, 3)
# mesh = pv.PolyData(points)
# mesh.plot(point_size=10, style='points')

# print(points)
x = np.random.rand(100)
y = np.random.rand(100)
z = np.random.rand(100)
 
fig = plt.figure()
 
# syntax for 3-D plotting
axis = mpl_toolkits.mplot3d.Axes3D(fig)

axis.scatter(x, y, z)
 
# syntax for plotting
# ax.plot_surface(x, y, z, cmap ='viridis', edgecolor ='green')
# ax.set_title('Surface plot geeks for geeks')
fig.show()

surf2stl.write('points.stl', x, y, z)
# %%
