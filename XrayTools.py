# -*- coding: utf-8 -*-
"""
 Modul help
"""
___author___   = 'Cédric Montero'
___contact___  = 'cedric.montero@esrf.fr'
___copyright__ = '2012, European Synchrotron Radiation Facility (ESRF)'
___version___  = '0'

""" External modules (preliminary installation could be require) """
import numpy

""" Functions definitions """
def bragg_TTh_to_d(wavelength,TTharray):
    """
    Convertor from two theta angle value [deg] to lattive spacing value [nm]
    @param Tharray : 2Theta array [deg]
    @type Tharray : numpy 1D array
    @param wavelength: wavelength value [nm]
    @type wavelength: float
    @return lattice: lattice spacing value(s) [nm]
    @type lattice: float or numpy 1D array
    """
    lattice = wavelength/(2*numpy.sin(numpy.radians(TTharray/2)))
    return lattice

def bragg_d_to_TTh(wavelength,d):
    """
    Covertor from lattice spacing value [nm] to two theta angle [deg]
    @param d: d-spacing value [nm]
    @type  d: float or numpy 1D array
    @param wavelength: wavelength [nm]
    @type wavelength: float
    @return TTh: Two theta value(s) [deg]
    @type TTh : float or numpy 1D array
    """
    TTh = numpy.degrees(2*numpy.arcsin(wavelength/(2*d)))
    return TTh

