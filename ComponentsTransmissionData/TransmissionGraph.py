import numpy as np
import matplotlib.pyplot as plt

filename1 = "Filter_BA510-550\\Transmission_1_510550.txt"
filename2 = "Filter_500-590\\Transmission_5_500590.txt"

x1 = np.loadtxt(filename1, usecols=0)
y1 = np.loadtxt(filename1, usecols=1)

x2 = np.loadtxt(filename2, usecols=0)
y2 = np.loadtxt(filename2, usecols=1)

Data0, = plt.plot(x1, y1, color='k', label='Filter 510-550')
Data1, = plt.plot(x2, y2, color='b', label='Filter 500-590')
plt.xlim([450, 650])
plt.ylim([0, 100])
plt.yticks(fontsize=16)
plt.xticks(fontsize=16)
plt.xlabel("Wavelength [nm]", fontsize=18)
plt.ylabel("Transmission [%]", fontsize=18)
plt.grid(False)
plt.legend(handles=[Data0, Data1], fontsize=18)
plt.minorticks_on()
fig = plt.gcf()
fig.set_size_inches(12, 7)
#fig.savefig('graphdiffuser.pdf', bbox_inches='tight', dpi=600)
plt.show()