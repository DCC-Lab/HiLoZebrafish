import numpy as np
import matplotlib.pyplot as plt
import tifffile
import os
from scipy.ndimage import gaussian_filter

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
left = np.mean(pointsForFW[np.where(pointsForFW < middlePoint)[-1]])
right = np.mean(pointsForFW[np.where(pointsForFW > middlePoint)[-1]])
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
left = np.mean(pointsForFW[np.where(pointsForFW < middlePoint)[-1]])
right = np.mean(pointsForFW[np.where(pointsForFW > middlePoint)[-1]])
print(f"left: {left}")
print(f"right: {right}")
FWHM = right - left
print("Diameter : ", FWHM)
print("Radius : ", FWHM / 2)
