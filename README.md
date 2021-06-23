# BahlSynapsesPy

This is a model of a single pyramidal cell with realistic morphology and ion channels, based on one of the pyramidal cell models from:
Bahl A, Stemmler MB, Herz AV, Roth A (2012) [Automated optimization of a reduced layer 5 pyramidal cell model based on experimental data.](https://www.sciencedirect.com/science/article/pii/S016502701200129X?via%3Dihub) *J Neurosci Methods* 210:22-34. Original code is available in ModelDB, [#146026](https://senselab.med.yale.edu/ModelDB/ShowModel?model=146026).

The code has been converted to NEURON+Python and modified to specify either an input from an electrode or synaptic inputs.

The model will simulate the cell's response to the inputs and record the membrane potential at the soma and in the cell dendrites. Then the code will save a picture of a plot of the membrane potential with time.

## Download and Install
Using GitHub Desktop:
1. Go to File > Clone repository ... 
2. Click the "URL" tab
3. In the Repository URL field, enter: https://github.com/risecourse/BahlSynapsesPy
4. Click the "Clone" button
* If it asks "How are you planning to use this fork?", select "For my own purposes" and click the button
5. This repository will now be the current repository in your GitHub Desktop. Hover your mouse over the "current repository" tab in the upper left part of GitHub Desktop, where the name of this repository is listed, and a tooltip should appear that gives the location of this repository on your computer. Take note of the location
6. In a terminal (if necessary, a pre-configured bash terminal in the NEURON directory), cd to the repository's directory and then enter `nrnivmodl` or `mknrndll` (if on Windows) to compile the ion channel mechanisms
7. Open Spyder (or another Python IDE)
8. Select File > Open and navigate to the location of the repository. Open the main.py file and take a look

Other options:
1. Click the button in the mid/upper right of the GitHub repository to download or clone this repository to your computer.
2. Select an option to download the zip file if you don't have Git or GitHub desktop installed. If you have Git (even if not GitHub Desktop), you can select the option to clone the repository to your local machine.
3. Expand the zip file
4. Continue from step 6 above


## Usage
You can run the main.py file to produce two output plots in Spyder. You may wish to customize some parameters in the "Set parameters" section of main.py to change properties of the cell or the stimulation (synaptic input versus current injection) or whether plots are displayed or saved as image files.

### Outputs
This simulation produces two types of data, the spike times of the pyramidal cell and the membrane potential traces for various parts of the cell. These outputs are produced as figures in python (optional), images of the figures, and text files of the data:
- \[simname\]\_spikes.dat
- \[simname\]\_voltages.dat

### Parameters
You may wish to add or customize parameters in the "Set parameters" section of main.py to change properties of the cell or the stimulation (synaptic input versus current injection) or whether plots are displayed or saved as image files. The following parameters are defined:
- **h.celsius** *Float*. Temperature of the model system in Celsius. This is a standard NEURON parameter
- **sltype** *String*. Forward or backward (Windows) slash for paths
- **simname** *String*. Unique name for simulation; the code will create a directory with this name to store the simulation results
- **plotflag** *Integer*. Controls plotting behavior of the simulation. Options are: 
  - 0 = don't open plots
  - 1 = open python plots
  - 2 = open python plots and photo files
- **batchflag** *Boolean*. Whether this simulation is being run as part of a batch of simulations:
  - 1 = part of batch
  - 0 = single simulation

- **myTauValue** *Float*. The rise time constant in ms of one of the synapses onto the model cell. (An example parameter; users can add their own similar to this)

- **mytstop** *Float*. Length of the simulation in milliseconds

- **addSynInputs** *Integer*. The type of simulation used in the model:
  - 2 = synaptic inputs and current injection
  - 1 = synaptic inputs only
  - 0 = current injection only

There are additional parameters for the current injection stimulation; they are relevant if addSynInputs = 0 or 2:
- **injectionLevel** *Float*. Amplitude of the current injection in nA (nanoAmps)
- **injectionDuration** *Float*. Duration of the current injection in ms (milliseconds)
- **injectionStart** *Float*. Start time (onset) of the current injection in ms

There is an additional parameter for the synaptic input stimulation, relevant if addSynInputs = 1;
- **stimPeriod** *Float*. The interval in ms between input spikes from the artificial presynaptic neurons

