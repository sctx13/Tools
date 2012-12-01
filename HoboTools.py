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

def display_env_data(Time,Temp,RH):
	"""
	Display double Y axis with temperature and relative humidity
	@param Time : instant of measurements
	@type  Time : 1d nparray of datetime values
	@param Temp : measurement of the temperature
	@type  Temp : 1d nparray size like parameter Time with float64 values
	@param   RH : measurements of the relative humidity
	@type    RH : 1d nparray size like parameter Time with float64 values
	"""
	import pylab
	pylab.ion()
	fig = pylab.figure(figsize=(8,4))
	pylab.title('Hygrothermal environment near sample along the experiment')
	ax1 = fig.add_subplot(111)
	ax1.plot(Time,Temp,'rx',markersize=1,label='Temperature')
	ax1.set_xlabel('Date [calendar]')
	ax1.set_ylabel('Temperature ['u'\u00B0''C]',color='r')
	#ax1.set_ylim((21,23))
	for tl in ax1.get_yticklabels():
		tl.set_color('r')
	ax2=ax1.twinx()
	ax2.plot(Time,RH,'bx',markersize=1,label='RH')
	ax2.set_ylabel('Relative Humidity [%]',color='b')
	#ax2.set_ylim((40,60))
	for tl in ax2.get_yticklabels():
		tl.set_color('b')
	pylab.grid(True)



