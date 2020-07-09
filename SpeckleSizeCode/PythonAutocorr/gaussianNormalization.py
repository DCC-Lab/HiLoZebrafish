import tifffile
from scipy.ndimage import gaussian_filter
import numpy as np
import cv2
import os


class GaussianNormalization:

    def __init__(self, image: np.ndarray):
        self.image = image
        self.normalized = None

    def normalize(self, stdDev: float):
        gaussianFiltered = gaussian_filter(self.image, stdDev)
        self.normalized = self.image / gaussianFiltered - np.mean(self.image)

    def saveToOriginalFormat(self, name: str, stdDevNormalization: float = 75):
        raise NotImplementedError("You must implement this method in format-specific classes.")


class TiffFileGaussianNormalization(GaussianNormalization):

    def __init__(self, path: str):
        image = tifffile.imread(path)
        super(TiffFileGaussianNormalization, self).__init__(image)

    def saveToOriginalFormat(self, name: str, stdDevNormalization: float = 75):
        if self.normalized is None:
            self.normalize(stdDevNormalization)
        if not name.endswith(".tif") and not name.endswith(".tiff"):
            name += ".tif"
        tifffile.imwrite(name, self.image)


class PNGFileGaussianNormalization(GaussianNormalization):

    def __init__(self, path: str):
        image = cv2.imread(path)
        super(PNGFileGaussianNormalization, self).__init__(image)

    def saveToOriginalFormat(self, name: str, stdDevNormalization: float = 75):
        if self.normalized is None:
            self.normalize(stdDevNormalization)
        if not name.endswith(".png"):
            name += ".png"
        cv2.imwrite(name, self.image)


if __name__ == '__main__':
    # This is where you can normalize and save files.
    # This is an example that normalizes avery tif file in MATLAB folder.
    for nb in range(1, 32):
        fname = r"20190924-200ms_20mW_Ave15_Gray_10X0.4_{}.tif".format(nb)
        p = os.path.dirname(os.path.join(os.getcwd(), "..", ".."))
        path = os.path.join(p, "MATLAB", fname)
        newName = path[:-4] + "_GaussianNorm_75StdDev.tif"

        tif = TiffFileGaussianNormalization(path)
        tif.saveToOriginalFormat(newName)
