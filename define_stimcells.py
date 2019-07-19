#################################
# Load modules
#################################

import numpy

import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from neuron import h, gui
import simrun
# h.load_file("stdrun.hoc")
# h.load_file("nrngui.hoc") // load_file
# h.nrn_load_dll("./channels/x86_64/.libs/libnrnmech.so")


#################################
# Set parameters
#################################
celsius = 37 # temperature = body temp
sltype="/"
simname = "testcell"
plotflag=1
batchflag=1

myTauValue = 0.5

fstem="Results" + sltype + simname
print("simname = " + simname + ", fstem = " + fstem)

mytstop = 800 # ms, length of the simulation

addSynInputs = 1 # 2: synaptic inputs and current injection
				 # 1: synaptic inputs only
				 # 0: current injection only

stimPeriod = 125

if addSynInputs>0:
	numExcCells = 2
	numInhDendCells = 2
	numInhSomaCells = 1
else:
	numExcCells = 0
	numInhDendCells = 0
	numInhSomaCells = 0

ntot = numExcCells + numInhDendCells + numInhSomaCells


#################################
# Make network
#################################
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


# Create stimulating cells
excStimcell_list, inhDendStimcell_list, inhSomaStimcell_list = make_stim_cells(numExcCells, numInhDendCells, numInhSomaCells, stimPeriod)

# Create model pyramidal cell
model_cell = cellClasses.reduced_cell_model(myTau=myTauValue)
model_cell.excStimcell_list = excStimcell_list
model_cell.inhDendStimcell_list = inhDendStimcell_list
model_cell.inhSomaStimcell_list = inhSomaStimcell_list

from init_models_with_ca import init_model2

model_cell = init_model2.setEphysParams(model_cell)
model_cell.recalculate_passive_properties()
model_cell.recalculate_channel_densities()


# Connect stimulating cells to synapses on the model pyramidal cell

nclist = [] #new List()
print("excStimcell_list length = ", len(model_cell.excStimcell_list), " and preExcDend_list length = ", len(model_cell.preExcDend_list))

for r in range(len(model_cell.excStimcell_list)):
	for j in range(len(model_cell.preExcDend_list)): # For each synapse location in the list of excitatory synapses on the dendrite
		syn = model_cell.preExcDend_list[j] # grab the synapse object
		#ncstim = h.NetCon(model_cell.excStimcell_list[r], syn)
		nc = model_cell.excStimcell_list[r].connect2target(syn) # connect the presynaptic cell (excStimcell_list.object(r) to the synapse object on the postsynaptic cell (syn)
		nclist.append(nc)
		
		nc.delay = 3 # ms, the length of the axonal conduction delay and the synaptic delay
		nc.weight[0] = model_cell.excitatory_syn_weight
		print("adding exc syn from ", r, " to Excitatory synapse #", j)


for r in range(len(model_cell.inhDendStimcell_list)):
	for j in range(len(model_cell.preInhDend_list)): # For each synapse location in the list of inhibitory synapses on the dendrite
		syn = model_cell.preInhDend_list[j] # grab the synapse object
		nc = model_cell.inhDendStimcell_list[r].connect2target(syn) # connect the presynaptic cell (inhDendStimcell_list.object(r) to the synapse object on the postsynaptic cell (syn)
		nclist.append(nc)
		nc.delay = 3 # ms, the length of the axonal conduction delay and the synaptic delay
		nc.weight[0] = model_cell.inhDend_syn_weight
		print("adding inhdend syn from ", r, " to inhibitory dendritic synapse #", j)


for r in range(len(model_cell.inhSomaStimcell_list)):
	for j in range(len(model_cell.preInhSoma_list)): # For each synapse location in the list of inhibitory synapses on the soma
		syn = model_cell.preInhSoma_list[j] # grab the synapse object
		nc = model_cell.inhSomaStimcell_list[r].connect2target(syn) # connect the presynaptic cell (inhSomaStimcell_list.object(r) to the synapse object on the postsynaptic cell (syn)
		nclist.append(nc)
		nc.delay = 3 # ms, the length of the axonal conduction delay and the synaptic delay
		nc.weight[0] = model_cell.inhSoma_syn_weight
		print("adding inhsoma syn from ", r, " to inhibitory somatic synapse #", j)



# Note: the configuration of the for loop decides how many synapses are going to made:
# for r=0, inhSomaStimcell_list.count()-1{
# 	for j=0, preInhSoma_list.count()-1 {
#      ...
#  }
# }
# ===> This allows each stim cell in the list of inhSomaStimcell_list to make a synapse onto every possible synapse location in preInhSoma_list
#
# whereas:
# for j=0, preInhSoma_list.count()-1 {
#  if (j<inhSomaStimcell_list.count()){
#      r = j
#      ...
#  }
# }
# ===> This connects each stim cell in the list of inhSomaStimcell_list to a single, unique synapse in preInhSoma_list
#
# whereas:
# for j=0, preInhSoma_list.count()-1 {
#    r = 0
#    ....
# }
# ===> This connects a single stim cell (the first entry in inhSomaStimcell_list) to every synapse in preInhSoma_list


	
#################################
# Run simulation and record results
#################################
# if plotflag==1:
#	h.load_file("regular_spiking.ses")


# h.load_file("example1.hoc")
soma_v_vec, dend_v_vec, t_vec = simrun.set_recording_vectors(model_cell)
spike_times = [h.Vector() for nc in nclist]
for nc, spike_times_vec in zip(nclist, spike_times):
	nc.record(spike_times_vec)

simrun.simulate(tstop=mytstop)

#################################
# Plot results and write results files
#################################
# h.load_file("produceoutput.hoc")
#for i, spike_times_vec in enumerate(spike_times):
#    print('cell {}: {}'.format(i, list(spike_times_vec)))

simrun.show_output(soma_v_vec, dend_v_vec, t_vec)

#for i, spike_times_vec in enumerate(spike_times):
#    plt.vlines(spike_times_vec, i + 0.5, i + 1.5)
#plt.show()
