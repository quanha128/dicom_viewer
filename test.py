import pyvista as pv
import vtk


pl = pv.Plotter()
vol = pv.read('./static/vtk/test.vtk')
_ = pl.add_volume(vol)
# vol.plot(volume=True, cmap="viridis")
# pl.export_html('balls.html')
import vtk
vwrite = vtk.vtkJSONDataSetWriter()
vwrite.SetInputData(vol)
vwrite.SetFileName('stuff')  # directory
vwrite.Update()
vwrite.Write()
pl.show()