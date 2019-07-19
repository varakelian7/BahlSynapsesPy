from neuron import h
import matplotlib
matplotlib.use("Agg") # matplotlib.use('module://ipykernel.pylab.backend_inline')
from matplotlib import pyplot

def set_recording_vectors(cell):
    """Set soma, dendrite, and time recording vectors on the cell.

    :param cell: Cell to record from.
    :return: the soma, dendrite, and time vectors as a tuple.
    """
    soma_v_vec = h.Vector()   # Membrane potential vector at soma
    dend_v_vec = h.Vector()   # Membrane potential vector at dendrite
    t_vec = h.Vector()        # Time stamp vector
    soma_v_vec.record(cell.soma(0.5)._ref_v)
    dend_v_vec.record(cell.apical(0.5)._ref_v)
    t_vec.record(h._ref_t)
    return soma_v_vec, dend_v_vec, t_vec

def simulate(tstop=25):
    """Initialize and run a simulation.

    :param tstop: Duration of the simulation.
    """
    h.tstop = tstop
    h.run()

import sys
import subprocess

def saveopenimage(pyplot,filename):
    pyplot.savefig(filename) #figure()
    imageViewerFromCommandLine = {'linux':'xdg-open','linux2':'xdg-open','win32':'explorer','darwin':'open'}[sys.platform]
    subprocess.call([imageViewerFromCommandLine,filename])

def show_output(soma_v_vec, dend_v_vec, t_vec, new_fig=True):
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
    dend_plot = pyplot.plot(t_vec, dend_v_vec, color='red')

    pyplot.legend(soma_plot + dend_plot, ['soma', 'apical(0.5)'])
    pyplot.xlabel('time (ms)')
    pyplot.ylabel('mV')

    saveopenimage(pyplot, "soma_and_dend.png")
