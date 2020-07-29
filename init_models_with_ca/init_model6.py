# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 11:34:36 2020

@author: maria_000
"""


def setEphysParams(cell):
	for sec in cell.all:
		sec.e_pas = -84.998432

	cell.Rm_axosomatic = 15158.600592
	for sec in cell.axosomatic_list:
		sec.cm = 2.708710
	cell.spinefactor = 0.500131
	for seg in cell.soma:
		seg.gbar_nat = 295.471939
	for seg in cell.soma:
		seg.gbar_kfast = 43.229568
	for seg in cell.soma:
		seg.gbar_kslow = 630.252495
	for seg in cell.soma:
		seg.gbar_nap = 3.524026
	
	#for seg in cell.soma:
	#	seg.km.gbar_km = 11.911267
		
	cell.basal.gbar_ih = 12.871974
	cell.tuft.gbar_ih = 23.929821
	cell.tuft.gbar_nat = 45.917053
	cell.decay_kfast = 65.606365
	cell.decay_kslow = 34.325297
	cell.hillock.gbar_nat = 9451.076984
	cell.iseg.gbar_nat = 17193.545673
	cell.iseg.vshift2_nat = -8.920295

	cell.Ra_apical = 4.45008826e+02
	cell.apical.Ra = cell.Ra_apical
	cell.tuft.gbar_sca = 4.86650161e-01
	#for seg in cell.tuft:
	#	seg.sca.vshift = 7.95615680e-01
	cell.tuft.gbar_kca = 9.68514833e+00
	return cell
	
# recalculate_passive_properties()
# recalculate_channel_densities()
