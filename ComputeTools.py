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

def CreateCompositeFromScan(wdname,sf,scannumber,roi=((0,0),(512,512))):
	"""
	TODO
	"""
	# TODO : display a statut bar on file number to display or else 
	# TODO : arrange to get the binning value in the roi
	# TODO : arrange this to fill in the composite according to positions
	# Create the list of the specified scan :
	filelist = CreateScanDataFileList(wdname,sf,scannumber)
	print filelist[0]
	print filelist[-1]
	# Retrieve the size of the image :
	ImShape = fabio.open(filelist[0]).data.shape
	print ImShape
	ImSize = ImShape #Necessary for ROI implementation
	# Create specimen position definition list
	scan_command_field = SpecTools.get_ScanCommandField(sf,scannumber)
	scan_command_type = scan_command_field.split()[2]
	if scan_command_type == 'mesh':
		# Get the number of images :
		MeshShape = (int(scan_command_field.split()[6])+1,int(scan_command_field.split()[10])+1)
		# Create an zero array of the composite image :
		CompositeArray = numpy.zeros((MeshShape[0]*ImShape[0],MeshShape[1]*ImShape[1]))
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
			CompositeArray[0+idx1*ImSize[0]:(ImSize[0]-1)+idx1*ImSize[0]+1,0+idx2*ImSize[1]:(ImSize[1]-1)+idx2*ImSize[1]+1] = imdata
			idx = idx+1
	"""if scan_command_type == 'mesh':
		Motor1   = scan_command_field.split()[3]
		Motor2   = scan_command_field.split()[7]
		print "Mesh type along (%s,%s)"%(Motor1,Motor2)
		SpecimenPosition1 = SpecTools.get_ScanMeasurement(sf,scannumber,Motor1)
		SpecimenPosition2 = SpecTools.get_ScanMeasurement(sf,scannumber,Motor2)
		print SpecimenPosition1,SpecimenPosition2
		SpecimenPosition = [SpecimenPosition1,SpecimenPosition2]
		#idx = 1 
		#for impath in filelist[1::]:
	#		Disp1 = SpecimenPosition1[idx] - SpecimenPosition1[idx-1]
	#		Disp2 = SpecimenPosition2[idx] - SpecimenPosition2[idx-1]
	#		imdata = fabio.open(impath).data
	#		if Disp1 < 0 and Disp2 == 0:# Following horizontal line
	#			CompositeArray = numpy.hstack((CompositeArray,imdata))
	#		if Disp1 > 0 and Disp2 > 0:
	#			CompositeArray = numpy.vstack((CompositeArray,imdata))
	#		idx = idx+1
	elif scan_command_type == 'ascan':
		Motor1 = scan_command_field[0].split()[3]
		SpecimenPosition = SpecTools.get_ScanMeasurement(sf,scannumber,Motor1)
		if SpecimenPosition[1] - SpecimenPosition[0] > 0:
			SpecimenDisplacement = 1#Positive direction
			for imagepath in filelist[1::]:
				imdata = fabio.open(imagepath).data
				CompositeArray = numpy.hstack((CompositeArray,imdata)) 
		else:
			SpecimenDisplacement = -1#Negative direction
	else:
		SpecimenPosition = 0
	"""
	return SpecimenPosition,CompositeArray
