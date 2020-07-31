from SpeckleSizeCode.PythonAutocorr import autocorrelation, peakMeasurement
import matplotlib.pyplot as plt
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

    def computeFWHMOfSpecificAxisWithLinearFit(self, axis: str):
        cleanedAxis = axis.lower().strip()
        if cleanedAxis == "horizontal":
            FWHM = peakMeasurement.FullWidthAtHalfMaximumOneDimension(self.__horizontalSlice, 1)
            FWHM = FWHM.findFWHMWithLinearFit()
        elif cleanedAxis == "vertical":
            FWHM = peakMeasurement.FullWidthAtHalfMaximumOneDimension(self.__verticalSlice, 1)
            FWHM = FWHM.findFWHMWithLinearFit()
        else:
            raise ValueError(f"Axis '{axis}' not supported. Try 'horizontal' or 'vertical'.")
        return FWHM

    def computeFWHMOfSpecificAxisWithError(self, axis: str, error: float = 0.05):
        cleanedAxis = axis.lower().strip()
        if cleanedAxis == "horizontal":
            FWHM = peakMeasurement.FullWidthAtHalfMaximumOneDimension(self.__horizontalSlice, 1)
            FWHM = FWHM.findFWHMWithinError(error)
        elif cleanedAxis == "vertical":
            FWHM = peakMeasurement.FullWidthAtHalfMaximumOneDimension(self.__verticalSlice, 1)
            FWHM = FWHM.findFWHMWithinError(error)
        else:
            raise ValueError(f"Axis '{axis}' not supported. Try 'horizontal' or 'vertical'.")
        return FWHM

    def computeFWHMOfSpecificAxisWithKNeighbors(self, axis: str, k: int = 2, moreInUpperNeighbors: bool = True):
        cleanedAxis = axis.lower().strip()
        if cleanedAxis == "horizontal":
            FWHM = peakMeasurement.FullWidthAtHalfMaximumOneDimension(self.__horizontalSlice, 1)
            FWHM = FWHM.findFWHMWithAverageOfKNeighbors(k, moreInUpperNeighbors)
        elif cleanedAxis == "vertical":
            FWHM = peakMeasurement.FullWidthAtHalfMaximumOneDimension(self.__verticalSlice, 1)
            FWHM = FWHM.findFWHMWithAverageOfKNeighbors(k, moreInUpperNeighbors)
        else:
            raise ValueError(f"Axis '{axis}' not supported. Try 'horizontal' or 'vertical'.")
        return FWHM

    def computeFWHMBothAxes(self, alsoReturnMean: bool = True, method: str = "error", *args, **kwargs):
        cleanedMethod = method.lower().strip()
        if cleanedMethod == "linear":
            vertical = self.computeFWHMOfSpecificAxisWithLinearFit("vertical")
            horizontal = self.computeFWHMOfSpecificAxisWithLinearFit("horizontal")
        elif cleanedMethod == "error":
            vertical = self.computeFWHMOfSpecificAxisWithError("vertical", *args, **kwargs)
            horizontal = self.computeFWHMOfSpecificAxisWithError("horizontal", *args, **kwargs)
        elif cleanedMethod == "neighbors":
            vertical = self.computeFWHMOfSpecificAxisWithKNeighbors("vertical", *args, **kwargs)
            horizontal = self.computeFWHMOfSpecificAxisWithKNeighbors("horizontal", *args, **kwargs)
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

    def fullReport(self, FWHMFindingError: float = 0.05):
        fileName = self.__fileName
        errorForFWHM = FWHMFindingError * 100
        nbBins = 256
        verticalDiameter, horizontalDiameter, mean = self.computeFWHMBothAxes(method='error', error=FWHMFindingError)
        meanIntensity = self.meanIntensity()
        stdDevIntensity = self.stdDevIntensity()
        medianIntensity = self.medianIntensity()
        minIntensity = self.minIntensity()
        maxIntensity = self.maxIntensity()
        header = "===== Speckle caracterization report ====="
        generalFileInfo = f"File path : {fileName}"
        speckleSizeInfo = f"Vertical speckle diameter : {verticalDiameter} (mean of local neighbors within ±" \
            f"{errorForFWHM}% of 0.5)\n" \
            f"Horizontal speckle diameter : {horizontalDiameter} (mean of local neighbors within ±" \
            f"{errorForFWHM}% of 0.5)\n" \
            f"Mean of both directions : {mean}"
        specklePatternInfo = f"Mean intensity : {meanIntensity}\nStandard deviation : {stdDevIntensity}" \
            f"\nMedian : {medianIntensity}\nMin intensity : {minIntensity}, max intensity : {maxIntensity}"
        midReport = "----- Intensity histogram & pattern statistical info -----"
        toShow = [header, generalFileInfo, speckleSizeInfo, specklePatternInfo, midReport,
                  "Displaying intensity histogram..."]
        print(*toShow, sep="\n")
        hist, bins = self.intensityHistogram(nbBins)
        maxPossible = self.__maxPossibleIntensityValue()
        histInfo = f"Intensity histogram with {nbBins} bins, ranging from 0 to {maxPossible}"
        isFullyDeveloped = self.isFullyDevelopedSpecklePattern(nbBins)
        fullyDeveloped = f"The pattern is not fully developed "
        fullyDeveloped += f"(based on {nbBins} bins, its maximum is not at 0, not assuming exponential distribution)"
        if isFullyDeveloped:
            fullyDeveloped = f"The pattern is fully developed"
            fullyDeveloped += f" (based on {nbBins} bins, its maximum is at 0, assuming exponential distribution)"

        toShow = [histInfo, fullyDeveloped]
        print(*toShow, sep="\n")

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
    path = r"..\PythonAutocorr\sumOfCircularWithPhases\100sims\32pixels_100simulationsOfCircles.tiff"
    path = r"..\PythonAutocorr\gaussianWithPhasesSimulations\6sigmaGaussianWithPhasesSimulations_cut1overE.tiff"
    sc = SpeckleCaracerization(path)
    print(np.round(sc.computeFWHMBothAxes(False, "error", error=20 / 100)[0] / 2, 2))
    print(np.round(sc.computeFWHMBothAxes(False, "linear")[0] / 2, 2))
