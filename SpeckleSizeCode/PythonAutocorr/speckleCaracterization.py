from SpeckleSizeCode.PythonAutocorr import autocorrelation, utils
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
            FWHM = utils.FullWidthAtHalfMaximumOneDimension(self.__horizontalSlice)
            FWHM = FWHM.findFWHMWithLinearFit(1)
        elif cleanedAxis == "vertical":
            FWHM = utils.FullWidthAtHalfMaximumOneDimension(self.__verticalSlice)
            FWHM = FWHM.findFWHMWithLinearFit(1)
        else:
            raise ValueError(f"Axis '{axis}' not supported. Try 'horizontal' or 'vertical'.")
        return FWHM

    def computeFWHMOfSpecificAxisWithError(self, axis: str, error: float = 0.05):
        cleanedAxis = axis.lower().strip()
        if cleanedAxis == "horizontal":
            FWHM = utils.FullWidthAtHalfMaximumOneDimension(self.__horizontalSlice)
            FWHM = FWHM.findFWHMWithinError(1, error)
        elif cleanedAxis == "vertical":
            FWHM = utils.FullWidthAtHalfMaximumOneDimension(self.__verticalSlice)
            FWHM = FWHM.findFWHMWithinError(1, error)
        else:
            raise ValueError(f"Axis '{axis}' not supported. Try 'horizontal' or 'vertical'.")
        return FWHM

    def computeFWHMBothAxes(self, method: str = "error", *errorArgs, **errorKwargs):
        cleanedMethod = method.lower().strip()
        if cleanedMethod == "linear":
            vertical = self.computeFWHMOfSpecificAxisWithLinearFit("vertical")
            horizontal = self.computeFWHMOfSpecificAxisWithLinearFit("horizontal")
        elif cleanedMethod == "error":
            vertical = self.computeFWHMOfSpecificAxisWithError("vertical", *errorArgs, **errorKwargs)
            horizontal = self.computeFWHMOfSpecificAxisWithError("horizontal", *errorArgs, **errorKwargs)
        else:
            raise ValueError(f"Method '{method}' not supported. Try 'linear' or 'error'.")
        return vertical, horizontal

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
        verticalDiameter, horizontalDiameter = sc.computeFWHMBothAxes('error', FWHMFindingError)
        meanIntensity = self.meanIntensity()
        stdDevIntensity = self.stdDevIntensity()
        medianIntensity = self.medianIntensity()
        minIntensity = self.minIntensity()
        maxIntensity = self.maxIntensity()
        header = "===== Speckle caracterization report ====="
        generalFileInfo = f"File path : {fileName}"
        speckleSizeInfo = f"Vertical speckle diameter (average) : {verticalDiameter} (with {errorForFWHM}% error)\n" \
            f"Horizontal speckle diameter (average) : {horizontalDiameter} (with {errorForFWHM}% error)"
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
            raise TypeError("The type 'dtype' is not supported for a speckle image.")
        return maxPossible


if __name__ == '__main__':
    path = r"..\PythonAutocorr\sumOfCircularWithPhases\10sims\4pixels_10simulationsOfCircles.tiff"
    path = r"..\PythonAutocorr\circularWithPhasesSimulations\16pixelsCircularWithPhasesSimulations.tiff"
    sc = SpeckleCaracerization(path)
    sc.fullReport(0.1)
