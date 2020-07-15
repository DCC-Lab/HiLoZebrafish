import numpy as np
import dcclab as dcc
import tifffile as tfile
import matplotlib.pyplot as plt


class SpeckleSimulationWithSource:

    def __init__(self, simShape: int):
        self._simShape = simShape
        self._simulation = None

    @property
    def simulation(self):
        if self._simulation is None:
            return None
        return self._simulation().copy()

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

    def generatePhases(self, lowerBound:float, upperBound:float):
        phases = np.random.uniform(lowerBound, upperBound, (self._simShape, self._simShape))
        return np.exp(1j * phases)

    def runSimulation(self):
        raise NotImplementedError("You must implement this abstract method in subclasses.")


class SpeckleSimulationWithCircularSource(SpeckleSimulationWithSource):

    def __init__(self, simShape: int, circleDiameter:float):
        super(SpeckleSimulationWithCircularSource, self).__init__(simShape)
        if circleDiameter <= 0:
            raise ValueError("The diameter must strictly positive (>0).")
        self.__radius = circleDiameter / 2

    def runSimulation(self):
        XY = np.indices((self._simShape, self._simShape))
        mask = dcc.Channel.createCircularMask(XY, self.__radius)
        simulationBefforeFFT = mask * self.generatePhases(-np.pi, np.pi)
        simulation = np.abs(np.fft.fftshift(np.fft.fft2(simulationBefforeFFT))) ** 2
        self._simulation = dcc.Channel(simulation.real)

class SpeckleSimulationWithGaussianSource(SpeckleSimulationWithSource):

    def __init__(self, simShape:int, gaussianSigma:float):
        super(SpeckleSimulationWithGaussianSource, self).__init__(simShape)
        if gaussianSigma <= 0:
            raise ValueError("The gaussian standard deviation must strictly positive (>0).")
        self.__sigma = gaussianSigma

    def runSimulation(self):
        XY = np.indices((self._simShape, self._simShape))
        mask = dcc.Channel.createGaussianMask(XY, self.__sigma)
        simulationBefforeFFT = mask * self.generatePhases(-np.pi, np.pi)
        simulation = np.abs(np.fft.fftshift(np.fft.fft2(simulationBefforeFFT))) ** 2
        self._simulation = dcc.Channel(simulation.real)