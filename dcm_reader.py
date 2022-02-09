import matplotlib.pyplot as plt
import pydicom

if __name__ == "__main__":
    ds = pydicom.dcmread("./dicoms/n2d_0004.dcm")
    n = ds.pixel_array.shape[0]
    fig, ax = plt.subplots(n,1, figsize=(200,200))
    for i in range(n):
        ax[i].imshow(ds.pixel_array[i], cmap=plt.cm.bone)