# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 11:34:36 2020

@author: maria_000
"""


def setEphysParams(cell):
	for sec in cell.all:
		sec.e_pas = -83.056442

	cell.Rm_axosomatic = 23823.061083
	for sec in cell.axosomatic_list:
		sec.cm = 2.298892
	cell.spinefactor = 0.860211
	for seg in cell.soma:
		seg.gbar_nat = 284.546493
	for seg in cell.soma:
		seg.gbar_kfast = 50.802287
	for seg in cell.soma:
		seg.gbar_kslow = 361.584735
	for seg in cell.soma:
		seg.gbar_nap = 0.873246
	
	for seg in cell.soma:
		seg.gbar_km = 7.123963
		
	cell.basal.gbar_ih = 15.709707
	cell.tuft.gbar_ih = 17.694744
	cell.tuft.gbar_nat = 6.558244
	cell.decay_kfast = 58.520995
	cell.decay_kslow = 42.208044
	cell.hillock.gbar_nat = 8810.657100
	cell.iseg.gbar_nat = 13490.395442
	cell.iseg.vshift2_nat = -9.802976

	cell.Ra_apical = 454.05939784
	cell.apical.Ra = cell.Ra_apical
	cell.tuft.gbar_sca = 3.67649485
	for seg in cell.tuft:
		seg.vshift_sca = 7.4783781
	cell.tuft.gbar_kca = 9.75672674
	return cell
	
# recalculate_passive_properties()
# recalculate_channel_densities()
