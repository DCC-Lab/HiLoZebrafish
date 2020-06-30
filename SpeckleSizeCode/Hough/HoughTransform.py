import numpy as np
from matplotlib import pyplot as plt
from cv2 import cv2
import statistics as st
from operator import itemgetter

class HoughImage:

    def __init__(self,path,style='none'):
        self.img = cv2.imread(path,0)
        self.output = self.img.copy()
        self.AvgR = 0
        self.radiusArray = []
        self.detection_cercles = 0
        self.nbCercles = 0
        self.thresh = self.img.copy()
        self.AvgBrightness = 0
        self.median = 0
        self.style = style
    
    def avgScaleVal(self):
        gray = 0 
        pixels = 0
        a,b = self.img.shape 
        for x in range(a):
            for y in range(b):
                gray += self.img[x,y]
                pixels += 1
        self.AvgBrightness = gray // pixels


    def Imaging(self):
        self.avgScaleVal()
        length,width = self.img.shape
        #the filter is not perfect for this section, some images may work better than others. It is possible to play with the
        #integers to get a better contrast depending on the image. They correspond to the change in grayscale value based on the
        #grayscale value of the analysed pixel.
        arrayformedian = []
        dicof = {}
        for i in range(length):
            for j in range(width):
                arrayformedian.append(self.img[i,j])
                if self.img[i,j] not in dicof.keys():
                    dicof[self.img[i,j]] = 1
                else:
                    dicof[self.img[i,j]] = dicof[self.img[i,j]] + 1
        dicof_items = dicof.items()
        sorted_items = sorted(dicof_items) 

        self.median = st.median(arrayformedian)
        maximum = max(arrayformedian)
        minimum = min(arrayformedian)
        rangegr = maximum - minimum
        print(maximum)
        print(minimum)
        print(self.median)
        print(self.AvgBrightness)
        print(dicof)
        print(sorted_items)
        print(length)
        print(width)

        nbpix = length * width
        thresh1 = nbpix * 0.66
        thresh2 = nbpix * 0.87
        thresh3 = nbpix * 0.94
        
        threshvalue = 0
        val1 = 0
        val2 = 0
        val3 = 0
        for colours in sorted_items:
            threshvalue += colours[1]
            if threshvalue >= thresh1 and threshvalue < thresh2 and val1 == 0:
                val1 = colours[0]
            if threshvalue >= thresh2 and threshvalue < thresh3 and val2 == 0:
                val2 = colours[0]
            if threshvalue >= thresh3 and val3 == 0:
                val3 = colours[0]
        
        print(val1)
        print(val2)
        print(val3)
        if self.style == 'full_threshold':
            for i in range(length):
                for j in range(width):
                    if self.img[i,j] > val3 :
                        self.thresh[i,j] = 255
                    if self.img[i,j] <= val3:
                        self.thresh[i,j] = 0
        if self.style == 'none':
            for i in range(length):
                for j in range(width):
                    if self.img[i,j] >= val1 :
                        if self.img[i,j] < val2 :
                            self.thresh[i,j] = self.img[i,j] + 10
                        if self.img[i,j] >val3:
                            self.thresh[i,j] = 255
                        if self.img[i,j] >= val2 and self.img[i,j] <= val3:
                            self.thresh[i,j] = self.img[i,j] + 55
                    if self.img[i,j] < val1:
                        if self.img[i,j] < 10:
                            self.thresh[i,j] = 0
                        else:
                            self.thresh[i,j] = self.img[i,j] - 10
        

    def houghDetect(self):
        self.Imaging()
        # it is possible to play with the values of the HoughCircles method to obtain a better distribution of hough circles.
        # dp is the inverse ratio of resolution, mindist is the minimal distance between the circles, param1 is the upper threshold
        # for the canny edge detector, param2 is the minimal grayscale value for a center to be detected, minRadius is the minimal
        #radius of the circle and the same logic applies to maxRadius. If the min and max values are unknown it is possible to set
        #them to 0
        cercles = cv2.HoughCircles(self.thresh, cv2.HOUGH_GRADIENT, 1, 6, param1=10, param2=8, minRadius=1, maxRadius=6)
        self.detection_cercles = np.uint16(np.around(cercles))
        for (x, y, r) in self.detection_cercles[0, :]:
            cv2.circle(self.output, (x,y), r, (255, 0 , 0), 1)
    
    def circleData(self):
        # I used the emojis as variables to get the average radius value in my array
        self.houghDetect()
        ಠ_ಠ = 0
        ( º_ºノ) = 0
        for (x,y,r) in self.detection_cercles[0, :]:
            ಠ_ಠ += r
            ( º_ºノ) += 1
            self.radiusArray += [r]
        self.AvgR = ಠ_ಠ // ( º_ºノ)
        self.nbCercles = len(self.radiusArray)
    
    def showImage(self, nom):
        self.circleData()
        resized_1 = cv2.resize(self.thresh,(800,800))
        resized_3 = cv2.resize(self.img,(800,800))
        resized_4 = cv2.resize(self.output,(800,800))
        if nom == 'threshold':
            cv2.imshow('treshold output',resized_1)
        if nom == 'image':
            cv2.imshow('input image',resized_3)
        if nom == 'output':
            cv2.imshow('output image',resized_4)
        if nom == 'all':
            cv2.imshow('treshold output',resized_1)
            cv2.imshow('input image',resized_3)
            cv2.imshow('output image',resized_4)
        cv2.waitKey(0)
    
    def showGraph(self):
        self.circleData()
        n,bins,patches = plt.hist(self.radiusArray,bins=np.arange(11)-0.5,facecolor='blue')
        plt.grid(True)
        plt.xlabel('radius in pixels')
        plt.ylabel('number of circles')
        plt.title('Analysis of the speckles in the image with {} circles and an average radius of {} pixels'.format(self.nbCercles,self.AvgR) )
        plt.show()



# enter the path of the image here; make sure that it is a raw string
q = HoughImage(r"C:\Users\ludod\Desktop\Stage_CERVO\speckle_imagery\20190924-SpeckleTest_10X0.4NA\20190924-200ms_20mW_Ave15_Gray_10X0.4_31.tif",style='full_threshold')

q.showGraph()
q.showImage('all')





            