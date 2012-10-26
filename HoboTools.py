# -*- coding: utf-8 -*-
"""
 Tools to handle OnSet HOBO measurements data file
"""
___author___   = 'Cédric Montero'
___contact___  = 'cedric.montero@univ-montp2.fr'
___copyright__ = '2011, Laboratoire de Mécanique et Génie Civil (LMGC)'
___version___  = '0'

""" External modules (preliminary installation could be require) """
import csv
import pylab
import time
import datetime
import numpy

""" Internal modules (local modules files) """

""" Program configurations """

""" Functions definitions """
#TODO : Automatically detect the file information organization according to filecontent[1]
def get_HoboData(path):
	"""
	Read the exported *.txt file from Onset Hobo software
	@param path: path of the file
	@type  path: string 
	"""
	file_content = list(csv.reader(open(path,'rU'), delimiter=';'))	
	date    = []
	data_T  = []
	data_RH = []
	for line in file_content[2::]:
		# Get the date information to datetime format :
		date_structure = time.strptime(line[1],'%d/%m/%Y %H:%M:%S')
		date_instant   = datetime.datetime(*date_structure[0:6])
		date.append(date_instant)
		# Get the temperature and RH measurements :
		data_T.append(float(line[2].replace(',','.')))
		data_RH.append(float(line[3].replace(',','.')))
	# Conversion into numpy array :
	data_T  = numpy.array(data_T)
	data_RH = numpy.array(data_RH)
	return date , data_T, data_RH

