def setEphysParams(cell):
	for sec in cell.all:
		sec.e_pas = -80.398657

	cell.Rm_axosomatic = 20587.734598
	for sec in cell.axosomatic_list:
		sec.cm = 2.230408
	cell.spinefactor = 0.784797
	for seg in cell.soma:
		seg.gbar_nat = 236.616175
	for seg in cell.soma:
		seg.gbar_kfast = 67.197508
	for seg in cell.soma:
		seg.gbar_kslow = 475.820646
	for seg in cell.soma:
		seg.gbar_nap = 1.443953
	
	#for seg in cell.soma:
	#	seg.km.gbar_km = 10.459916
		
	cell.basal.gbar_ih = 11.039583
	cell.tuft.gbar_ih = 16.194815
	cell.tuft.gbar_nat = 47.817841
	cell.decay_kfast = 20.075497
	cell.decay_kslow = 37.711817
	cell.hillock.gbar_nat = 9512.289205
	cell.iseg.gbar_nat = 13326.766938
	cell.iseg.vshift2_nat = -10.612583

	cell.Ra_apical = 382.22414867
	cell.apical.Ra = cell.Ra_apical
	cell.tuft.gbar_sca = 0.45423528
	#for seg in cell.tuft:
	#	seg.sca.vshift = 7.19485311
	cell.tuft.gbar_kca = 6.15058501
	return cell
	