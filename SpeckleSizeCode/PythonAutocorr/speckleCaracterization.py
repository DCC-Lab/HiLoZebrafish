from SpeckleSizeCode.PythonAutocorr import autocorrelation, peakMeasurement
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
import numpy as np


class SpeckleCaracerization:

    def __init__(self, imagePath: str, gaussianFilterNormalizationStdDev: float = 75, medianFilterSize: int = 3):
        self.__fileName = imagePath
        self.__autocorrObj = autocorrelation.Autocorrelation(imagePath)
        self.__image = self.__autocorrObj.image
        self.__autocorrObj.computeAutocorrelation(gaussianFilterNormalizationStdDev, medianFilterSize)
        self.__autocorrelation = self.__autocorrObj.autocorrelation
        self.__verticalSlice, self.__horizontalSlice = self.__autocorrObj.getSlices()
        self.__histInfo = (None, None, None)
        self.peakMeasureReport = {}

    @property
    def fullAutocorrelation(self):
        return self.__autocorrelation.copy()

    @property
    def autocorrelationSlices(self):
        return self.__verticalSlice.copy(), self.__horizontalSlice.copy()

    def computeFWHMOfSpecificAxisWithLinearFit(self, axis: str, maxNbPoints: int = 3, moreInUpperPart: bool = True):
        cleanedAxis = axis.lower().strip()
        if cleanedAxis == "horizontal":
            FWHM = peakMeasurement.FullWidthAtHalfMaximumLinearFit(self.__horizontalSlice, 1, maxNbPoints,
                                                                   moreInUpperPart)
            FWHM_value = FWHM.findFWHM()
        elif cleanedAxis == "vertical":
            FWHM = peakMeasurement.FullWidthAtHalfMaximumLinearFit(self.__verticalSlice, 1, maxNbPoints,
                                                                   moreInUpperPart)
            FWHM_value = FWHM.findFWHM()
        else:
            raise ValueError(f"Axis '{axis}' not supported. Try 'horizontal' or 'vertical'.")
        return FWHM_value

    def computeFWHMOfSpecificAxisWithNeighborsAveraging(self, axis: str, averageRange: float = 0.2):
        cleanedAxis = axis.lower().strip()
        if cleanedAxis == "horizontal":
            FWHM = peakMeasurement.FullWidthAtHalfMaximumNeighborsAveraging(self.__horizontalSlice, 1, averageRange)
            FWHM_value = FWHM.findFWHM()
        elif cleanedAxis == "vertical":
            FWHM = peakMeasurement.FullWidthAtHalfMaximumNeighborsAveraging(self.__verticalSlice, 1, averageRange)
            FWHM_value = FWHM.findFWHM()
        else:
            raise ValueError(f"Axis '{axis}' not supported. Try 'horizontal' or 'vertical'.")
        return FWHM_value

    def computeFWHMBothAxes(self, alsoReturnMean: bool = True, method: str = "mean", *args, **kwargs):
        cleanedMethod = method.lower().strip()
        if cleanedMethod == "linear":
            vertical = self.computeFWHMOfSpecificAxisWithLinearFit("vertical", *args, **kwargs)
            horizontal = self.computeFWHMOfSpecificAxisWithLinearFit("horizontal", *args, **kwargs)
        elif cleanedMethod == "mean":
            vertical = self.computeFWHMOfSpecificAxisWithNeighborsAveraging("vertical", *args, **kwargs)
            horizontal = self.computeFWHMOfSpecificAxisWithNeighborsAveraging("horizontal", *args, **kwargs)
        else:
            raise ValueError(f"Method '{method}' not supported. Try 'linear' or 'error'.")
        return (vertical, horizontal, (vertical + horizontal) / 2) if alsoReturnMean else (vertical, horizontal)

    def intensityHistogram(self, nbBins: int = 256, showHistogram: bool = True):
        hist, bins, _ = plt.hist(self.__image.ravel(), nbBins, (0, self.__maxPossibleIntensityValue()))
        plt.xlabel("Bin [-]")
        plt.ylabel("Number of occurrences [-]")
        plt.title(f"Intensity histogram of the speckle pattern, with {nbBins} bins.")
        if showHistogram:
            plt.show()
        self.__histInfo = (hist, bins, nbBins)
        return hist, bins

    def isFullyDevelopedSpecklePattern(self, nbBins: int = 256):
        if self.__histInfo[-1] != nbBins:
            self.intensityHistogram(nbBins, False)
        hist, bins, _ = self.__histInfo
        if np.argmax(hist) == 0:  # If the maximum of the intensity distribution is at index 0, we suppose exp dist.
            return True
        return False

    def meanIntensity(self):
        return np.mean(self.__image)

    def stdDevIntensity(self):
        return np.std(self.__image)

    def medianIntensity(self):
        return np.median(self.__image)

    def maxIntensity(self):
        return np.max(self.__image)

    def minIntensity(self):
        return np.min(self.__image)

    def contrastModulation(self):
        return (self.maxIntensity() - self.minIntensity()) / (self.maxIntensity() + self.minIntensity())

    def globalContrast(self):
        return self.stdDevIntensity() / self.meanIntensity()

    def localContrast(self, kernelSize: int = 7):
        if kernelSize < 2:
            raise ValueError("The size of the local contrast kernel must be at least 2.")
        kernel = np.ones((kernelSize, kernelSize))
        n = kernel.size
        windowedAverage = convolve2d(self.__image, kernel, "valid") / n
        squaredImageFilter = convolve2d(self.__image ** 2, kernel, "valid")
        # Compute de sample standard deviation
        stdImageWindowed = ((squaredImageFilter - n * windowedAverage ** 2) / (n - 1)) ** 0.5
        return stdImageWindowed / windowedAverage

    def __maxPossibleIntensityValue(self):
        dtype = self.__image.dtype
        if "float" in str(dtype):
            maxPossible = 1
        elif "int" in str(dtype):
            maxPossible = np.iinfo(dtype).max
        else:
            raise TypeError(f"The type '{dtype}' is not supported for a speckle image.")
        return maxPossible


if __name__ == '__main__':
    # path = r"..\PythonAutocorr\sumOfCircularWithPhases\100sims\32pixels_100simulationsOfCircles.tiff"
    #path = r"..\PythonAutocorr\gaussianWithPhasesSimulations\32sigmaGaussianWithPhasesSimulations_cut1overE.tiff"
    # sc = SpeckleCaracerization(path)
    # sc.showFullAutocorrelation()
    # sc.fullReport(20 / 100)
    # # print(np.round(sc.computeFWHMBothAxes(False, "error", error=20 / 100)[0] / 2, 2))
    # # print(np.round(sc.computeFWHMBothAxes(False, "linear", maxNbPoints=10)[0] / 2, 2))
    path = r"C:\Users\ludod\Desktop\Stage_CERVO\speckle_imagery\simsave_for_speckle_diameter\test1.tiff"
    k = SpeckleCaracerization(path)
    print(k.computeFWHMBothAxes)
    from scipy.ndimage import correlate
    import tifffile as tf

    image = tf.imread(path)
    #corr = correlate(image[:200, :200], image[:200, :200], )
    #plt.imshow(corr)
    #plt.show()
