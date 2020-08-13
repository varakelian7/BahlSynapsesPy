import cellClasses # Define classes


def make_stim_cells(pc,numExc, numInhDend, numInhSoma, stPer): # local i,j  localobj cell, nc, nil
    lcl_excStimcell_list = []
    lcl_inhDendStimcell_list = []
    lcl_inhSomaStimcell_list = []
    cells = []
    
    for r in range (numExc):
        cell = cellClasses.stimcell()
        cell.pp.start = -1
        cell.pp.interval = 10000 #stPer
        cell.pp.number = 0 #stPer
        lcl_excStimcell_list.append(cell)
        cells.append(cell)
        exc_gid = len(cells)-1
        nc = cell.connect2target(None)  # attach spike detector to cell
        pc.cell(r+1, nc)  # associate cell's gid with its spike detector

    for r in range (numInhDend):
        cell = cellClasses.stimcell()
        cell.pp.interval = stPer*2
        cell.pp.start = 1e9 # stPer/2
        lcl_inhDendStimcell_list.append(cell)
        cells.append(cell)

    for r in range (numInhSoma):
        cell = cellClasses.stimcell()
        cell.pp.interval = stPer*2
        cell.pp.start = 1e9 # stPer/2+stPer
        lcl_inhSomaStimcell_list.append(cell)
        cells.append(cell)

    return exc_gid, lcl_excStimcell_list, lcl_inhDendStimcell_list, lcl_inhSomaStimcell_list, cells

