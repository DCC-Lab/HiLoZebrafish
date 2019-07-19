import numpy as np
import matplotlib.pyplot as plt

filename1 = "ExperimentOptotuneDiffuser.txt"
filename2 = "diffuserTransmissionTheoretical.txt"

distanceDiffuserScreen1 = 36  # mm
distanceDiffuserScreen2 = 46  # mm
distanceDiffuserScreen3 = 50  # mm
distanceDiffuserScreen4 = 60  # mm
distanceDiffuserScreen5 = 70  # mm

x1 = np.loadtxt(filename1, usecols=0)
y1 = np.loadtxt(filename1, usecols=1)
y2 = np.loadtxt(filename1, usecols=2)
y3 = np.loadtxt(filename1, usecols=3)
y4 = np.loadtxt(filename1, usecols=4)
y5 = np.loadtxt(filename1, usecols=5)
a6 = np.loadtxt(filename2, usecols=0)
y6 = np.loadtxt(filename2, usecols=1)

a1 = np.degrees(np.arctan((np.array(x1) - x1[-1]/2)/distanceDiffuserScreen1)) + 4
y1n = np.array(y1)/max(y1)
a2 = np.degrees(np.arctan((np.array(x1) - x1[-1]/2)/distanceDiffuserScreen2)) + 4
y2n = np.array(y2)/max(y2)
a3 = np.degrees(np.arctan((np.array(x1) - x1[-1]/2)/distanceDiffuserScreen3)) + 2.22
y3n = np.array(y3)/max(y3)
a4 = np.degrees(np.arctan((np.array(x1) - x1[-1]/2)/distanceDiffuserScreen4)) + 2.22
y4n = np.array(y4)/max(y4)
a5 = np.degrees(np.arctan((np.array(x1) - x1[-1]/2)/distanceDiffuserScreen5)) + 2.22
y5n = np.array(y5)/max(y5)

Data0, = plt.plot(a1, y1n, color='k', label='Grit 1500 3.6 cm')
Data1, = plt.plot(a2, y2n, color='k', label='Grit 1500 4.6 cm', linestyle='--')
Data2, = plt.plot(a3, y3n, color='b', label='Optotune Diffuser 5 cm')
Data3, = plt.plot(a4, y4n, color='g', label='Optotune Diffuser 6 cm')
Data4, = plt.plot(a5, y5n, color='r', label='Optotune Diffuser 7 cm')
Data5, = plt.plot(a6, y6, color='k', label='Thorlabs Data', linestyle=':')
plt.xlim([a3[0], a3[-1]])
plt.ylim([0, 1.05])
plt.yticks(fontsize=16)
plt.xticks(fontsize=16)
plt.xlabel("Output Angle [°]", fontsize=18)
plt.ylabel("Normalized gray value (Laser power = 5 mW) [-]", fontsize=18)
plt.grid(False)
plt.legend(handles=[Data0, Data1, Data2, Data3, Data4, Data5], fontsize=16)
plt.minorticks_on()
fig = plt.gcf()
fig.set_size_inches(12, 7)
#fig.savefig('graphDiffuser1500gritPowermeter.pdf', bbox_inches='tight', dpi=600)
plt.show()