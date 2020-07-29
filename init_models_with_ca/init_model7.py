# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 11:34:36 2020

@author: maria_000
"""


def setEphysParams(cell):
	for sec in cell.all:
		sec.e_pas = -83.681797

	cell.Rm_axosomatic = 21298.371768
	for sec in cell.axosomatic_list:
		sec.cm = 2.371953
	cell.spinefactor = 0.548509
	for seg in cell.soma:
		seg.gbar_nat = 447.254408
	for seg in cell.soma:
		seg.gbar_kfast = 43.784070
	for seg in cell.soma:
		seg.gbar_kslow = 190.331780
	for seg in cell.soma:
		seg.gbar_nap = 0.852072
	
	#for seg in cell.soma:
	#	seg.km.gbar_km = 11.049652
		
	cell.basal.gbar_ih = 3.121003
	cell.tuft.gbar_ih = 40.673635
	cell.tuft.gbar_nat = 0.408584
	cell.decay_kfast = 82.070143
	cell.decay_kslow = 65.182920
	cell.hillock.gbar_nat = 8171.378905
	cell.iseg.gbar_nat = 19582.667257
	cell.iseg.vshift2_nat = -5.357797

	cell.Ra_apical = 332.92
	cell.apical.Ra = cell.Ra_apical
	cell.tuft.gbar_sca = 2.81
	#for seg in cell.tuft:
	#	seg.sca.vshift = 2.35
	cell.tuft.gbar_kca = 9.55
	return cell

# recalculate_passive_properties()
# recalculate_channel_densities()
