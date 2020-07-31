import numpy as np
import math


class HalfWidthAtHalfMaximumOneDimension:

    def __init__(self, data: np.ndarray, maximum: float = None, positiveSlopeSideOfPeak: bool = None):
        # If no maximum is provided, taking the maximal value of data. Else, taking the provided one.
        # if positiveSlopeSideOfPeak is not None: assumes there is only half of the central peak, either the increasing
        # side (arg is True) or the decreasing one (arg is False).
        # Else, the algorithm takes the left left side of the peak.
        if maximum is None:
            maximum = np.max(data)
        self.maximum = maximum
        if positiveSlopeSideOfPeak is None:
            data = data[:np.argmax(data)]
            positiveSlopeSideOfPeak = True
        if not isinstance(data, np.ndarray):
            raise TypeError("The data must be within a numpy array.")
        if data.ndim != 1:
            raise ValueError("The data must be in one dimension.")
        self.__data = data
        self.__sideOfPeak = "left" if positiveSlopeSideOfPeak else "right"

    def findHWHMWithAverageOfKNeighbors(self, k: int = 2, moreInUpperNeighbors: bool = True):
        if k > 2:
            raise ValueError("There should be at least 2 neighbors")
        halfMax = self.maximum / 2
        halfK = k / 2
        upperKs = math.ceil(halfK)
        lowerKs = math.floor(halfK)
        if not moreInUpperNeighbors:
            temp = upperKs
            upperKs = lowerKs
            lowerKs = temp
        upperPoints = np.where(self.__data >= halfMax)[0]
        lowerPoints = np.where(self.__data <= halfMax)[0]
        if self.__sideOfPeak == "left":
            upperPointsForHWHM = upperPoints[:upperKs]
            lowerPointsForHWHM = lowerPoints[-lowerKs:]
            left = np.mean(np.append(upperPointsForHWHM, lowerPointsForHWHM))
            right = len(self.__data)
        else:
            upperPointsForHWHM = upperPoints[-upperPoints:]
            lowerPointsForHWHM = lowerPoints[:lowerPoints]
            left = 0
            right = np.mean(np.append(upperPointsForHWHM, lowerPointsForHWHM))
        HWHM = right - left
        return HWHM

    def findHWHMWithinError(self, error=0.05):
        halfMax = self.maximum / 2
        print(np.max(self.__data) / 2)
        inferiorBound = halfMax - halfMax * error
        superiorBound = halfMax + halfMax * error
        pointsForHWHM = np.where((self.__data >= inferiorBound) & (self.__data <= superiorBound))[0]
        nbPoints = len(pointsForHWHM)
        if nbPoints == 0:
            raise ValueError("The error is too small. Not enough values were found to compute the HWHM.")
        if self.__sideOfPeak == "left":
            left = np.mean(pointsForHWHM)
            right = len(self.__data)
        else:
            left = 0
            right = np.mean(pointsForHWHM)
        HWHM = right - left
        return HWHM

    def findHWHMWithLinearFit(self):
        halfMax = self.maximum / 2
        lows, highs, lIndices, hIndices = splitInTwoWithMiddleValue(halfMax, self.__data, True)
        if self.__sideOfPeak == "left":
            low = lows[-1]
            high = highs[0]
            lIndice = lIndices[-1]
            hIndice = hIndices[0]
            slope, zero = linearEquation(low, high, lIndice, hIndice)
            left = findXWithY(halfMax, slope, zero)
            right = len(self.__data)
        else:
            low = lows[0]
            high = highs[-1]
            lIndice = lIndices[0]
            hIndice = hIndices[-1]
            slope, zero = linearEquation(low, high, lIndice, hIndice)
            right = findXWithY(halfMax, slope, zero)
            left = 0
        HWHM = right - left
        return HWHM


class FullWidthAtHalfMaximumOneDimension(HalfWidthAtHalfMaximumOneDimension):

    def __init__(self, data: np.ndarray, maximum: float = None):
        super(FullWidthAtHalfMaximumOneDimension, self).__init__(data, maximum)

    def findFWHMWithAverageOfKNeighbors(self, k: int = 2, moreInUpperNeighbors: bool = True):
        HWHM = self.findHWHMWithAverageOfKNeighbors(k, moreInUpperNeighbors)
        return 2 * HWHM

    def findFWHMWithinError(self, error: float = 0.05):
        HWHM = self.findHWHMWithinError(error)
        return 2 * HWHM

    def findFWHMWithLinearFit(self):
        HWHM = self.findHWHMWithLinearFit()
        return 2 * HWHM


def splitInTwoWithMiddleValue(middleValue: float, array: np.ndarray, returnIndices: bool = False):
    # Assumes the values are only increasing or decreasing, not both.
    # Excludes the middle value
    upper = np.ravel(np.where(array > middleValue))  # Doesn't change anything since 1D data
    lower = np.ravel(np.where(array < middleValue))  # Doesn't change anything since 1D data
    lowerValues = array[lower]
    upperValues = array[upper]
    if not returnIndices:
        return lowerValues, upperValues
    return lowerValues, upperValues, lower, upper


def linearEquation(y1, y2, x1, x2):
    deltaY = y2 - y1
    deltaX = x2 - x1
    slope = deltaY / deltaX
    zero = y1 - slope * x1
    return slope, zero


def findXWithY(y, slope, zero):
    x = (y - zero) / slope
    return x
