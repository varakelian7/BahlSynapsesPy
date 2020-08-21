# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 12:50:51 2020
Modified from Bahl et al 2012
Converted to Python
Added ability to receive synaptic inputs (and/or current injection)
@author: maria_000
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
plotflag=2 # 0: don't open plots. 1: open python plot. 2: open python plot and photo file
batchflag=1

h('{load_file("netparmpi.hoc")}')  # to give each cell its own sequence generator

myTauValue = 0.5 # This is an example of how to modify synaptic parameters
                 # Look in the cellClass file to see how this is used.

fstem="Results" + sltype + simname
print("simname = " + simname + ", fstem = " + fstem)

mytstop = 1200 # ms, length of the simulation

addSynInputs = 1 # 2: synaptic inputs and current injection
				 # 1: synaptic inputs only
				 # 0: current injection only

# parameters for current injection, will be applied if addSynInputs is 0 or 2
injectionLevel = 0.4 # nA
injectionDuration = 500 # ms
injectionStart = 100 # ms


stimPeriod = 125 # ms, the interval between input spikes
                 # from the artificial presynaptic neurons


if addSynInputs>0:
	numExcCells = 2
	numInhDendCells = 2
	numInhSomaCells = 1
else:
	numExcCells = 0
	numInhDendCells = 0
	numInhSomaCells = 0

ntot = numExcCells + numInhDendCells + numInhSomaCells

ncell = ntot + 1

pnm = h.ParallelNetManager(ncell)	# Set up a parallel net manager for all the cells
pc = pnm.pc # Even if running serially, we can create and use this
                         # in serial, pc.nhost == 1
pnm.round_robin()					#Incorporate all processors - cells 0 through ncell-1



#################################
# Make network
#################################
import define_stimcells
import cellClasses

# Create stimulating cells
exc_gid, inh_gid, excStimcell_list, inhDendStimcell_list, inhSomaStimcell_list, cells = define_stimcells.make_stim_cells(pc, numExcCells, numInhDendCells, numInhSomaCells, stimPeriod)

if addSynInputs>0:
    
    # Set incoming spike train
    import numpy as np
    import csv
    # spiketrain = np.loadtxt("spikes1.0", delimiter=",")
    # spiketrain = np.genfromtxt('spikes1.0', delimiter=',')[:,:-1]
    
    from scipy import signal
    
    mydata = np.loadtxt("spiketimes0.060.0.dat", skiprows=1)
    
    #import matplotlib.pyplot as plt
    
    # plt.figure()
    # plt.plot(mydata[:,0], mydata[:,1])
    
    
    pp = signal.find_peaks(mydata[:,1], threshold=-20)
    
    inputtimes = []
    inh_inputtimes = []

    for p in pp[0]:
        #plt.plot(mydata[p,0], mydata[p,1], 'ro')   
        inputtimes.append(mydata[p,0])
        inh_inputtimes.append(mydata[p,0]+3) # inhibitory delay
    
    #plt.show() 
    
    # celltrainlist = []
    # with open("spikes1.0", "r") as f:
    #     filelines = f.readlines()
    #     for line in filelines:
    #         spiketrain = line.split(",")
    #         celltrainlist.append(list(map(float,spiketrain[:-1])))
    
            
    # assuming that each element in celltrainlist
    # is a list of spike times from a single input
    # cell, let's model the effect of the activity
    # from that single input cell onto a visual
    # cortical pyramidal cell as follows:
        
    gidvec = h.Vector(len(inputtimes)) #[exc_gid]*len(celltrainlist[0])    
    gidvec.fill(exc_gid)

        
    inh_gidvec = h.Vector(len(inh_inputtimes)) #[exc_gid]*len(celltrainlist[0])    
    inh_gidvec.fill(inh_gid)
    
    spktimes = h.Vector(len(inputtimes))
    for i,time in enumerate(inputtimes):
        spktimes.x[i] = time
        print(time)

    s = h.PatternStim()    
    s.play(spktimes, gidvec)    
    s.fake_output=1

    inh_spktimes = h.Vector(len(inh_inputtimes))
    for i,time in enumerate(inh_inputtimes):
        inh_spktimes.x[i] = time
        print("inh time =",time)

    inhs = h.PatternStim()    
    inhs.play(inh_spktimes, inh_gidvec)
    inhs.fake_output=1
    print("inh_gid =", inh_gid)


# Create model pyramidal cell
model_cell = cellClasses.reduced_cell_model(myTau=myTauValue)
model_cell.excStimcell_list = excStimcell_list
model_cell.inhDendStimcell_list = inhDendStimcell_list
model_cell.inhSomaStimcell_list = inhSomaStimcell_list


# The next two lines are where you can set which cell to use. Different
# pyramidal cells (and these pyramidal cell models) have slightly
# different electrical personalities (ephys or electrophysiology is the
# technical term for that). You can choose from init_model1, init_model2,
# ...3, 4, 6, 7, 8 in the init_models_with_ca folder, currently.
from init_models_with_ca import init_model1

model_cell = init_model1.setEphysParams(model_cell)
model_cell.recalculate_passive_properties()
model_cell.recalculate_channel_densities()

cells.append(model_cell) # add to list of cells

# # this is an example of altering the resting membrane potential
# for sec in model_cell.all:
# 	sec.e_pas = -83.056442
# h.v_init = -75
# model_cell.recalculate_passive_properties()



# If synaptic inputs were speficied above,
# the lists below will be populates and the
# code will efine synapses on the model pyramidal cell
# and connect stimulating cells to it
nclist = [] #new List()
print("excStimcell_list length = ", len(model_cell.excStimcell_list), " and preExcDend_list length = ", len(model_cell.preExcDend_list))

for r in range(len(model_cell.excStimcell_list)):
	for j in range(len(model_cell.preExcDend_list)): # For each synapse location in the list of excitatory synapses on the dendrite
		syn = model_cell.preExcDend_list[j] # grab the synapse object
		#ncstim = h.NetCon(model_cell.excStimcell_list[r], syn)
		nc = model_cell.excStimcell_list[r].connect2target(syn) # connect the presynaptic cell (excStimcell_list.object(r) to the synapse object on the postsynaptic cell (syn)
		nclist.append(nc)
		
		nc.delay = 3 # ms, the length of the axonal conduction delay and the synaptic delay
		nc.weight[0] = 4*model_cell.excitatory_syn_weight
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
		nc.weight[0] = 0 # model_cell.inhSoma_syn_weight/20
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
# Current injection
#################################

if addSynInputs!=1:
    print("add current injection")
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
