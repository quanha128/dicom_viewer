import matplotlib.pyplot as plt
import numpy as np
import pydicom
import glob
from PIL import Image
from os.path import join, dirname, realpath

DCM_FOLDER = join(dirname(realpath(__file__)), 'static/dcm/')

slices = []

for fname in glob.glob(join(DCM_FOLDER, '*.dcm'), recursive=False):
    print("loading: {}".format(fname))
    slices.append(pydicom.dcmread(fname))

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

#axial
img = Image.fromarray(img3d[:, :, img_shape[2]//2], 'RGB')
img.save('my.png')