# Define types of model cells here
# so that instances (objects based on them)
# can be created in main.py after loading in
# this file

# The classes defined below include:
# reduced_cell_model: the pyramidal cell model
# stimcell: an artificial cell that synapses onto
#            the pyramidal cell and that can spike
#            during the simulation, activating a 
#            postsynaptic current in the pyramidal cell.
#            Note: Excitatory and inhibitory stimulating
#            cells can both be created from this cell class.
#            The difference is which synapse on the post-
#            synaptic pyramidal cell you connect them to

from neuron import h
import math
  
class stimcell():
    def __init__(self):
        self.is_art=1
        self.noiseFromRandom=0
        self.gid=[]
        self.x=0
        self.y=0
        self.z=0

        pp = h.MyNetStim(.5)
        pp.interval = 1000/8 # Gives an 8 Hz rhythm with an interval of 125 ms
        pp.number = 1e9
        pp.noise = 0 # 0 = no noise, same interval every time. 1 = maximum noise, variable interval with poisson mean of 125 ms                
        pp.start = 0
        self.pp = pp

    def is_art(self):
        return 1

    def setnoiseFromRandom(self,ranstream):
        self.noiseFromRandom(ranstream)
    
    def connect2target(self, target, thresh=-10):
        nc = h.NetCon(self.pp, target)
        nc.threshold = thresh
        
        #self.spike_times = []
        #vecrecs = []
        #vecrecs.append(h.Vector())
        #nc.record(vecrecs[0])
        #self.nclist.append(nc)
        #self.spike_times.append(vecrecs[0])

        return nc
        
    def position(self,xp,yp,zp):
        self.x = xp
        self.y = yp
        self.z = zp    
        xpos = xp
        ypos = yp
        zpos = zp    
        #self.pp.position(xpos, ypos, zpos)
        
