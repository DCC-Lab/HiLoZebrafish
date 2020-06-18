import cv2
import numpy as np

from matplotlib import pyplot as plt
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

dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
f_shift = np.fft.fftshift(dft)
f_complex = f_shift[:, :, 0] + 1j * f_shift[:, :, 1]
f_abs = np.abs(f_complex) + 1  # lie between 1 and 1e6
f_bounded = 20 * np.log(f_abs)
f_img = 255 * f_bounded / np.max(f_bounded)
plt.imshow(np.log(f_abs))
plt.show()

f = f_img

somme = np.sum(f, 1)
moyenne = np.mean(f, 0)

maximum = np.max(moyenne)
data = moyenne[moyenne < maximum]

dataNorm = (data - np.min(data))
dataNorm /= np.max(dataNorm)

dataNorm = data

halfMax = 0.5
halfMax = np.mean([dataNorm[0], dataNorm[-1]])
halfMax = (np.max(dataNorm) + halfMax) / 2
print(halfMax)

plt.plot(dataNorm)
plt.show()

boundsError = 5
inferiorBound = halfMax - halfMax * boundsError / 100
superiorBound = halfMax + halfMax * boundsError / 100
middlePoint = np.argmax(dataNorm)
pointsForFW = np.where((dataNorm >= inferiorBound) & (dataNorm <= superiorBound))[0]
print(pointsForFW)
left = np.mean(pointsForFW[pointsForFW < middlePoint])
right = np.mean(pointsForFW[pointsForFW > middlePoint])
print(f"left: {left}")
print(f"right: {right}")
FWHM = right - left
print(FWHM)

shape = len(dataNorm)
print(shape)

print(2 * shape / FWHM)

x = np.arange(shape)
y = dataNorm
n = len(x)  # the number of data
mean = sum(x * y) / sum(y)
sigma = np.sqrt(sum(y * (x - mean) ** 2) / sum(y))


def Gauss(x, a, b, c, d):
    return a + (b - a) * np.exp(-(x - c) ** 2 / (2 * d ** 2))


popt, pcov = curve_fit(Gauss, x, y, p0=[max(y), 1, mean, sigma])

plt.plot(x, y, 'b+:', label='data')
plt.plot(x, Gauss(x, *popt), 'r-', label='fit')
plt.legend()
plt.show()
print(abs(popt[-1]))
