# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 13:34:04 2020

@author: maria_000
"""


import numpy as np
import csv
# spiketrain = np.loadtxt("spikes1.0", delimiter=",")
# spiketrain = np.genfromtxt('spikes1.0', delimiter=',')[:,:-1]

celltrainlist = []
with open("spikes1.0", "r") as f:
    filelines = f.readlines()
    for line in filelines:
        spiketrain = line.split(",")
        celltrainlist.append(list(map(float,spiketrain[:-1])))
        
# assuming that each element in celltrainlist
# is a list of spike times from a single input
# cell, let's model the effect of the activity
# from that single input cell onto a visual
# cortical pyramidal cell as follows:
    
    
