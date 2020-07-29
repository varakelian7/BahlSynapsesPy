# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 11:34:36 2020

@author: maria_000
"""


def setEphysParams(cell):
	for sec in cell.all:
		sec.e_pas = -80.495767

	cell.Rm_axosomatic = 20513.848207
	for sec in cell.axosomatic_list:
		sec.cm = 2.411070
	cell.spinefactor = 0.691767
	for seg in cell.soma:
		seg.gbar_nat = 238.879842
	for seg in cell.soma:
		seg.gbar_kfast = 59.256783
	for seg in cell.soma:
		seg.gbar_kslow = 433.798677
	for seg in cell.soma:
		seg.gbar_nap = 1.479049
	
	#for seg in cell.soma:
	#	seg.km.gbar_km = 11.118662
		
	cell.basal.gbar_ih = 10.720289
	cell.tuft.gbar_ih = 17.796075
	cell.tuft.gbar_nat = 29.006481
	cell.decay_kfast = 55.581656
	cell.decay_kslow = 88.716317
	cell.hillock.gbar_nat = 8302.875131
	cell.iseg.gbar_nat = 17623.525167
	cell.iseg.vshift2_nat = -9.567698

	cell.Ra_apical = 4.44130503e+02
	cell.apical.Ra = cell.Ra_apical
	cell.tuft.gbar_sca = 2.12343632e+00
	#for seg in cell.tuft:
	#	seg.sca.vshift = 8.34639038e+00
	cell.tuft.gbar_kca = 8.22978203e+00
	return cell
	
# recalculate_passive_properties()
# recalculate_channel_densities()
