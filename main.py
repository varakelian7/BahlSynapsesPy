# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 12:50:51 2020
Modified from Bahl et al 2012
Converted to Python
Added ability to receive synaptic input
(and/or current injection)
@author: marianne.bezaire@gmail.com
"""
#################################
# Load modules
#################################

from neuron import h
import simrun
h.load_file("stdrun.hoc")
h.load_file("nrngui.hoc") # load_file


#################################
# Set parameters
#################################
h.celsius = 37 # temperature = body temp
sltype="/"
simname = "testcell"
plotflag=2 # 0: don't open plots. 1: open python plot.
           # 2: open python plot and photo file
           
batchflag=1
fstem="Results" + sltype + simname
print("simname = " + simname + ", fstem = " + fstem)


# Parameter to set the decay time constant of GABA_A
# synapses onto the pyramidal neuron
myTauValue = 3 # This is an example of (one way to) 
                 # how to modify synaptic parameters
                 # Look at (approx) line 77 in this
                 # file to see how this parameter is
                 # passed to the cell; then look in 
                 # the cellClass file to trace the
                 # usage to the specific synapse
                 # that references this parameter
                 #
                 # You may implement a similar strategy
                 # to change other parameters in the model


mytstop = 800 # ms, length of the simulation

addSynInputs = 1 # 2: synaptic inputs and current injection
				 # 1: synaptic inputs only
				 # 0: current injection only

# parameters for current injection, will be applied if addSynInputs is 0 or 2
injectionLevel = 0.4 # nA
injectionDuration = 500 # ms
injectionStart = 100 # ms


stimPeriod = 125 # ms, the interval between input spikes
                 # from the artificial presynaptic neurons


#################################
# Design network
#################################

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
import define_stimcells
import cellClasses

# Create stimulating cells
excStimcell_list, inhDendStimcell_list, inhSomaStimcell_list, cells = define_stimcells.make_stim_cells(numExcCells, numInhDendCells, numInhSomaCells, stimPeriod)

# Create model pyramidal cell
model_cell = cellClasses.reduced_cell_model(myTau=myTauValue)
model_cell.excStimcell_list = excStimcell_list
model_cell.inhDendStimcell_list = inhDendStimcell_list
model_cell.inhSomaStimcell_list = inhSomaStimcell_list


# The next few lines are where you can set which model pyramidal cell
# to use. Different pyramidal cells (and these pyramidal cell models)
# have slightly different electrical personalities (ephys or 
# electrophysiology is the technical term for that). You can choose
# from init_model1, init_model2, ...3, 4, 6, 7, 8 in the 
# init_models_with_ca folder, currently.

from init_models_with_ca import init_model1

# create and initialize a new cell of this model type
model_cell = init_model1.setEphysParams(model_cell)
model_cell.recalculate_passive_properties()
model_cell.recalculate_channel_densities()

cells.append(model_cell) # add this new cell to a list of created cells

# # this is an example of altering the resting membrane potential of the
# # cell by iterating over all sections in the cell and setting the
# # reversal potential of the leak channels (which are always active)
# for sec in model_cell.all:
# 	sec.e_pas = -83.056442

# # And now setting the starting membrane potential of the cell
# h.v_init = -75

# # Now, recalculate the other electrical properties now that the 
# # resting membrane potential has been changed.
# model_cell.recalculate_passive_properties()



# If synaptic inputs were specified above,
# the lists below will be populated and the
# code will define synapses on the model pyramidal cell
# and connect stimulating cells to it
nclist = [] #new List()
print("excStimcell_list length = ", len(model_cell.excStimcell_list), 
      " and preExcDend_list length = ", len(model_cell.preExcDend_list))

for r in range(len(model_cell.excStimcell_list)): # For each artificial 
        # stimulating cell that synapses onto this type of location,
	for j in range(len(model_cell.preExcDend_list)): # For each synapse
            # location in the list of excitatory synapses on the dendrite

        # grab the synapse object
		syn = model_cell.preExcDend_list[j]
		#ncstim = h.NetCon(model_cell.excStimcell_list[r], syn)
        
        # connect the presynaptic cell (excStimcell_list.object(r)
        # to the synapse object on the postsynaptic cell (syn)
		nc = model_cell.excStimcell_list[r].connect2target(syn) 
		nclist.append(nc) # add the synaptic connection object to a list
		
		nc.delay = 3 # ms, axonal conduction delay + synaptic delay
		nc.weight[0] = model_cell.excitatory_syn_weight # synaptic weight 
		print("adding exc syn from ", r, " to Excitatory synapse #", j)


for r in range(len(model_cell.inhDendStimcell_list)):
	for j in range(len(model_cell.preInhDend_list)): # For each synapse location in the list of inhibitory synapses on the dendrite
		syn = model_cell.preInhDend_list[j] # grab the synapse object
		nc = model_cell.inhDendStimcell_list[r].connect2target(syn) # connect the presynaptic cell (inhDendStimcell_list.object(r) to the synapse object on the postsynaptic cell (syn)
		nclist.append(nc)
		nc.delay = 3 # ms, axonal conduction delay + synaptic delay
		nc.weight[0] = model_cell.inhDend_syn_weight # synaptic weight
		print("adding inhdend syn ", r, " to inhibitory dendritic synapse #", j)


for r in range(len(model_cell.inhSomaStimcell_list)):
	for j in range(len(model_cell.preInhSoma_list)): # For each synapse location in the list of inhibitory synapses on the soma
		syn = model_cell.preInhSoma_list[j] # grab the synapse object
		nc = model_cell.inhSomaStimcell_list[r].connect2target(syn) # connect the presynaptic cell (inhSomaStimcell_list.object(r) to the synapse object on the postsynaptic cell (syn)
		nclist.append(nc)
		nc.delay = 3 # ms, axonal conduction delay + synaptic delay
		nc.weight[0] = model_cell.inhSoma_syn_weight # synaptic weight
		print("adding inhsoma syn from ", r, " to inhibitory somatic synapse #", j)



# # Note: Regarding the connection-making code above,
# # the configuration of the for loop decides how many 
# # synapses are going to made. Currently, it will loop over
# # each artificial stimulating cell that exists (these cells
# # were created using the define_stimcells module earlier).
# # For each artificial stimulating cell, another for loop will
# # loop over each synapse on the model cell that is included
# # in a list of synapses meant to receive input from that
# # stimulating cell.
# # Within the inner for loop, code can be added to connect the
# # artificial stimulating cell to the particular synapse on the
# # model cell.
#
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
# Current injection
#################################

if addSynInputs!=1:
    stimobj = h.IClamp(model_cell.soma(0.5))
    stimobj.delay = injectionStart # ms, time after start of sim when you want the current injection to begin
    stimobj.dur = injectionDuration # ms, duration of current pulse
    stimobj.amp = injectionLevel # nA
    # stimobj.i # nA, contains the level of current being injected at any given time during simulation   


#################################
# Run simulation and record results
#################################

soma_v_vec, dend_v_vec, tuft_v_vec, t_vec, spike_times = simrun.set_recording_vectors(model_cell, nclist)

simrun.simulate(tstop=mytstop)

#################################
# Plot results and write results files
#################################
    
with open("{}_spikes.dat".format(fstem), 'w') as f:
    f.write("{}\t{}\n".format("time","cell"))
    i=1
    for spk in spike_times:
        f.write("{:.2f}\t{}\n".format(spk, i))

with open("{}_voltages.dat".format(fstem), 'w') as f:
    f.write("{}\t{}\t{}\t{}\n".format("time", "soma_v", "apical_v", "tuft_v"))
    for i, v in enumerate(soma_v_vec):
        f.write("{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}\n".format(i*h.dt, v, dend_v_vec[i], tuft_v_vec[i]))


simrun.show_output(soma_v_vec, dend_v_vec, tuft_v_vec, t_vec, spike_times, plotflag, fstem)
