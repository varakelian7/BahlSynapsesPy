class reduced_cell_model():
	def __init__(self):
		self.x = 0; self.y = 0; self.z = 0
		self.create_sections()
		self.build_topology()
		self.build_subsets()
		self.define_geometry()
		self.define_biophysics()
		self.addSynapses()

	def create_sections(self):
		self.soma = h.Section(name='soma', cell=self)
		self.basal = h.Section(name='basal', cell=self)
		self.apical = h.Section(name='apical', cell=self)
		self.tuft = h.Section(name='tuft', cell=self)
		self.hillock = h.Section(name='hillock', cell=self)
		self.iseg = h.Section(name='iseg', cell=self)
		self.axon = h.Section(name='axon', cell=self)

	def	build_topology(self):
		self.basal.connect(self.soma(0.5))
		self.apical.connect(self.soma(1))
		self.tuft.connect(self.apical(1))
		self.hillock.connect(self.soma(0))
		self.iseg.connect(self.hillock(1))
		self.axon.connect(self.iseg(1))		


	def recalculate_geometry(self):
		self.soma.diam = L =  sqrt(soma_area/PI)
		self.basal.diam = basal_area/PI/basal.L	
		self.apical.diam = diam_apical	
		self.tuft.diam = tuft_area/PI/tuft.L

	def define_geometry(self):
		# Set spatial resolution of sections
		self.soma.nseg = 1
		self.basal.nseg = 1
		self.apical.nseg = 5
		self.tuft.nseg = 2
		self.hillock.nseg = 5
		self.iseg.nseg = 5
		self.axon.nseg = 1

		# Set dimensions of the sections
		self.basal.L	 = 257   
		self.apical.L = 500
		self.tuft.L = 499
		self.hillock.L = 20
		self.axon.L = 500
		self.iseg.L = 25
		self.axon.diam = 1.5
		self.iseg.diam=1.8 #(0:1) = 2.0:1.5
		self.hillock.diam=2.8 #(0:1) = 3.5:2.0

		diam_apical = apicalshaftoblique_area/PI/self.apical.L
		self.recalculate_geometry()
		
	def build_subsets(self):
		self.all = h.SectionList()
		self.all.wholetree(sec=self.soma)

	def recalculate_passive_properties(self):
		for sec in self.axosomatic_list:
			sec.g_pas = 1./Rm_axosomatic
			
		for sec in self.apicaltree_list:
			sec.g_pas = self.soma.g_pas*self.spinefactor 
			sec.cm = self.soma.cm*self.spinefactor

	def recalculate_channel_densities(self):		
		# See Keren et al. 2009		
		h.distance(sec=self.soma, seg=0)
		
		for sec in self.apicaltree_list:
			for seg in sec:
				seg.gbar_kfast = self.soma.gbar_kfast(0.5) * exp(-distance(seg.x)/decay_kfast)
				seg.gbar_kslow = self.soma.gbar_kslow(0.5) * exp(-distance(seg.x)/decay_kslow)
		
		self.tuft.mih = gbar_ih/h.distance(0)
		self.tuft.mnat = (gbar_nat-self.soma.gbar_nat(0.5))/h.distance(0)
		
		for seg in self.apical:
			seg.gbar_nat = self.apical.mnat*h.distance(seg.x) + self.soma.gbar_nat(0.5)
			seg.gbar_ih = self.apical.mih*h.distance(seg.x)

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

		self.hillock.Ra = soma.Ra
		self.axon.Ra = soma.Ra
		self.iseg.Ra = soma.Ra

		for sec in self.all: # 'all' defined in build_subsets
			sec.insert('pas')
			sec.cm = 1.0
			for seg in sec:
				seg.pas.g_pas = 1./15000
				seg.pas.e_pas = -70
		
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

		with self.tuft:
			insert('cad')
			insert('sca')
			insert('kca')
			eca = 140
			ion_style("ca_ion",0,1,0,0,0)

		self.recalculate_passive_properties()
		self.recalculate_channel_densities()


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

		self.axon_list.append(hillock)
		self.axon_list.append(iseg)
		self.axon_list.append(axon)

		self.axosomatic_list.append(soma)
		self.axosomatic_list.append(basal)
		self.axosomatic_list.append(hillock)
		self.axosomatic_list.append(iseg)
		self.axosomatic_list.append(axon)

		self.apicalshaftoblique_list.append(apical)

		self.apicaltree_list.append(apical)
		self.apicaltree_list.append(tuft)

		self.tuft_list.append(tuft)

		self.soma_list.append(soma)

		self.basal_list.append(basal)

	# Create lists of cell parts that contain each ion channel type
		self.nat_list = []
		self.kslow_list = []
		self.kfast_list = []
		self.ih_list = []

		self.ih_list.append(basal)
		self.ih_list.append(apical)
		self.ih_list.append(tuft)

		self.excsyn_list.append(basal)
		self.excsyn_list.append(apical)
		self.excsyn_list.append(tuft)

		self.inhdendsyn_list.append(basal)
		self.inhdendsyn_list.append(apical)

		self.inhsomasyn_list.append(soma)

		self.nat_list.append(soma)
		self.nat_list.append(hillock)
		self.nat_list.append(iseg)
		self.nat_list.append(apical)
		self.nat_list.append(tuft)

		self.kfast_list.append(soma)
		self.kfast_list.append(apical)
		self.kfast_list.append(tuft)

		self.kslow_list.append(soma)
		self.kslow_list.append(apical)
		self.kslow_list.append(tuft)



	def addSynapses(self):
	# Define synapses in various areas of the cell
	#   and set the connection parameters (synapse
	# rise time, decay time, reversal potential,
	# conductance/weight).
	# Also create lists of synapses onto the model cell:
	#    excsyn_list: excitatory synapses onto the cell
	#    inhdendsyn_list: inhibitory synapses onto the cell dendrites
	#    inhsomasyn_list: inhibitory synapses onto the cell body	objref preInhSoma_list, preInhDend_list, preExcDend_list
		self.preInhSoma_list = []
		self.preInhDend_list = []
		self.preExcDend_list = []

		s=0
		for sec in self.inhsomasyn_list:
			syn_ = h.ExpSyn(sec(0.5))
			self.preInhSoma_list.append(syn_)	# AMPA		EC
			syn_.tau1 = myTauValue #0.5
			syn_.tau2 = 3
			syn_.e = -70
			sprint(cmdstr,"objref recInhSomaCurrent%d", s)
			{execute(cmdstr)}
			sprint(cmdstr,"recInhSomaCurrent%d = new Vector()", s)
			{execute(cmdstr)}
			sprint(cmdstr,"recInhSomaCurrent%d.record(&preInhSoma_list.object(%d).i)", s, s)
			{execute(cmdstr)}
			s = s + 1

		totInhSoma = s

		s = 0
		for sec in self.inhdendsyn_list:
			syn_ = h.ExpSyn(sec(0.5))
			self.preInhDend_list.append(syn_)	# AMPA		EC
			syn_.tau1 = 0.5
			syn_.tau2 = 3
			syn_.e = -70
			sprint(cmdstr,"objref recInhDendCurrent%d", s)
			{execute(cmdstr)}
			sprint(cmdstr,"recInhDendCurrent%d = new Vector()", s)
			{execute(cmdstr)}
			sprint(cmdstr,"recInhDendCurrent%d.record(&preInhDend_list.object(%d).i)", s, s)
			{execute(cmdstr)}
			s = s + 1

		totInhDend = s

		s = 0
		for sec in self.excsyn_list:
			syn_ = h.ExpSyn(sec(0.5))
			self.preExcDend_list.append(syn_)	# AMPA		EC
			syn_.tau1 = 1
			syn_.tau2 = 5
			syn_.e = 0
			sprint(cmdstr,"objref recExcCurrent%d", s)
			{execute(cmdstr)}
			sprint(cmdstr,"recExcCurrent%d = new Vector()", s)
			{execute(cmdstr)}
			sprint(cmdstr,"recExcCurrent%d.record(&preExcDend_list.object(%d).i)", s, s)
			{execute(cmdstr)}
			s = s + 1

		self.totExc = s

		excitatory_syn_weight = 0.005 # the maximum synaptic conductance in microSiemens, aka the synaptic amplitude, of the excitatory connections
		inhDend_syn_weight = 0.003 # the maximum synaptic conductance of the inhibitory connections onto the dendrites
		inhSoma_syn_weight = 0.006 # the maximum synaptic conductance of the inhibitory connections onto the soma

		self.spike_times = []
		vecrecs = []
		vecrecs.append(h.Vector())
		nc.record(vecrecs[0])
		self.nclist.append(nc)
		self.spike_times.append(vecrecs[0])