# -*- coding: utf-8 -*-
"""
 Module to bring display tools for diffraction images
"""
___author___   = 'Cédric Montero'
___contact___  = 'cedric.montero@esrf.fr'
___copyright__ = '2012, ESRF'
___version___  = '0'

""" External modules (preliminary installation could be require) """
import fabio
import numpy
import pylab

""" Internal modules (local modules files) """

""" Program configurations """
pylab.ion()

""" Functions definitions """
#TODO : colormap selector window that apear when a display is called.
def display_image_from_edffile(filepath):
	nparray = fabio.open(filepath).data
	pylab.figure()
	#Display array with grayscale intensity and no pixel smoothing interpolation
	pylab.imshow(numpy.log(nparray),cmap='binary',interpolation='nearest',origin='lower')
	pylab.axis('off')

def display_image_from_array(nparray,colory='binary',roi=None):
	"""
	Produce a display of the nparray 2D matrix
	@param nparray : image to display
	@type nparray : numpy 2darray
	@param colory : color mapping of the image (see http://www.scipy.org/Cookbook/Matplotlib/Show_colormaps)
	@type colory : string
	"""
	#Set the region of interest to display :
	#  (0,0) is set at lower left corner of the image
	if roi == None:
		roi = ((0,0),nparray.shape)
		nparraydsp = nparray
		print roi
	elif type(roi[0])==tuple and type(roi[1])==tuple: 
		# Case of 2 points definition of the domain : roi = integers index of points ((x1,y1),(x2,y2))
		print roi
		nparraydsp = nparray[roi[0][0]:roi[1][0],roi[0][1]:roi[1][1]]
	elif type(roi[0])==int and type(roi[1])==int:	
		# Case of image centered domain : roi = integers (width,high)
		nparraydsp = nparray[int(nparray.shape[0]/2)-int(roi[0])/2:int(nparray.shape[0]/2)+int(roi[0])/2,int(nparray.shape[1]/2)-int(roi[1])/2:int(nparray.shape[1]/2)+int(roi[1])/2]
	fig = pylab.figure()
    #Display array with grayscale intensity and no pixel smoothing interpolation
	pylab.imshow(numpy.log(nparraydsp),cmap=colory,interpolation='nearest')#,origin='lower')
	pylab.axis('off')

# Using PIL
import Image
def display_PIL(nparray):
	image = Image.fromarray(nparray,'I;16')
	image.show()


"""
def display_histogram(filepath):
	



def display_image_thresholded(filepath):
	nparray = fabio.open(filepath).data
	pylab.figure()
    #Display array with grayscale intensity and no pixel smoothing interpolation
    pylab.imshow(nparray,cmap='gray',interpolation='nearest')
    pylab.axis('off')
    pylab.colorbar()
"""
