import numpy as np
import matplotlib.pyplot as plt
import tifffile
import os
from scipy.ndimage import gaussian_filter
import cv2


class FileReader:
    # FIXME: This is only until pydcclab is ok

    @staticmethod
    def readFile(path: str):
        if path.endswith(".tif") or path.endswith(".tiff"):
            pixels = tifffile.imread(path)
        else:
            pixels = cv2.imread(path)
        return pixels.T  # we want shape[0] as the width and shape[1] as the height


class Autocorrelation:
    # FIXME: Use pydcclab when ok

    def __init__(self, imagePath: str):
        self.__image = FileReader.readFile(imagePath)
        self.__original = self.image
        self.__autocorrelation = None

    @property
    def image(self):
        return self.__image.copy()

    @property
    def autocorrelation(self):
        if self.__autocorrelation is None:
            return None
        return self.__autocorrelation.copy()

    def showImage(self):
        plt.imshow(self.__image)
        plt.show()

    def showAutocorrelation(self, showColorbar: bool = True):
        if self.__autocorrelation is None:
            raise ValueError("No autocorrelation computed.")
        plt.imshow(self.__autocorrelation)
        if showColorbar:
            plt.colorbar()
        plt.show()

    def showAutocorrelationSlices(self, indices: tuple = None, showHorizontal: bool = True, showVertical: bool = True):
        vSlice, hSlice = self._getSlices(indices)
        if showHorizontal and showVertical:
            fig, (ax1, ax2) = plt.subplots(2, sharey="col")
            fig.suptitle("Autocorrelation slices")

            ax1.plot(hSlice)
            ax1.set_title(f"Horizontal slice of the autocorrelation (at index {indices[0]})")
            ax1.set_xlabel("Horizontal position $x$ [pixel]")

            ax2.plot(vSlice)
            ax1.set_title(f"Vertical slice of the autocorrelation (at index {indices[1]})")
            ax1.set_xlabel("Vertical position $y$ [pixel]")

            ylabel = "Normalized autocorrelation coefficient [-]"
            fig.text(0.06, 0.5, ylabel, ha='center', va='center', rotation='vertical')
            plt.subplots_adjust(hspace=0.32)
            plt.show()
        elif showVertical:
            pass
        elif showHorizontal:
            pass


    def _gaussianNormalization(self, filterStdDev: float = 75):
        filteredImage = gaussian_filter(self.__image, filterStdDev)
        self.__image = self.__image / filteredImage - np.mean(self.__image)

    def _autocorrelationWithFourierTransform(self):
        fft = np.fft.fft2(self.__image)
        ifft = np.fft.ifftshift(np.fft.ifft2(np.abs(fft) ** 2)).real
        ifft /= np.size(ifft)
        self.__autocorrelation = (ifft - np.mean(ifft) ** 2) / np.var(ifft)

    def _getSlices(self, indices: tuple = None):
        # We suppose shape[0] is the width and shape[1] is the height
        if indices is None:
            xSlice, ySlice = self.__autocorrelation.shape[0] // 2, self.__autocorrelation.shape[1] // 2
        elif len(indices) != 2:
            raise ValueError("There must be 2 indices when specified.")
        else:
            xSlice, ySlice = indices[0], indices[1]
        verticalSlice = self.__autocorrelation[:, ySlice]
        horizontalSlice = self.__autocorrelation[xSlice, :]
        return verticalSlice, horizontalSlice
