# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 11:34:36 2020

@author: maria_000
"""

def setEphysParams(cell):
	for sec in cell.all:
		sec.e_pas = -80.735127

	cell.Rm_axosomatic = 11594.384797
	for sec in cell.axosomatic_list:
		sec.cm = 2.336857
	cell.spinefactor = 0.500000
	for seg in cell.soma:
		seg.gbar_nat = 402.172079
	for seg in cell.soma:
		seg.gbar_kfast = 41.351830
	for seg in cell.soma:
		seg.gbar_kslow = 264.787820
	for seg in cell.soma:
		seg.gbar_nap = 4.179878
	
	#for seg in cell.soma:
	#	seg.km.gbar_km = 14.917361
		
	cell.basal.gbar_ih = 11.921506
	cell.tuft.gbar_ih = 15.266638
	cell.tuft.gbar_nat = 11.555568
	cell.decay_kfast = 91.798929
	cell.decay_kslow = 75.607992
	cell.hillock.gbar_nat = 8030.326751
	cell.iseg.gbar_nat =17591.201145
	cell.iseg.vshift2_nat = -5.982169

	cell.Ra_apical = 358.47
	cell.apical.Ra = cell.Ra_apical
	cell.tuft.gbar_sca = 3.86
	#for seg in cell.tuft:
	#	seg.sca.vshift = 3.79
	cell.tuft.gbar_kca = 9.60
	return cell

# recalculate_passive_properties()
# recalculate_channel_densities()
