# -*- coding: utf-8 -*-
"""
 Modul help
"""
___author___   = 'Cédric Montero'
___contact___  = 'cedric.montero@esrf.fr'
___copyright__ = '2012, ESRF'
___version___  = '0'

""" External modules (preliminary installation could be require) """
import SpecTools
import fabio
import numpy
""" Internal modules (local modules files) """


""" Program configurations """

""" Functions definitions """
def CreateScanDataFileList(wdname,sf,scannumber):
	"""
	Create the list of localized file from specfile scan number specified
	@param     wdname: main working path directory containing DATA/, PROCESS/ and REPORT/ folders afterward
	@type      wdname: string
	@param         sf: specfile informations
	@type          sf: specfile object
	@param scannumber: number of the scan data to find out
	@type  scannumber: string
	"""
	# Original ESRF directory name of files
	odname   = SpecTools.get_ScanValueInSpecHeaderComment(sf,scannumber,'#C qq.adet.dname')
	# Equivalent directory name in the path
	edname   = odname.split('/')
	# Set the last directory specified in wdname as the key to set the equivalency
	keydname = wdname.split('/')[-2]
	# Position of edname in the odname field
	poskey   = int([pos for pos in range(len(odname.split('/'))) if odname.split('/')[pos] == keydname][0])
	fdname   = wdname + '/'.join(odname.split('/')[poskey+1::]) + '/'#Directory of the files
	nbmeas   = sf.select(str(scannumber)).data().shape[1]#Number of measurements recorded (can be different from expected in the command if user stop the scan)
	fprefix  = SpecTools.get_ScanValueInSpecHeaderComment(sf,scannumber,'#C qq.adet.prefix')
	filelist = [fdname + fprefix + str(val).zfill(4) + '.edf' for val in range(0,nbmeas)]
	return filelist

