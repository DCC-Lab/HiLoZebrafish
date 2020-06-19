import numpy as np
import matplotlib.pyplot as plt
import tifffile
import os
from scipy.ndimage import gaussian_filter
from scipy.optimize import curve_fit

nb = 20
fname = rf"20190924-200ms_20mW_Ave15_Gray_10X0.4_{nb}.tif"

p = os.path.dirname(os.path.join(os.getcwd(), "..", ".."))
path = os.path.join(p, "MATLAB", fname)

if path.endswith("tif"):
    img = tifffile.imread(path)
else:
    img = plt.imread(path)

plt.imshow(img)
plt.show()

imgDivide = gaussian_filter(img, 75)

img = img / imgDivide - np.mean(img)
plt.imshow(img)
plt.show()

fft = np.fft.fft2(img)
ifft = np.fft.ifftshift(np.fft.ifft2(np.abs(fft) ** 2)).real
ifft /= np.size(ifft)

r = (ifft - np.mean(img) ** 2) / np.var(img)
plt.imshow(r)
plt.colorbar()
plt.show()

xSlice, ySlice = r.shape[1] // 2, r.shape[0] // 2

verticalSlice = r[:, xSlice]
horizontalSlice = r[ySlice, :]


def normalize(verticalSlice, horizontalSlice):
    verticalSlice = verticalSlice - np.min(verticalSlice)
    verticalSlice = verticalSlice / np.max(verticalSlice)

    horizontalSlice = horizontalSlice - np.min(horizontalSlice)
    horizontalSlice = horizontalSlice / np.max(horizontalSlice)
    return verticalSlice, horizontalSlice


plt.plot(verticalSlice)
plt.title("Autocorrelation profile (x centered)")
plt.xlabel("Vertical position y [px]")
plt.ylabel("Normalized correlation coefficient [-]")
plt.show()

plt.plot(horizontalSlice)
plt.title("Autocorrelation profile (y centered)")
plt.xlabel("Horizontal position x [px]")
plt.ylabel("Normalized correlation coefficient [-]")
plt.show()

relativeErrorHalfMax = 25

# Y FWHM
print("Y FWHM")
halfMax = 0.5
inferiorBound = halfMax - halfMax * relativeErrorHalfMax / 100
superiorBound = halfMax + halfMax * relativeErrorHalfMax / 100

# Range of values to compute FWHM
pointsForFW = np.where((verticalSlice >= inferiorBound) & (verticalSlice <= superiorBound))[0]
print(pointsForFW)
middlePoint = np.argmax(verticalSlice)  # Find the middle point to separate the values at the left and at the right
left = np.mean(pointsForFW[pointsForFW < middlePoint])
right = np.mean(pointsForFW[pointsForFW > middlePoint])
print(f"left: {left}")
print(f"right: {right}")
FWHM = right - left
print("Diameter : ", FWHM)
print("Radius : ", FWHM / 2)

# X FWHM
print("= = = = = = = = = = = = = = = = = = = = = = = =")
print("X FWHM")
halfMax = 0.5
inferiorBound = halfMax - halfMax * relativeErrorHalfMax / 100
superiorBound = halfMax + halfMax * relativeErrorHalfMax / 100

# Range of values to compute FWHM
pointsForFW = np.where((horizontalSlice >= inferiorBound) & (horizontalSlice <= superiorBound))[0]
print(pointsForFW)
middlePoint = np.argmax(horizontalSlice)  # Find the middle point to separate the values at the left and at the right
left = np.mean(pointsForFW[pointsForFW < middlePoint])
right = np.mean(pointsForFW[pointsForFW > middlePoint])
print(f"left: {left}")
print(f"right: {right}")
FWHM = right - left
print("Diameter : ", FWHM)
print("Radius : ", FWHM / 2)

shape = len(verticalSlice)

x = np.arange(shape)
y = verticalSlice
n = len(x)  # the number of data
mean = sum(x * y) / sum(y)
sigma = np.sqrt(sum(y * (x - mean) ** 2) / sum(y))


def Gauss(x, a, b, c, d):
    return a + (b - a) * np.exp(-(x - c) ** 2 / (2 * d ** 2))


# Following lines: Gaussian fit on the distribution/profile
popt, pcov = curve_fit(Gauss, x, y, p0=[max(y), 1, mean, 1])

plt.plot(x, y, 'b+:', label='data')
plt.plot(x, Gauss(x, *popt), 'r-', label='fit')
plt.legend()
plt.show()
sigma = abs(popt[-1])
FWHM = sigma * 2 * (2 * np.log(2)) ** .5
print(sigma)
print(pcov)
print(FWHM)
