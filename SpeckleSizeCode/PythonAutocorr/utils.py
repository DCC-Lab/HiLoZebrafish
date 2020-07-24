import numpy as np
import math


def findKNearestNeighbor(k: int, value: float, array: np.ndarray, moreInUpper: bool = True):
    middle = k / 2
    lowerStop = math.floor(middle)
    upperStop = math.ceil(middle)
    if not moreInUpper:
        temp = upperStop
        upperStop = lowerStop
        lowerStop = temp
    lower, upper = splitInTwoWithMiddleValue(value, array)
    return lower[-lowerStop:], upper[:upperStop]


def splitInTwoWithMiddleValue(middleValue: float, array: np.ndarray):
    upper = np.where(array > middleValue)
    lower = np.where(array < middleValue)
    return array[lower], array[upper]
