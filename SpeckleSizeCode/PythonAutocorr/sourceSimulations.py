import numpy as np
import dcclab as dcc
import tifffile as tfile


class FullyDeveloppedSpeckleSimulationWithSource:

    def __init__(self, simShape: int):
        self._simShape = simShape
        self._simulation = None

    @property
    def simulation(self):
        if self._simulation is None:
            return None
        return self._simulation.copy()

    def saveSimulation(self, path: str):
        sim = self._simulation
        if sim is None:
            raise ValueError("No simulation to save.")
        tfile.imwrite(path, sim.pixels)

    def showSimulation(self):
        sim = self.simulation
        if sim is None:
            raise ValueError("No simulation to show.")
        sim.display("gray")

    def generatePhases(self, lowerBound: float, upperBound: float):
        phases = np.random.uniform(lowerBound, upperBound, (self._simShape, self._simShape))
        return np.exp(1j * phases)

    def runSimulation(self):
        raise NotImplementedError("You must implement this abstract method in subclasses.")

    def intensityHistogram(self):
        sim = self.simulation
        if sim is None:
            raise ValueError("No simulation to extract intensity histogram.")
        hist, bins = sim.displayHistogram()
        return hist, bins


class FullyDeveloppedSpeckleSimulationWithCircularSource(FullyDeveloppedSpeckleSimulationWithSource):

    def __init__(self, simShape: int, circleDiameter: float):
        super(FullyDeveloppedSpeckleSimulationWithCircularSource, self).__init__(simShape)
        if circleDiameter <= 0:
            raise ValueError("The diameter must strictly positive (>0).")
        self.__radius = circleDiameter / 2

    def runSimulation(self):
        XY = np.indices((self._simShape, self._simShape))
        mask = dcc.Channel.createCircularMask(XY, self.__radius)
        simulationBefforeFFT = mask * self.generatePhases(-np.pi, np.pi)
        simulation = np.abs(np.fft.fftshift(np.fft.fft2(simulationBefforeFFT))) ** 2
        self._simulation = dcc.Channel(simulation.real)


class FullyDeveloppedSpeckleSimulationWithGaussianSource(FullyDeveloppedSpeckleSimulationWithSource):

    def __init__(self, simShape: int, gaussianSigma: float):
        super(FullyDeveloppedSpeckleSimulationWithGaussianSource, self).__init__(simShape)
        if gaussianSigma <= 0:
            raise ValueError("The gaussian standard deviation must strictly positive (>0).")
        self.__sigma = gaussianSigma

    def runSimulation(self):
        XY = np.indices((self._simShape, self._simShape))
        mask = dcc.Channel.createGaussianMask(XY, self.__sigma)
        simulationBefforeFFT = mask * self.generatePhases(-np.pi, np.pi)
        simulation = np.abs(np.fft.fftshift(np.fft.fft2(simulationBefforeFFT))) ** 2
        self._simulation = dcc.Channel(simulation.real)


class NotFullyDeveloppedSpecklesSimulationWithSource:
    # FIXME: Use ImageCollection, but need to be fixed first
    # FIXME: Implement addition, subtraction, etc. of Channel instances

    def __init__(self, simShape: int, nbOfSimulations: int):
        self._simShape = simShape
        if nbOfSimulations <= 0:
            raise ValueError("There must be at least one simulation to do.")
        self._nbSimulation = nbOfSimulations
        self.__allSims = None

    def runSimulationsWithCircularSources(self, circleDiameter: float):
        self.__allSims = []
        for _ in range(self._nbSimulation):
            sim = FullyDeveloppedSpeckleSimulationWithCircularSource(self._simShape, circleDiameter)
            sim.runSimulation()
            self.__allSims.append(sim)

    def runSimulationsWithGaussianSources(self, sigma: float):
        self.__allSims = []
        for _ in range(self._nbSimulation):
            sim = FullyDeveloppedSpeckleSimulationWithGaussianSource(self._simShape, sigma)
            sim.runSimulation()
            self.__allSims.append(sim)

    @property
    def allSimulations(self):
        if self.__allSims is None:
            return None
        return self.__allSims.copy()

    def sumOfAllSimulations(self):
        if self.__allSims is None:
            raise ValueError("No simulations done.")
        s = sum([x.simulation.pixels for x in self.__allSims])
        return dcc.Channel(s)

    def meanOfAllSimulations(self):
        s = self.sumOfAllSimulations()
        return dcc.Channel(s.pixels / len(self.__allSims))

    def intensityHistogram(self, sumOnly: bool = True):
        if sumOnly:
            data = self.sumOfAllSimulations()
        else:
            data = self.meanOfAllSimulations()
        hist, bins = data.displayHistogram()
        return hist, bins

    def showSimulation(self, sumOnly: bool = True):
        if sumOnly:
            data = self.sumOfAllSimulations()
        else:
            data = self.meanOfAllSimulations()
        data.display("gray")


if __name__ == '__main__':
    # c = FullyDeveloppedSpeckleSimulationWithCircularSource(256, 256 // 2)
    # c.runSimulation()
    # c.showSimulation()
    # c.intensityHistogram()

    # g = FullyDeveloppedSpeckleSimulationWithGaussianSource(256, 256 // 2)
    # g.runSimulation()
    # g.showSimulation()
    # g.intensityHistogram()

    manyC = NotFullyDeveloppedSpecklesSimulationWithSource(256, 500)
    manyC.runSimulationsWithCircularSources(256 // 2)
    manyC.showSimulation()
    manyC.intensityHistogram()
