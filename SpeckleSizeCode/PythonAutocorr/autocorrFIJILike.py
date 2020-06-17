import cv2
import numpy as np

from matplotlib import pyplot as plt
import tifffile
import os

nb = 20
fname = rf"20190924-200ms_20mW_Ave15_Gray_10X0.4_{nb}.tif"

p = os.path.dirname(os.path.join(os.getcwd(), "..", ".."))
path = os.path.join(p, "MATLAB", fname)

if path.endswith("tif"):
    img = tifffile.imread(path)
else:
    img = plt.imread(path)
imgNotFocus = plt.imread(path)
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
data = moyenne[np.where(moyenne <= maximum - 2 / 100 * maximum)]

dataNorm = (data - np.min(data))
dataNorm /= np.max(dataNorm)
plt.plot(dataNorm)
plt.show()

halfMax = 0.5
boundsError = 5
inferiorBound = halfMax - halfMax * boundsError / 100
superiorBound = halfMax + halfMax * boundsError / 100
middlePoint = np.argmax(dataNorm)
pointsForFW = np.where((dataNorm >= inferiorBound) & (dataNorm <= superiorBound))[0]
print(pointsForFW)
left = np.mean(pointsForFW[np.where(pointsForFW < middlePoint)[-1]])
right = np.mean(pointsForFW[np.where(pointsForFW > middlePoint)[-1]])
print(f"left: {left}")
print(f"right: {right}")
FWHM = right - left
print(FWHM)

shape = len(dataNorm)
print(shape)

print(2 * shape / FWHM)
