import numpy as np
import matplotlib.pyplot as plt

filename1 = "Filter_BA510-550\\Transmission_1_510550.txt"
filename2 = "Filter_500-590\\Transmission_5_500590.txt"
# filename3 = "Filter_500-590\\Transmission_6_500590.txt"
# filename4 = "Filter_500-590\\Transmission_7_500590.txt"

x1 = np.loadtxt(filename1, usecols=0)
y1 = np.loadtxt(filename1, usecols=1)

x2 = np.loadtxt(filename2, usecols=0)
y2 = np.loadtxt(filename2, usecols=1)

# x3 = np.loadtxt(filename2, usecols=0)
# y3 = np.loadtxt(filename2, usecols=1)
#
# x4 = np.loadtxt(filename2, usecols=0)
# y4 = np.loadtxt(filename2, usecols=1)

Data0, = plt.plot(x1, y1, color='k', label='Filter 510-550')
Data1, = plt.plot(x2, y2, color='b', label='Filter 500-590')
# Data2, = plt.plot(x3, y3, color='g', label='third')
# Data3, = plt.plot(x4, y4, color='y', label='fourth')
plt.xlim([450, 650])
plt.ylim([0, 100])
plt.yticks(fontsize=16)
plt.xticks(fontsize=16)
plt.xlabel("Wavelength [nm]", fontsize=18)
plt.ylabel("Transmission [%]", fontsize=18)
# plt.grid(True)
plt.legend(handles=[Data0, Data1], fontsize=18)
plt.minorticks_on()
fig = plt.gcf()
fig.set_size_inches(12, 7)
#fig.savefig('graphdiffuser.pdf', bbox_inches='tight', dpi=600)
plt.show()