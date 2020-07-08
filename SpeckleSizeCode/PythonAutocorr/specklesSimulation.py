import cv2 as cv2
import numpy as np
import warnings
import matplotlib.pyplot as plt


class RandomPositionGenerator:

    def __init__(self, minimumX: float, maximumX: float, minimumY: float, maximumY: float, minimumSpacing: float = 1):
        self.xRange = (minimumX, maximumX)
        self.yRange = (minimumY, maximumY)
        if minimumSpacing <= 0:
            raise ValueError("The minimum spacing must be positive and different from 0.")
        self.minimumSpacing = minimumSpacing

    def generatePositions(self, nbPositions: int = 1):
        if nbPositions < 1:
            raise ValueError("There must be at least 1 position.")
        allX = np.arange(*self.xRange, self.minimumSpacing)
        allY = np.arange(*self.yRange, self.minimumSpacing)
        nbPossiblePositions = len(allX) * len(allY)
        if nbPositions > nbPossiblePositions:
            msg = "The required number of positions if larger than the possible number of positions."
            msg += " The latter will be considered."
            warnings.warn(msg)
            nbPositions = nbPossiblePositions
        counter = 0
        while counter < nbPositions:
            x = np.random.choice(allX, 1, False)
            y = np.random.choice(allY, 1, False)
            position = (x, y)
            counter += 1
            yield position


class CirclesGenerator(RandomPositionGenerator):

    def __init__(self, imageShape: tuple, radius: float = 1, minimumSpacing: float = None):
        if radius <= 0:
            raise ValueError("The radius must be larger than 0.")
        if len(imageShape) != 2:
            raise ValueError("The image must be grayscale (i.e. a tuple of 2 elements).")
        self.radius = radius
        self.imageShape = imageShape
        if minimumSpacing is None:
            minimumSpacing = 2 * self.radius
        minX, maxX = 0, imageShape[1]
        minY, maxY = 0, imageShape[0]
        super(CirclesGenerator, self).__init__(minX, maxX, minY, maxY, minimumSpacing)

    def generateCircles(self, nbCircles: int = 1):
        if nbCircles < 1:
            raise ValueError("There must be at least 1 circle.")
        image = np.zeros(self.imageShape)
        for pos in self.generatePositions(nbCircles):
            image = cv2.circle(image, pos, self.radius, 1, -1)
        return image


if __name__ == '__main__':
    x = 2000
    y = 2000
    radius = 30
    separation = 1
    nbCircles = 1600
    cgen = CirclesGenerator((y, x), radius, separation)
    image = cgen.generateCircles(nbCircles)
    plt.imshow(image)
    plt.show()
    save = input("Proceed with saving (y to continue, any other key to abort)?\n")
    if save.lower() == "y":
        cv2.imwrite(f"simulation_{y}x{x}_{nbCircles}circles_{separation}separation_{radius}radius.png", image)
