# Some tips to use the python scripts in this folder to plot Transmission Vs Wavelength graphs
- Make sure that the file that contains the data you are trying to plot is a text file.
- Make sure there is no line of text at the beginning and at the end of the file.
- The decimal mark must be a decimal point. If your data contain decimal commas, use the Ctrl + H function of the note pad to replace all commas with points.
- By default, any consecutive whitespaces act as delimiter. If the string used to separate values is anything but whitespace, use np.genfromtxt to load your data and specify the delimiter.
