import json
import re


def twoListsIntersection(l1, l2):
    return [element for element in l1 if element in l2]


def sortedAlphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanumKey = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanumKey)
