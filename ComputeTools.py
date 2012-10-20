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

def CreateCompositeFromScan(wdname,sfpath,scannumber,roi=((0,0),(512,512))):
	"""
	TODO
	"""
	# TODO : display a statut bar on file number to display or else 
	# TODO : arrange to get the binning value in the roi
	# Create the list of the specified scan :
	filelist = CreateScanDataFileList(wdname,sfpath,scannumber)
	# Create specimen position definition list
	sf = SpecTools.specfile.Specfile(wdname + sfpath)
	scan_command_field = SpecTools.get_ScanCommandField(sf,scannumber)
	scan_command_type = scan_command_field[0].split()[2]
	CompositeArray = fabio.open(filelist[0]).data
	if scan_command_type == 'mesh':
		Motor1   = scan_command_field[0].split()[3]
		Motor2   = scan_command_field[0].split()[7]
		print "Mesh type along (%s,%s)"%(Motor1,Motor2)
		SpecimenPosition = SpecTools.get_ScanMeasurement(sf,scannumber,Motor1)
	elif scan_command_type == 'ascan':
		Motor1 = scan_command_field[0].split()[3]
		SpecimenPosition = SpecTools.get_ScanMeasurement(sf,scannumber,Motor1)
		if SpecimenPosition[1] - SpecimenPosition[0] > 0:
			SpecimenDisplacement = 1#Positive direction
			for imagepath in filelist[1::]:
				imdata = fabio.open(imagepath).data
				CompositeArray = numpy.hstack((CompositeArray,imdata)) 
		else:
			SpecimenDiplacement = -1#Negative direction
	else:
		SpecimenPosition = 0
	return SpecimenPosition,CompositeArray