class reduced_cell_model():
    def __init__(self,myTau=0.5):
        self.soma = None
        self.x = 0; self.y = 0; self.z = 0
        self.create_sections()
        self.build_topology()
        self.build_subsets()
        self.define_geometry()
        self.define_biophysics()
        self.addSynapses(myTau)

    def create_sections(self):
        self.soma = h.Section(name='soma', cell=self)
        self.basal = h.Section(name='basal', cell=self)
        self.apical = h.Section(name='apical', cell=self)
        self.tuft = h.Section(name='tuft', cell=self)
        self.hillock = h.Section(name='hillock', cell=self)
        self.iseg = h.Section(name='iseg', cell=self)
        self.axon = h.Section(name='axon', cell=self)

    def    build_topology(self):
        self.basal.connect(self.soma(0.5))
        self.apical.connect(self.soma(1))
        self.tuft.connect(self.apical(1))
        self.hillock.connect(self.soma(0))
        self.iseg.connect(self.hillock(1))
        self.axon.connect(self.iseg(1))        


    def recalculate_geometry(self):
        self.soma.diam = self.soma.L =  math.sqrt(self.soma_area/self.PI)
        self.basal.diam = self.basal_area/self.PI/self.basal.L    
        self.apical.diam = self.diam_apical    
        self.tuft.diam = self.tuft_area/self.PI/self.tuft.L

    def define_geometry(self):
        self.soma_area = 1682.96028429
        self.basal_area = 7060.90626796
        self.apicalshaftoblique_area = 9312.38528764
        self.tuft_area = 9434.24861189
        self.PI  = 3.1415926535897932384

        # Set spatial resolution of sections
        self.soma.nseg = 1
        self.basal.nseg = 1
        self.apical.nseg = 5
        self.tuft.nseg = 2
        self.hillock.nseg = 5
        self.iseg.nseg = 5
        self.axon.nseg = 1

        # Set dimensions of the sections
        self.basal.L     = 257   
        self.apical.L = 500
        self.tuft.L = 499
        self.hillock.L = 20
        self.axon.L = 500
        self.iseg.L = 25
        self.axon.diam = 1.5
        
        self.iseg.diam = 1.75
        self.hillock.diam = 2.75
        # for seg in self.iseg:
        #     seg.diam = 2.0 - seg.x*.5
            
        # for seg in self.hillock:
        #     seg.diam = 3.5 - seg.x*1.5
            
        #self.iseg.diam=1.8 #(0:1) = 2.0:1.5
        #self.hillock.diam=2.8 #(0:1) = 3.5:2.0

        self.diam_apical = self.apicalshaftoblique_area/self.PI/self.apical.L
        self.recalculate_geometry()
        
    def build_subsets(self):
        self.all = h.SectionList()
        self.all.wholetree(sec=self.soma)

    def recalculate_passive_properties(self):
        for sec in self.axosomatic_list:
            sec.g_pas = 1./self.Rm_axosomatic
            
        for sec in self.apicaltree_list:
            sec.g_pas = self.soma.g_pas*self.spinefactor 
            sec.cm = self.soma.cm*self.spinefactor

    def recalculate_channel_densities(self):        
        # See Keren et al. 2009        
        h.distance(sec=self.soma)
        
        for sec in self.apicaltree_list:
            based = h.distance(self.soma(0),sec(0))
            for seg in sec:
                seg.gbar_kfast = self.soma(0.5).gbar_kfast * math.exp(-(seg.x*sec.L+based)/self.decay_kfast)
                seg.gbar_kslow = self.soma(0.5).gbar_kslow * math.exp(-(seg.x*sec.L+based)/self.decay_kslow)

        d = h.distance(self.soma(0),self.tuft(0))
        if d>0:
            mih = self.tuft.gbar_ih/d
            mnat = (self.tuft.gbar_nat-self.soma(0.5).gbar_nat)/d
        else:
            mih = self.tuft.gbar_ih/self.apical.L
            mnat = (self.tuft.gbar_nat-self.soma(0.5).gbar_nat)/self.apical.L
            
        based = h.distance(self.soma(0),self.apical(0))
        for seg in self.apical.allseg():
            seg.gbar_nat = mnat*(seg.x*self.apical.L+based) + self.soma(0.5).gbar_nat
            seg.gbar_ih = mih*(seg.x*self.apical.L+based)

    def define_biophysics(self):
        self.Rm_axosomatic = 15000
        self.spinefactor = 2.0

        self.decay_kfast = 50.0
        self.decay_kslow = 50.0

        self.soma.Ra =  82
        self.basal.Ra = 734 
        self.tuft.Ra = 527

        Ra_apical = 261
        self.apical.Ra =  Ra_apical

        self.hillock.Ra = self.soma.Ra
        self.axon.Ra = self.soma.Ra
        self.iseg.Ra = self.soma.Ra

        for sec in self.all: # 'all' defined in build_subsets
            sec.insert('pas')
            sec.cm = 1.0
            sec.g_pas = 1./15000
            sec.e_pas = -70
        
        for sec in self.ih_list:
            sec.insert('ih')
            for seg in sec:
                seg.ehd_ih = -47

        for sec in self.nat_list:
            sec.insert('nat')
            sec.ena = 55
            sec.vshift_nat = 10

        for sec in self.kfast_list:
            sec.insert('kfast')
            sec.ek = -80

        for sec in self.kslow_list:
            sec.insert('kslow')
            sec.ek = -80

        self.soma.insert('nap')
        self.soma.insert('km')

        self.tuft.insert('cad')
        self.tuft.insert('sca')
        self.tuft.insert('kca')
        self.tuft.eca = 140
        h.ion_style("ca_ion",0,1,0,0,0)

        self.recalculate_passive_properties()
        self.recalculate_channel_densities()
        #self.tuft.gbar_sca = 3.67649485*10 # TODO what is this


    ######################/

    #Define Section lists
    def build_subsets(self):
        """Build subset lists. For now we define 'all'."""
        self.all = h.SectionList()
        self.all.wholetree(sec=self.soma)

        # morphological section lists
        self.axon_list = []
        self.axosomatic_list = []
        self.apicalshaftoblique_list = []
        self.apicaltree_list = []
        self.tuft_list = []
        self.soma_list = []
        self.basal_list = []

        self.axon_list.append(self.hillock)
        self.axon_list.append(self.iseg)
        self.axon_list.append(self.axon)

        self.axosomatic_list.append(self.soma)
        self.axosomatic_list.append(self.basal)
        self.axosomatic_list.append(self.hillock)
        self.axosomatic_list.append(self.iseg)
        self.axosomatic_list.append(self.axon)

        self.apicalshaftoblique_list.append(self.apical)

        self.apicaltree_list.append(self.apical)
        self.apicaltree_list.append(self.tuft)

        self.tuft_list.append(self.tuft)

        self.soma_list.append(self.soma)

        self.basal_list.append(self.basal)

    # Create lists of cell parts that contain each ion channel type
        self.nat_list = []
        self.kslow_list = []
        self.kfast_list = []
        self.ih_list = []

        self.ih_list.append(self.basal)
        self.ih_list.append(self.apical)
        self.ih_list.append(self.tuft)
        
        self.excsyn_list = []
        self.inhdendsyn_list = []
        self.inhsomasyn_list = []

        self.excsyn_list.append(self.basal)
        self.excsyn_list.append(self.apical)
        self.excsyn_list.append(self.tuft)

        self.inhdendsyn_list.append(self.basal)
        self.inhdendsyn_list.append(self.apical)

        self.inhsomasyn_list.append(self.soma)

        self.nat_list.append(self.soma)
        self.nat_list.append(self.hillock)
        self.nat_list.append(self.iseg)
        self.nat_list.append(self.apical)
        self.nat_list.append(self.tuft)

        self.kfast_list.append(self.soma)
        self.kfast_list.append(self.apical)
        self.kfast_list.append(self.tuft)

        self.kslow_list.append(self.soma)
        self.kslow_list.append(self.apical)
        self.kslow_list.append(self.tuft)

    def recordData(self):
        self._spike_detector = h.NetCon(self.soma(0.5)._ref_v, None, sec=self.soma)
        self.spike_times = h.Vector()
        self._spike_detector.record(self.spike_times)

    def addSynapses(self,myTauValue):
    # Define synapses in various areas of the cell
    #   and set the connection parameters (synapse
    # rise time, decay time, reversal potential,
    # conductance/weight).
    # Also create lists of synapses onto the model cell:
    #    excsyn_list: excitatory synapses onto the cell
    #    inhdendsyn_list: inhibitory synapses onto the cell dendrites
    #    inhsomasyn_list: inhibitory synapses onto the cell body    objref preInhSoma_list, preInhDend_list, preExcDend_list
        self.preInhSoma_list = []
        self.preInhDend_list = []
        self.preExcDend_list = []

        s=0
        self.recInhSomaCurrent = []
        for sec in self.inhsomasyn_list:
            syn_ = h.MyExp2Syn(sec(0.5))
            self.preInhSoma_list.append(syn_)    # GABA_A Synapses onto Cell Body
            syn_.tau1 = myTauValue # synaptic rise time constant in ms
            syn_.tau2 = 3 # synaptic decay time constant in ms
            syn_.e = -70 # reversal potential of the synaptic current


            self.recInhSomaCurrent.append(h.Vector())    
            self.recInhSomaCurrent[s].record(self.preInhSoma_list[s]._ref_i)

            #sprint(cmdstr,"objref recInhSomaCurrent%d", s)
            #{execute(cmdstr)}
            #sprint(cmdstr,"recInhSomaCurrent%d = new Vector()", s)
            #{execute(cmdstr)}
            #sprint(cmdstr,"recInhSomaCurrent%d.record(&preInhSoma_list.object(%d).i)", s, s)
            #{execute(cmdstr)}
            s = s + 1

        totInhSoma = s

        s = 0
        self.recInhDendCurrent = []
        for sec in self.inhdendsyn_list:
            syn_ = h.MyExp2Syn(sec(0.5))
            self.preInhDend_list.append(syn_)    # GABA_A Synapses onto Cell Dendrites
            syn_.tau1 = 0.5 # synaptic rise time constant in ms
            syn_.tau2 = 3 # synaptic decay time constant in ms
            syn_.e = -70 # reversal potential of the synaptic current
            self.recInhDendCurrent.append(h.Vector())        
            self.recInhDendCurrent[s].record(self.preInhDend_list[s]._ref_i)

            #sprint(cmdstr,"recInhDendCurrent%d = new Vector()", s)
            #sprint(cmdstr,"recInhDendCurrent%d.record(&preInhDend_list.object(%d).i)", s, s)
            s = s + 1

        totInhDend = s

        s = 0
        self.recExcCurrent = []
        for sec in self.excsyn_list:
            syn_ = h.MyExp2Syn(sec(0.5))
            self.preExcDend_list.append(syn_)    # AMPA Synapse
            syn_.tau1 = 1 # synaptic rise time constant in ms
            syn_.tau2 = 5 # synaptic decay time constant in ms
            syn_.e = 0 # reversal potential of the synaptic current
            self.recExcCurrent.append(h.Vector())
            self.recExcCurrent[s].record(self.preExcDend_list[s]._ref_i)

            #sprint(cmdstr,"objref recExcCurrent%d", s)
            #{execute(cmdstr)}
            #sprint(cmdstr,"recExcCurrent%d = new Vector()", s)
            #{execute(cmdstr)}
            #sprint(cmdstr,"recExcCurrent%d.record(&preExcDend_list.object(%d).i)", s, s)
            #{execute(cmdstr)}
            s = s + 1

        self.totExc = s

        # Synaptic conductances (max)
        self.excitatory_syn_weight = 0.005 # the maximum synaptic conductance in microSiemens, aka the synaptic amplitude, of the excitatory connections
        self.inhDend_syn_weight = 0.003 # the maximum synaptic conductance of the inhibitory connections onto the dendrites
        self.inhSoma_syn_weight = 0.006 # the maximum synaptic conductance of the inhibitory connections onto the soma