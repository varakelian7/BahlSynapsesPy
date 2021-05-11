# BahlSynapsesPy

This is a model of a single pyramidal cell with realistic morphology and ion channels.

It has been modified to specify either an input from an electrode or synaptic inputs.

It will simulate the cell's response to the inputs and record the membrane potential at the soma and in the cell dendrites. Then it will save a picture of a plot of the membrane potential with time.

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
