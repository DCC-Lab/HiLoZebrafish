from labjack import ljm
import numpy as np
import time
import matplotlib.pyplot as mpl
from scipy import signal
import traceback
import sys
import argparse

from labjackcontrol import *
#from calibration_functions import *
from signal_processing_functions import *

parser = argparse.ArgumentParser(prog='Labjack T7 470010370 controller debug version',description='''Outputs a sine wave of a given frequency that is used to control the Optotune Lens Driver 4. Needs scipy to run for spike detection. You will also need drivers for labjack T7 and LJM interpreter. The program can always be broken with a keyboard interrupt (ctrl-c)''',epilog='''Version 1.0''')
parser.add_argument('-v',"--verbosity",help ='Increase verbosity',default=0, action="count")
parser.add_argument('-fq',type=int,help='Frequency of sine wave in Hz. Defaults to 90 Hz',nargs='?',default=90)
parser.add_argument('-wvfrmres',type=int,help='Periods per 127 dots. Defaults to 1.',nargs='?',default=1)
parser.add_argument('-readsize',type=float,help='Waveforms scanned by each read function. Proportionnal to size of data packet sent. Defaults to 3.',default=3)
parser.add_argument('-readnum',type=int,help='Number of times the read function is called. Is infinite by default',default=float('inf'))
parser.add_argument('-amp',type=float,help='Amplitude of oscillation. Defaults to 0.5',nargs='?',default=0.5)
parser.add_argument('-offset',type=float, help='Voltage around where the oscillation takes place.',default=3.75)
parser.add_argument('-nocalib', help ='Allows calibration of offset voltage', action = 'store_false', default=True)
parser.add_argument('-compar', help ='Gives a visual of the exit voltage', action = 'store_true', default=False)
args = parser.parse_args()

#Paramters for acquisition (shortcut variables)
fqreal = int(args.fq/float(args.wvfrmres))
scanres = args.readsize * 127
scanrate = fqreal*127


if int(args.fq/float(args.wvfrmres)) != args.fq/float(args.wvfrmres):
	raise AssertionError('Waveform resolution not multiple of frequency')
if args.readnum <= 1:
	raise AssertionError('Must read stream more than once for stability')
if args.compar == True and args.readnum>=10000:
	raise AssertionError('Cannot give visual for very large loop')

if __name__ == "__main__":
	#Opening labjack and generating handle object
	try:
		handle = ljm.openS("T7","ETHERNET","470010370")
	except ljm.LJMError: 
		print('Could not open labjack \n Program is terminated') 
		sys.exit()
	try:
		if args.nocalib==False:
			val = initialise_sinus(args.wvfrmres,args.amp, args.offset)
		else:
			val = initialise_sinus(args.wvfrmres,args.amp,offset_calibration(handle,args.verbosity))

		initialise_streamout(handle,val)

		#Start streaming. 4800 is Stream-Out. 0 is Stream-In
		if args.verbosity > 0: print("Streaming initiated")
		
		ljm.eStreamStart(handle,scanres,2,[4800,0],scanrate)

		data = mainloop_reading(handle,scanres,args.readnum,args.verbos)

	#Error catching
	except ljm.LJMError:
		print("LJM Error break")
	except Exception:
		print("System error break")
		print(traceback.format_exc())
		sys.exit()
	except KeyboardInterrupt:
		if args.verbosity > 0 : print("\n User called break")
	try:
		ljm.eStreamStop(handle)
		if args.verbosity > 0: print("Streaming finished")
	except ljm.LJMError: 
		print('Could not stop stream')
	try:
		ljm.close(handle)
		if args.verbosity >0: print("Labjack closed")
	except ljm.LJMError: 
		print('Could not close labjack')
		sys.exit()
	

	if args.compar == True:
		#Initialising x-axis for plotting
		plotspace = np.linspace(0,((args.readnum-1)*args.readsize)/(float(fqreal)),scanres*(args.readnum-1))
		plotspace2 = np.linspace(0,(1)/(float(args.fq)),127/args.wvfrmres)

		#Converting theoritical sine wave to square wave

		theofunction = np.sin(np.linspace(0,args.wvfrmres*(2*np.pi)*(args.readnum-1)*args.readsize, scanres*(args.readnum-1)))
		square = [1 if x>=np.mean(theofunction) else 0 for x in theofunction]

		#Visualisation of the peaks and function created
		spectrum = np.fft.fft(data)
		freqseq = np.fft.fftfreq(len(spectrum),1/float(scanrate))
		spectrum[np.where(np.logical_or(np.less(abs(freqseq),args.fq*0.9),np.greater(abs(freqseq),args.fq*30)))] = 0
		spectrum = spectrum * np.exp(-np.power(freqseq - (args.fq+2*args.fq)/2 , 2.) / (2 * np.power(300, 2.)))
		datamod = np.real(np.fft.ifft(spectrum))
		peak = np.zeros(len(data))
		peak[peak_detect_periodic(data,args.fq,scanrate,sensibility=0)] = 5

		mpl.plot(plotspace, square)
		mpl.plot(plotspace, normalize_set(data,square))
		mpl.plot(plotspace, normalize_set(datamod,square))
		mpl.plot(plotspace, normalize_set(peak,square))
		mpl.show()