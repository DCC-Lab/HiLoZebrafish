import numpy as np
import dcclab as dcc
import tifffile as tfile
import matplotlib.pyplot as plt
import time
from cv2 import cv2


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
        tfile.imwrite(path, sim)

    def showSimulation(self):
        sim = self.simulation
        if sim is None:
            raise ValueError("No simulation to show.")
        plt.imshow(sim, "gray")
        plt.show()

    def generatePhases(self, lowerBound: float, upperBound: float):
        phases = np.random.uniform(lowerBound, upperBound, (self._simShape, self._simShape))
        return np.exp(1j * phases)

    def runSimulation(self):
        raise NotImplementedError("You must implement this abstract method in subclasses.")

    def intensityHistogram(self):
        sim = self.simulation
        if sim is None:
            raise ValueError("No simulation to extract intensity histogram.")
        values, binEdges, _ = plt.hist(sim.ravel(), 256)
        plt.show()
        return values, 

    def applyShotNoise(self):
        self._simulation = np.random.poisson(self._simulation)
        

    def addShotNoise(self,scaling=2,resize=False):
        self._simulation = self._simulation * 255
        self._simulation = self._simulation.astype(np.uint8)
        print(self._simulation)
        if resize != False:
            self._simulation = cv2.resize(self._simulation,resize)
        x,y = self._simulation.shape
        simbase = self._simulation
        if scaling >= -2:
            self._simulation = self._simulation * (1 + ((scaling - 2) * 0.25))
            arraybefore = self._simulation.astype(np.int16)
            print(arraybefore)
            self.applyShotNoise()
            arrayafter = self._simulation.astype(np.int16)
            print(arrayafter)
            diff = arrayafter - arraybefore
            transfo = simbase.astype(np.int16)
            final = np.clip(transfo + diff,0,255)
            self._simulation = final.astype(np.uint8)
            print(self._simulation)
        else:
            raise ValueError("scaling value out of range: the scaling values have to be higher than -2")
    
    def supergaussian(self,center,pos,n,sigmax,sigmay,a=1):
       return a * np.exp((-2 * ((pos[0] - center[0]) / sigmax)**n) + (-2 * ((pos[1] - center[1]) / sigmay)**n))

    def nonUniformIntensity(self,n=4,sigmax=250,sigmay=250):
        if n % 2 != 0 or n < 2 :
            raise ValueError("n value can only be a positive and even number")
        i,j = self._simulation.shape
        center = (i // 2, j // 2)
        for xval in range(i):
            for yval in range(j):
                self._simulation[xval,yval] = self._simulation[xval,yval] * self.supergaussian(center,(xval,yval),n,sigmax,sigmay)



class FullyDeveloppedSpeckleSimulationWithCircularSource(FullyDeveloppedSpeckleSimulationWithSource):

    def __init__(self, simShape: int, circleDiameter: float):
        super(FullyDeveloppedSpeckleSimulationWithCircularSource, self).__init__(simShape)
        if circleDiameter <= 0:
            raise ValueError("The diameter must strictly positive (>0).")
        self.__radius = circleDiameter / 2

    def runSimulation(self):
        XY = np.indices((self._simShape, self._simShape))
        XY -= self._simShape // 2
        mask = dcc.Channel.createCircularMask(XY, self.__radius)
        simulationBefforeFFT = mask * self.generatePhases(-np.pi, np.pi)
        simulation = np.abs(np.fft.fftshift(np.fft.fft2(simulationBefforeFFT))) ** 2
        self._simulation = simulation.real
        self._simulation /= np.max(self._simulation)
        self._simulation = self._simulation.astype(np.float32)


class FullyDeveloppedSpeckleSimulationWithGaussianSource(FullyDeveloppedSpeckleSimulationWithSource):

    def __init__(self, simShape: int, gaussian2Sigma: float):
        super(FullyDeveloppedSpeckleSimulationWithGaussianSource, self).__init__(simShape)
        if gaussian2Sigma <= 0:
            raise ValueError("The gaussian standard deviation must be strictly positive (>0).")
        self.__sigma = gaussian2Sigma // 2

    def runSimulation(self):
        XY = np.indices((self._simShape, self._simShape))
        XY -= self._simShape // 2
        mask = dcc.Channel.createGaussianMask(XY, self.__sigma)
        simulationBefforeFFT = mask * self.generatePhases(-np.pi, np.pi)
        simulation = np.abs(np.fft.fftshift(np.fft.fft2(simulationBefforeFFT))) ** 2
        self._simulation = simulation.real
        self._simulation /= np.max(self._simulation)
        self._simulation = self._simulation.astype(np.float32)


class SumOfFullyDeveloppedSpecklesSimulationWithSource:
    # FIXME: Use ImageCollection, but need to be fixed first
    # FIXME: Implement addition, subtraction, etc. of Channel instances

    def __init__(self, simShape: int, nbOfSimulations: int):
        self._simShape = simShape
        if nbOfSimulations <= 0:
            raise ValueError("There must be at least one simulation to do.")
        self._nbSimulation = nbOfSimulations
        self.__allSims = None
        self.__progress = 0

    def __runSimulations_iterative(self, array: np.ndarray, simulationClass: type, classArg):
        for i in range(self._nbSimulation):
            obj = simulationClass(self._simShape, classArg)
            obj.runSimulation()
            sim = obj.simulation
            array[:, :, i] = sim
            self.__progress += 1
            if self.__progress % 10 == 0 or self.__progress == self._nbSimulation:
                print(f"All simulations: {self.__progress} / {self._nbSimulation} done,")

    def __runSimulations(self, slice_array, simulationClass: type, classArg):
        obj = simulationClass(self._simShape, classArg)
        obj.runSimulation()
        sim = obj.simulation
        self.__progress += 1
        if self.__progress % 10 == 0 or self.__progress == self._nbSimulation:
            print(f"All simulations: {self.__progress} / {self._nbSimulation} done,")
        return sim.ravel()

    def runSimulationsWithCircularSources(self, circleDiameter: float):
        start = time.perf_counter_ns()
        # self.__allSims = np.zeros((self._simShape * self._simShape, self._nbSimulation))
        # self.__allSims = np.apply_along_axis(self.__runSimulations, 0, self.__allSims,
        #                                      FullyDeveloppedSpeckleSimulationWithCircularSource,
        #                                      circleDiameter).reshape(
        #     (self._simShape, self._simShape, self._nbSimulation))
        self.__allSims = np.zeros((self._simShape, self._simShape, self._nbSimulation))
        self.__runSimulations_iterative(self.__allSims, FullyDeveloppedSpeckleSimulationWithCircularSource,
                                        circleDiameter)
        end = time.perf_counter_ns()
        print(f"Time: {(end - start) / 1e9} seconds")

    def runSimulationsWithGaussianSources(self, sigma: float):
        self.__allSims = np.zeros((self._simShape * self._simShape, self._nbSimulation))
        self.__allSims = np.apply_along_axis(self.__runSimulations, 0, self.__allSims,
                                             FullyDeveloppedSpeckleSimulationWithGaussianSource,
                                             sigma).reshape((self._simShape, self._simShape, self._nbSimulation))

    @property
    def allSimulations(self):
        if self.__allSims is None:
            return None
        return self.__allSims.copy()

    def sumOfAllSimulations(self):
        if self.__allSims is None:
            raise ValueError("No simulations done.")
        s = np.sum(self.__allSims, 2)
        return s

    def meanOfAllSimulations(self):
        mean = np.mean(self.__allSims, 2)
        return mean

    def intensityHistogram(self, sumOnly: bool = False):
        if sumOnly:
            data = self.sumOfAllSimulations()
        else:
            data = self.meanOfAllSimulations()
        values, binEdges, _ = plt.hist(data.ravel(), 256)
        plt.show()
        return values, binEdges

    def showSimulation(self, sumOnly: bool = False):
        if sumOnly:
            data = self.sumOfAllSimulations()
        else:
            data = self.meanOfAllSimulations()
        plt.imshow(data, "gray")
        plt.show()

    def saveSimulation(self, path: str, sumOnly: bool = False):
        if sumOnly:
            data = self.sumOfAllSimulations()
        else:
            data = self.meanOfAllSimulations()
        tfile.imwrite(path, data)


if __name__ == '__main__':
    shape = 1000
    """
    c = SumOfFullyDeveloppedSpecklesSimulationWithSource(shape, 2)
    c.runSimulationsWithCircularSources(shape // 6)
    values, _ = c.intensityHistogram()
    """
    k = FullyDeveloppedSpeckleSimulationWithCircularSource(shape,100)
    k.runSimulation()
    k.showSimulation()
    k.saveSimulation(r"C:\Users\ludod\Desktop\Stage_CERVO\speckle_imagery\simsave_for_speckle_diameter\test1.tiff")
    """
    k.addShotNoise(scaling=3)
    """
    k.addShotNoise(scaling=2)
    k.nonUniformIntensity(n=2,sigmax=500,sigmay=500)
    k.showSimulation()
    k.saveSimulation(r"C:\Users\ludod\Desktop\Stage_CERVO\speckle_imagery\simsave_for_speckle_diameter\test2.tiff")

    
