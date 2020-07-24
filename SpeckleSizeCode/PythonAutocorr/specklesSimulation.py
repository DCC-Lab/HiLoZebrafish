import tifffile as tfile
import numpy as np
import warnings
import matplotlib.pyplot as plt
import itertools
import random
import cv2
from scipy.ndimage import gaussian_filter


class RandomPositionGenerator:

    def __init__(self, minimumX: float, maximumX: float, minimumY: float, maximumY: float, minimumSpacing: float = 1):
        self.xRange = (minimumX, maximumX)
        self.yRange = (minimumY, maximumY)
        if minimumSpacing <= 0:
            raise ValueError("The minimum spacing must be positive and different from 0.")
        self.minimumSpacing = minimumSpacing
        self._image = None

    @property
    def image(self):
        if self._image is None:
            return None
        return self._image.copy()

    def saveImage(self, name: str):
        if self._image is None:
            raise AttributeError("The simulation is not done. Please generate the image first.")
        tfile.imwrite(name, self._image)

    def showImage(self):
        if self._image is None:
            raise AttributeError("The simulation is not done. Please generate the image first.")
        plt.imshow(self._image)
        plt.show()

    def generatePositions(self, nbPositions: int = 1):
        if nbPositions < 1:
            raise ValueError("There must be at least 1 position.")
        allX = np.arange(*self.xRange, self.minimumSpacing)
        allY = np.arange(*self.yRange, self.minimumSpacing)
        allPos = list(itertools.product(allX, allY))
        nbPossiblePositions = len(allPos)
        if nbPositions > nbPossiblePositions:
            msg = "The required number of positions if larger than the possible number of positions."
            msg += " The latter will be considered."
            warnings.warn(msg)
            nbPositions = nbPossiblePositions
        chosenPositions = random.sample(allPos, nbPositions)
        return chosenPositions


class CirclesGenerator(RandomPositionGenerator):

    def __init__(self, imageShape: tuple, radius: int = 1, minimumSpacing: float = None):
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
        allPos = self.generatePositions(nbCircles)
        for pos in allPos:
            # FIXME: circle position is (x, y) or (y, x)?
            image = cv2.circle(image, pos, self.radius, 1, -1)
        self._image = image


class GaussianGenerator(RandomPositionGenerator):

    def __init__(self, imageShape: tuple, sigma: float = 1, minimumSpacing: float = None):
        if sigma <= 0:
            raise ValueError("The gaussian standard deviation sigma cannot be negative nor zero.")
        if len(imageShape) != 2:
            raise ValueError("The image must be grayscale (i.e. a tuple of 2 elements).")
        self.sigma = sigma
        self.imageShape = imageShape
        minX, maxX = 0, imageShape[1]
        minY, maxY = 0, imageShape[0]
        if minimumSpacing is None:
            minimumSpacing = 2 * self.sigma
        super(GaussianGenerator, self).__init__(minX, maxX, minY, maxY, minimumSpacing)

    def generateGaussians(self, nbGaussians: int = 1, displayProgress: bool = True):
        if nbGaussians <= 0:
            raise ValueError("There must be at least one gaussian.")

        allPos = self.generatePositions(nbGaussians)
        image = np.zeros(self.imageShape)
        current = 0
        total = len(allPos)
        for pos in allPos:
            image += self.gaussianDistribution3DMax(self.sigma, self.imageShape, *pos)
            current += 1
            if displayProgress and (current % 10 == 0 or current == total):
                print(f"{current} / {total} done.")
        self._image = image

    @classmethod
    def gaussianDistribution3DMax(cls, sigma: float, imageShape: tuple, muX, muY):
        arrY, arrX = np.indices(imageShape).copy()
        return np.exp(-((arrX - muX) ** 2 / (2 * sigma ** 2) + (arrY - muY) ** 2 / (2 * sigma ** 2)))


if __name__ == '__main__':
    x = 1000
    y = 1000
    sigma = 4
    separation = 1
    nbGaussians = 10000
    g = GaussianGenerator((y, x), sigma, minimumSpacing=separation)
    g.generateGaussians(int(nbGaussians))
    img = g.image
    g.showImage()
    ok = input("Save image?\n")
    if ok.lower() == "y":
        g.saveImage(f"gaussianSimulations\\{nbGaussians}gaussians_{x}x{y}_{sigma}sigma_{separation}separation.tiff")
    cv2.imwrite("10000.png", img)
