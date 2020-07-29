import cellClasses # Define classes


def make_stim_cells(numExc, numInhDend, numInhSoma, stPer): # local i,j  localobj cell, nc, nil
	lcl_excStimcell_list = []
	lcl_inhDendStimcell_list = []
	lcl_inhSomaStimcell_list = []
	
	for r in range (numExc):
		cell = cellClasses.stimcell()
		cell.pp.start = 0
		cell.pp.interval = stPer
		lcl_excStimcell_list.append(cell)

	for r in range (numInhDend):
		cell = cellClasses.stimcell()
		cell.pp.interval = stPer*2
		cell.pp.start = stPer/2
		lcl_inhDendStimcell_list.append(cell)

	for r in range (numInhSoma):
		cell = cellClasses.stimcell()
		cell.pp.interval = stPer*2
		cell.pp.start = stPer/2+stPer
		lcl_inhSomaStimcell_list.append(cell)

	return lcl_excStimcell_list, lcl_inhDendStimcell_list, lcl_inhSomaStimcell_list

