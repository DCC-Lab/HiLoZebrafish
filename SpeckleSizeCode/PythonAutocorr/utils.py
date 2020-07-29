import numpy as np


class FullWidthAtHalfMaximumOneDimension:

    def __init__(self, data: np.ndarray):
        # Assumes the data is increasing, then decreasing. There should be one peak at the maximum value.
        if not isinstance(data, np.ndarray):
            raise TypeError("The data must be within a numpy array.")
        if data.ndim != 1:
            raise ValueError("The data must be in one dimension.")
        self.__data = data

    def findFWHMWithinError(self, maximum: float = 1, error: float = 0.05):
        middlePoint = np.argmax(self.__data)
        halfMax = maximum / 2
        inferiorBound = halfMax - halfMax * error
        superiorBound = halfMax + halfMax * error
        pointsForFWHM = np.where((self.__data >= inferiorBound) & (self.__data <= superiorBound))[0]
        leftPointsForFWHM = pointsForFWHM[pointsForFWHM < middlePoint]
        rightPointsForFWHM = pointsForFWHM[pointsForFWHM > middlePoint]
        if len(rightPointsForFWHM) == 0 or len(leftPointsForFWHM) == 0:
            raise ValueError("The error is too small. Not enough values were found to compute the FWHM.")
        left = np.mean(leftPointsForFWHM)
        right = np.mean(rightPointsForFWHM)
        FWHM = right - left
        return FWHM

    def findFWHMWithLinearFit(self, maximum: float = 1):
        middlePoint = np.argmax(self.__data)
        print(self.__data[middlePoint] / 2)
        halfMax = maximum / 2
        firstHalf = self.__data[:middlePoint]
        secondHalf = self.__data[middlePoint:]
        lowFirst, highFirst, lowFirstIndices, highFirstIndices = splitInTwoWithMiddleValue(halfMax, firstHalf, True)
        lowSecond, highSecond, lowSecondIndices, highSecondIndices = splitInTwoWithMiddleValue(halfMax, secondHalf,
                                                                                               True)
        lowSecondIndices += middlePoint + 1
        highSecondIndices += middlePoint + 1
        firstSlope, firstZero = linearEquation(lowFirst[-1], highFirst[0], lowFirstIndices[-1], highFirstIndices[0])
        secondSlope, secondZero = linearEquation(lowSecond[-1], highSecond[-1], lowSecondIndices[0],
                                                 highSecondIndices[0])
        left = findXWithY(halfMax, firstSlope, firstZero)
        right = findXWithY(halfMax, secondSlope, secondZero)
        FWHM = right - left
        return FWHM


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
