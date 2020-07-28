import numpy as np
import math


class FullWidthAtHalfMaximum:

    def __init__(self, data: np.ndarray):
        if not isinstance(data, np.ndarray):
            raise TypeError("The data must be within a numpy array.")
        if data.ndim != 1:
            raise ValueError("The data must be in one dimension.")
        self.__data = data

    def findFWHMWithNeighbors(self, k: int, moreInUpper: bool = True):
        middlePoint = np.argmax(self.__data)
        halfMax = self.__data[middlePoint] / 2
        firstHalf = self.__data[:middlePoint]
        secondHalf = self.__data[middlePoint:]
        lowerNeighborsFirstHalf, upperNeighborsFirstHalf = findKNeighbors(k, halfMax, firstHalf, moreInUpper)
        lowerNeighborsSecondHalf, upperNeighborsSecondHalf = findKNeighbors(k, halfMax, secondHalf, moreInUpper)
        right = np.mean(np.append(lowerNeighborsFirstHalf, upperNeighborsFirstHalf))
        left = np.mean(np.append(lowerNeighborsSecondHalf, upperNeighborsSecondHalf))
        FWHM = right - left
        return FWHM

    def findFWHMWithLinearFit(self):
        middlePoint = np.argmax(self.__data)
        halfMax = self.__data[middlePoint] / 2
        firstHalf = self.__data[:middlePoint]
        secondHalf = self.__data[middlePoint:]
        lowFirst, highFirst, lowFirstIndices, highFirstIndices = splitInTwoWithMiddleValue(halfMax, firstHalf, True)
        lowSecond, highSecond, lowSecondIndices, highSecondIndices = splitInTwoWithMiddleValue(halfMax, secondHalf,
                                                                                               True)
        firstSlope, firstZero = linearEquation(lowFirst[-1], highFirst[0], lowFirstIndices[-1], highFirstIndices[0])
        secondSlope, secondZero = linearEquation(lowSecond[-1], highSecond[0], lowSecondIndices[-1],
                                                 highSecondIndices[0])
        left = findXWithY(halfMax, firstSlope, firstZero)
        right = findXWithY(halfMax, secondSlope, secondZero)
        FWHM = right - left
        return FWHM


def findKNeighbors(k: int, value: float, array: np.ndarray, moreInUpper: bool = True):
    middle = k / 2
    lowerStop = math.floor(middle)
    upperStop = math.ceil(middle)
    if not moreInUpper:
        temp = upperStop
        upperStop = lowerStop
        lowerStop = temp
    lower, upper = splitInTwoWithMiddleValue(value, array)
    return lower[-lowerStop:], upper[:upperStop]


def splitInTwoWithMiddleValue(middleValue: float, array: np.ndarray, returnIndices: bool = False):
    upper = np.where(array > middleValue)
    lower = np.where(array < middleValue)
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
