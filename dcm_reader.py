import matplotlib.pyplot as plt
import numpy as np
import pydicom
import glob
from PIL import Image
from os.path import join, dirname, realpath

IMG_FOLDER = join(dirname(realpath(__file__)), 'static/img/')
DCM_FOLDER = join(dirname(realpath(__file__)), 'static/dcm/')

def read():
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

  
  # fig = plt.figure()
  # # axial aspect
  # a1 = fig.add_subplot(2, 2, 1)
  # a1.imshow(img3d[:, :, img_shape[2]//2])
  # a1.set_aspect(ax_aspect)
  # extent = a1.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
  # fig.savefig(join(IMG_FOLDER, 'axial.png'), bbox_inches=extent)

  # # sagittal aspect
  # a2 = fig.add_subplot(2, 2, 2)
  # a2.imshow(img3d[:, img_shape[1]//2, :])
  # a2.set_aspect(sag_aspect)
  # extent = a2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
  # fig.savefig(join(IMG_FOLDER, 'sagittal.png'), bbox_inches=extent)

  # # coronal aspect
  # a3 = fig.add_subplot(2, 2, 3)
  # a3.imshow(img3d[img_shape[0]//2, :, :].T)
  # a3.set_aspect(cor_aspect)
  # extent = a3.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
  # fig.savefig(join(IMG_FOLDER, 'coronal.png'), bbox_inches=extent)

  # fig.savefig(join(IMG_FOLDER, 'full.png'))