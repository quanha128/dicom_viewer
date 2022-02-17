from csv import writer
import matplotlib.pyplot as plt
import numpy as np
import pydicom
import glob
from os.path import join, dirname, realpath
import pyvista as pv
import vtk

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

  # axial
  plt.imshow(img3d[:, :, img_shape[2]//2])
  plt.axis('off')
  # plt.savefig(join(IMG_FOLDER, 'axial.png'), bbox_inches='tight', pad_inches = 0)

  # sagittal
  plt.imshow(img3d[:, img_shape[1]//2, :])
  plt.axis('off')
  plt.savefig(join(IMG_FOLDER, 'sagittal.png'), bbox_inches='tight', pad_inches = 0)
  
  # coronal
  plt.imshow(img3d[img_shape[0]//2, :, :].T)
  plt.axis('off')
  plt.savefig(join(IMG_FOLDER, 'coronal.png'), bbox_inches='tight', pad_inches = 0)

  # Create the 3D NumPy array of spatially referenced data
  # This is spatially referenced such that the grid is 20 by 5 by 10
  #   (nx by ny by nz)
  # values = np.linspace(0, 10, 1000).reshape((20, 5, 10))
  values = img3d
  values.shape

  # Create the spatial reference
  grid = pv.UniformGrid()

  # Set the grid dimensions: shape because we want to inject our values on the
  #   POINT data
  grid.dimensions = values.shape

  # Edit the spatial reference
  # grid.origin = (100, 33, 55.6)  # The bottom left corner of the data set
  # grid.spacing = (1, 5, 2)  # These are the cell sizes along each axis

  # Add the data values to the cell data
  grid.point_data["values"] = values.flatten(order="F")  # Flatten the array!

  print(grid)
  filepath = join(VTK_FOLDER, 'test.vtk')
  grid.save(filepath, binary=True)
  reader = vtk.vtkGenericDataObjectReader()
  reader.SetFileName(filepath)
  reader.Update()
  ex = vtk.vtkOBJExporter()
  ex.SetInput(reader)
  ex.Update()
  ex.Write()
  print('reached here')
