import matplotlib.pyplot as plt
import numpy as np
import pydicom
import glob
from os.path import join, dirname, realpath
import nrrd

IMG_FOLDER = join(dirname(realpath(__file__)), 'static/img/')
DCM_FOLDER = join(dirname(realpath(__file__)), 'static/dcm/')
VTK_FOLDER = join(dirname(realpath(__file__)), 'static/vtk/')

def read():
  slices = []

  files = glob.glob(join(DCM_FOLDER, '*.dcm'))

  for fname in files:
      # print("loading: {}".format(fname))
      slices.append(pydicom.dcmread(fname))

  slices = sorted(slices, key=lambda s:s.ImagePositionPatient[2])

  return slices

def create_array(slices):
  # pixel aspects, assuming all slices are the same
  ps = slices[0].PixelSpacing
  ss = slices[0].SliceThickness
  # ax_aspect = ps[1]/ps[0]
  # sag_aspect = ps[1]/ss
  # cor_aspect = ss/ps[0]

  # create 3D array
  img_shape = list(slices[0].pixel_array.shape)
  img_shape.append(len(slices))
  img3d = np.zeros(img_shape)

  # fill 3D array with the images from the files
  for i, s in enumerate(slices):
    img2d = s.pixel_array
    img3d[:, :, i] = img2d

  return img3d, img_shape


def render_img(img3d, img_shape):
  # axial
  plt.imsave(join(IMG_FOLDER, 'axial.png'), img3d[:, :, img_shape[2]//2])

  # sagittal
  plt.imsave(join(IMG_FOLDER, 'sagittal.png'), img3d[:, img_shape[1]//2, :])
  
  # coronal
  plt.imsave(join(IMG_FOLDER, 'coronal.png'), img3d[img_shape[0]//2, :, :].T)

  print('rendered images')

def render_nrrd(img3d):
  # write to NRRD
  nrrd.write('output.nrrd', img3d, index_order='C')
  print('rendered nrrd')
