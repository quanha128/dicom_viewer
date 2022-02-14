#%%
import matplotlib.pyplot as plt
import mpl_toolkits
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pydicom
import glob
from os.path import join, dirname, realpath
import surf2stl

# load the DICOM files
# IMG_FOLDER = join(dirname(realpath(__file__)), 'static/img/')
DCM_FOLDER = join(dirname(realpath(__file__)), 'static/dcm/')

slices = []

files = glob.glob(join(DCM_FOLDER, '*.dcm'))
# print(files)

for fname in files:
    # print("loading: {}".format(fname))
    slices.append(pydicom.dcmread(fname))

# skip files with no SliceLocation (eg scout views)
# slices = []
# skipcount = 0
# for f in files:
#     if hasattr(f, 'SliceLocation'):
#         slices.append(f)
#     else:
#         skipcount = skipcount + 1

# print("skipped, no SliceLocation: {}".format(skipcount))

# ensure they are in the correct order

slices = sorted(slices, key=lambda s: s.ImagePositionPatient[2])

# pixel aspects, assuming all slices are the same
ps = slices[0].PixelSpacing
ss = slices[0].SliceThickness
ax_aspect = ps[1]/ps[0]
sag_aspect = ps[1]/ss
cor_aspect = ss/ps[0]

# create 3D array
img_shape = list(slices[0].pixel_array.shape)
img_shape.append(len(slices))
img3d = np.zeros(img_shape)

# fill 3D array with the images from the files
for i, s in enumerate(slices):
    img2d = s.pixel_array
    img3d[:, :, i] = img2d

z, x, y = img3d.nonzero()

# print(x)
# print(len(y))
# print(len(z))
# print(y)
# print(z)

fig = plt.figure()

axis = mpl_toolkits.mplot3d.Axes3D(fig)

axis.scatter(x, y, z, c=z, alpha=1)

# fig.show()

# plot 3 orthogonal slices
# a1 = plt.subplot(2, 2, 1)
# plt.imshow(img3d[:, :, img_shape[2]//2])
# a1.set_aspect(ax_aspect)

# a2 = plt.subplot(2, 2, 2)
# plt.imshow(img3d[:, img_shape[1]//2, :])
# a2.set_aspect(sag_aspect)

# a3 = plt.subplot(2, 2, 3)
# plt.imshow(img3d[img_shape[0]//2, :, :].T)
# a3.set_aspect(cor_aspect)

# plt.show()

# plt.savefig('full.png')
# %%