def CreateCompositeFromScan(wdname,sf,scannumber,background=None,roi=((0,0),(512,512))):
	"""
	Create a composite image of a large 2D nparray obtained during a mesh or a scan
	@param     wdname: working directory name
	@type      wdname: string
	@param         sf: specfile object
	@type          sf: specfile object
	@param scannumber: number of the scan to use
	@type  scannumber: string or integer
	@param background: set a background image compatible with the images size of the scan
	@type  background: numpy 2D array
	@param        roi: tuple of region of interest in the image
	@type         roi: tuple of 2 tuple of integer
	"""
	# TODO : display a statut bar on file number to display or else 
	# TODO : arrange to get the binning value in the roi
	# TODO : arrange this to fill in the composite according to positions
	# Create the list of the specified scan :
	filelist = CreateScanDataFileList(wdname,sf,scannumber)
	#print filelist[0]
	#print filelist[-1]
	# Retrieve the size of the image :
	ImShape = fabio.open(filelist[0]).data.shape
	# Handle background image :
	if background == None:
		print "No background specified !"
		background = numpy.zeros(ImShape)
	ImSize = ImShape #Necessary for ROI implementation
	# Create specimen position definition list
	scan_command_field = SpecTools.get_ScanCommandField(sf,scannumber)
	scan_command_type = scan_command_field.split()[2]
	if scan_command_type == 'mesh':
		# Get the number of images :
		MeshShape = (int(scan_command_field.split()[6])+1,int(scan_command_field.split()[10])+1)
		# Create an zero array of the composite image :
		CompositeArray = numpy.zeros((MeshShape[0]*ImSize[0],MeshShape[1]*ImSize[1]))
		print "Empty Composite image of (%i,%i) shape created."%(CompositeArray.shape[0],CompositeArray.shape[1])
		# Get the positions of each image along Motor1 and Motor2
		Motor1   = scan_command_field.split()[3]
		Motor2   = scan_command_field.split()[7]
		SpecimenPosition1 = SpecTools.get_ScanMeasurement(sf,scannumber,Motor1)
		SpecimenPosition2 = SpecTools.get_ScanMeasurement(sf,scannumber,Motor2)
		SpecimenPosition = [SpecimenPosition1,SpecimenPosition2]
		Min1 = min(SpecimenPosition1)
		Max1 = max(SpecimenPosition1)
		Min2 = min(SpecimenPosition2)
		Max2 = max(SpecimenPosition2)
		Delta1 = round((Max1-Min1)/(MeshShape[0]-1),3)# [nm]
		Delta2 = round((Max2-Min2)/(MeshShape[1]-1),3)# [nm]
		idx = 0# Number of the file in the list
		for impath in filelist[0::]:
			Deltax1 = round(SpecimenPosition1[idx] - min(SpecimenPosition1),3)
			Deltax2 = round(SpecimenPosition2[idx] - min(SpecimenPosition2),3)
			idx1 = int(Deltax1 / Delta1)
			idx2 = int(Deltax2 / Delta2)
			imdata = fabio.open(impath).data
			CompositeArray[0+idx1*ImSize[0]:(ImSize[0]-1)+idx1*ImSize[0]+1,0+idx2*ImSize[1]:(ImSize[1]-1)+idx2*ImSize[1]+1] = imdata - background
			idx = idx+1
	elif scan_command_type == 'ascan':
		ScanShape = int(scan_command_field.split()[6])+1
		Motor = scan_command_field.split()[3]
		if Motor == 'nny' or 'stry':
			# Case of horizontal scan : 
			SpecimenPosition = SpecTools.get_ScanMeasurement(sf,scannumber,Motor)
			if SpecimenPosition[1] - SpecimenPosition[0] > 0:
				CompositeArray = fabio.open(filelist[0]).data
				for impath in filelist[0::]:
					imdata = fabio.open(impath).data
					CompositeArray = numpy.hstack([CompositeArray,imdata])
			elif SpecimenPosition[1] - SpecimenPosition[0] < 0:
				CompositeArray = fabio.open(filelist[0]).data
				for impath in filelist[0::]:
					imdata = fabio.open(impath).data
					CompositeArray = numpy.hstack([imdata,CompositeArray])
		if Motor == 'nnz' or 'strz':
			# Case of vertical scan : 
			SpecimenPosition = SpecTools.get_ScanMeasurement(sf,scannumber,Motor)
			if SpecimenPosition[1] - SpecimenPosition[0] > 0:
				CompositeArray = fabio.open(filelist[0]).data
				for impath in filelist[0::]:
					imdata = fabio.open(impath).data
					CompositeArray = numpy.vstack([CompositeArray,imdata])
			elif SpecimenPosition[1] - SpecimenPosition[0] < 0:
				CompositeArray = fabio.open(filelist[0]).data
				for impath in filelist[0::]:
					imdata = fabio.open(impath).data
					CompositeArray = numpy.vstack([imdata,CompositeArray])
	return SpecimenPosition,CompositeArray


def CreateAverageFromScan(wdname,sf,scannumber):
	"""
	Create an average of all files of the scan (used for ex. for background determination)
	@param wdname : working directory name
	@type wdname : string
	@param sf: specfile object
	@type sf: specfile object
	"""
	filelist = CreateScanDataFileList(wdname,sf,scannumber)
	nbfiles = len(filelist)
	CompositeArray = fabio.open(filelist[0]).data
	for impath in filelist[1::]:
		imdata = fabio.open(impath).data
		CompositeArray = CompositeArray + imdata
	CompositeArray = numpy.divide(CompositeArray,float(nbfiles))
	return CompositeArray

if __name__ == "__main__":
	wdname = '/Users/labo/Folder/ESRF/DATA/d_2012-07-29_inh_hygro-wood/'
	sfpath_mat = 'DATA/sample1/sample1.dat'
	import sys
	sys.path.append('.'+'/Tools/')
	import SpecTools
	sf_mat = SpecTools.specfile.Specfile(wdname + sfpath_mat)
	ScanBackAt55pc = '9'
	Back = CreateAverageFromScan(wdname,sf_mat,ScanBackAt55pc)
	scannumber = '6'
	SpecimenPos, Composite = CreateCompositeFromScan(wdname,sf_mat,scannumber,background=Back)
	import DisplayTools
	DisplayTools.display_image_from_array(Composite)
	#scannumber = '9'
	#CreateAverageFromScan(wdname,sf_mat,scannumber)
