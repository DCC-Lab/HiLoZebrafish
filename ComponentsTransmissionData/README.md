# Some tips to use python scripts to plot graphs
- Make sure that the file that contains the data you are trying to plot is a **text file**.
- Make sure there is no line of text at the beginning and at the end of the file.
- The decimal mark must be a **decimal point**. If your data contain decimal commas, use the Ctrl + H function of the note pad to replace all commas with points.
- By default, any consecutive whitespaces act as delimiter. If the string used to separate values is anything but whitespace, use np.genfromtxt to load your data and specify the delimiter.
- When loading your files with np.loadtxt or np.genfromtxt, you need to specify which columns to read using **usecols**, with 0 being the first.
- You can edit axis, curves and image parameters using matplotlib functions like xlim, xticks, xlabel, etc. and use *plt.show* to look at the modifications.
- When you are ready to save your figure in *pdf*, comment the `plt.show` line and uncomment the `fig.savefig('FigureName.pdf', bbox_inches='tight', dpi=600)` line (where, obviously, `FigureName` is your figure name). Run the script and your figure is now saved in *pdf* in the same folder as the python script.
