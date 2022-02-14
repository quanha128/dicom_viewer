
import pydicom
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import sys
import glob
import surf2stl
# import pyvista as pv

points = np.random.rand(100, 3)
# mesh = pv.PolyData(points)
# mesh.plot(point_size=10, style='points')

# print(points)
x = np.outer(np.linspace(-2, 2, 10), np.ones(10))
y = x.copy().T
z = np.cos(x ** 2 + y ** 3)
 
fig = plt.figure()
 
# syntax for 3-D plotting
ax = plt.axes(projection ='3d')
 
# syntax for plotting
ax.plot_surface(x, y, z, cmap ='viridis', edgecolor ='green')
ax.set_title('Surface plot geeks for geeks')
# plt.show()

surf2stl.write('3d-model-graph.stl', x, y, z)