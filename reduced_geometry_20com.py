# Geometry by Armin Bahl, Jun 18 2009
# Simplified Geometry for layer 5 Pyramidal Neuron
#
# The Geometry will fulfill these area conditions
# Surface areas were calculated from a detailed reconstruction from a Pyramidal Neuron
soma_area = 1682.96028429
basal_area = 7060.90626796
apicalshaftoblique_area = 9312.38528764
tuft_area = 9434.24861189

# Create sections
soma = h.Section(name='soma') # self.soma = h.Section(name='soma', cell=self)
basal = h.Section(name='basal')
apical = h.Section(name='apical')
tuft = h.Section(name='tuft')
hillock = h.Section(name='hillock')
iseg = h.Section(name='iseg')
axon = h.Section(name='axon')

# Topology - connect the sections into a single neuron
basal.connect(soma(0.5)) # self.dend.connect(self.soma(1))
apical.connect(soma(1))
tuft.connect(apical(1))
hillock.connect(soma(0))
iseg.connect(hillock(1))
axon.connect(iseg(1))

# Set spatial resolution of sections
soma.nseg = 1
basal.nseg = 1
apical.nseg = 5
tuft.nseg = 2
hillock.nseg = 5
iseg.nseg = 5
axon.nseg = 1

# Set dimensions of the sections
basal.L	 = 257   
apical.L = 500
tuft.L = 499
hillock.L = 20
axon.L = 500
iseg.L = 25
axon.diam = 1.5
iseg.diam(0:1) = 2.0:1.5
hillock.diam(0:1) = 3.5:2.0

diam_apical = apicalshaftoblique_area/PI/apical.L

def recalculate_geometry(self):
	self.soma.diam = L =  sqrt(soma_area/PI)
	self.basal.diam = basal_area/PI/basal.L	
	self.apical.diam = diam_apical	
	self.tuft.diam = tuft_area/PI/tuft.L

recalculate_geometry()


# Set electrical properties of sections

soma.Ra =  82
basal.Ra = 734 
tuft.Ra = 527

Ra_apical = 261
apical.Ra =  Ra_apical

hillock.Ra = soma.Ra
axon.Ra = soma.Ra
iseg.Ra = soma.Ra


# Define Sections
#    def build_subsets(self):
#        """Build subset lists. For now we define 'all'."""
#        self.all = h.SectionList()
#        self.all.wholetree(sec=self.soma)

#objref axon_list, axosomatic_list, apicaltree_list, apicalshaftoblique_list, tuft_list, soma_list, basal_list
#
#axon_list 				= new SectionList()
#axosomatic_list 		= new SectionList()
#apicalshaftoblique_list = new SectionList()
#apicaltree_list 		= new SectionList()
#tuft_list 				= new SectionList()
#soma_list 				= new SectionList()
#basal_list 				= new SectionList()
#
#hillock			axon_list.append()
#iseg			axon_list.append()
#axon			axon_list.append()
#
#soma			axosomatic_list.append()
#basal			axosomatic_list.append()
#hillock			axosomatic_list.append()
#iseg			axosomatic_list.append()
#axon			axosomatic_list.append()
#
#apical 			apicalshaftoblique_list.append()
#apical			apicaltree_list.append()
#tuft			apicaltree_list.append()
#
#tuft 			tuft_list.append() 
#
#soma			soma_list.append()
#
#basal			basal_list.append()
