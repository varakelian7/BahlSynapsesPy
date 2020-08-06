from neuron import h
#import matplotlib
#matplotlib.use("Agg") # matplotlib.use('module://ipykernel.pylab.backend_inline')
from matplotlib import pyplot

def set_recording_vectors(cell,nclist):
    """Set soma, dendrite, and time recording vectors on the cell.

    :param cell: Cell to record from.
    :return: the soma, dendrite, and time vectors as a tuple.
    """
    soma_v_vec = h.Vector()   # Membrane potential vector at soma
    dend_v_vec = h.Vector()   # Membrane potential vector at dendrite
    tuft_v_vec = h.Vector()   # Membrane potential vector at dendrite
    t_vec = h.Vector()        # Time stamp vector
    soma_v_vec.record(cell.soma(0.5)._ref_v)
    dend_v_vec.record(cell.apical(0.5)._ref_v)
    tuft_v_vec.record(cell.tuft(0.5)._ref_v)
    t_vec.record(h._ref_t)

    # spike_times = [h.Vector() for nc in nclist]
    # for nc, spike_times_vec in zip(nclist, spike_times):
    # 	nc.record(spike_times_vec)
    cell._spike_detector = h.NetCon(cell.soma(0.5)._ref_v, None, sec=cell.soma)
    cell.spike_times = h.Vector()
    cell._spike_detector.record(cell.spike_times)
        
    
    return soma_v_vec, dend_v_vec, tuft_v_vec, t_vec, cell.spike_times

def simulate(tstop=25):
    """Initialize and run a simulation.

    :param tstop: Duration of the simulation.
    """
    h.tstop = tstop
    h.stdinit()
    h.run()

import sys
import subprocess

def saveopenimage(pyplot,filename, plotflag):
    pyplot.savefig(filename) #figure()
    if plotflag==2:
        imageViewerFromCommandLine = {'linux':'xdg-open','linux2':'xdg-open','win32':'explorer','darwin':'open'}[sys.platform]
        subprocess.call([imageViewerFromCommandLine,filename.replace("/", "\\")])

def show_output(soma_v_vec, dend_v_vec, tuft_v_vec, t_vec, spike_times, plotflag, fstem, new_fig=True):
    """Draw the output.

    :param soma_v_vec: Membrane potential vector at the soma.
    :param dend_v_vec: Membrane potential vector at the dendrite.
    :param t_vec: Timestamp vector.
    :param new_fig: Flag to create a new figure (and not draw on top
            of previous results)
    """
    if new_fig:
        pyplot.figure(figsize=(8,4)) # Default figsize is (8,6)
    soma_plot = pyplot.plot(t_vec, soma_v_vec, color='black')
    dend_plot = pyplot.plot(t_vec, dend_v_vec, color='blue')
    tuft_plot = pyplot.plot(t_vec, tuft_v_vec, color='red')

    pyplot.legend(soma_plot + dend_plot + tuft_plot, ['soma', 'apical(0.5)', 'tuft(0.5)'])
    pyplot.xlabel('time (ms)')
    pyplot.ylabel('mV')

    saveopenimage(pyplot, fstem+"_soma_and_dend.png", plotflag)
    
    if plotflag>0:
        pyplot.show()
        
    
    pyplot.figure()
    i=1
    if (spike_times.size()>0):
        pyplot.vlines(spike_times, i + 0.5, i + 1.5)
    pyplot.xlabel('time (ms)')
    pyplot.ylabel('Cell #')
    pyplot.ylim([0,5])

    saveopenimage(pyplot, fstem+"_spikeraster.png", plotflag)
    
    if plotflag>0:
        pyplot.show()
