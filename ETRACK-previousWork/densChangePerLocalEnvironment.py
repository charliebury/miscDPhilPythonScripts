import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import matplotlib.colors as colors
import matplotlib.cm as cmx
from scipy import stats
from matplotlib.mlab import PCA
from mpl_toolkits.mplot3d import Axes3D
from confidenceIntervalCalculator import mean_confidence_interval


def batchRun(PDBmulti,atomsbychain_present):
	# run the function below separately for each dataset number i 
	for i in range(0,9):
		print 'Running for dataset number {}'.format(i)
		barplot_densitychangeperrestype(PDBmulti,atomsbychain_present,i,False)

def barplot_densitychangeperrestype(PDBmulti,atomsbychain_present,i,plot):
	# this function plots a series of bar plots for a given damage level i, for all atoms
	# present in the structure specified by atomtype and resitype (which can be strings or 
	# lists of strings). A figure is produced with separate subplots for mean density, min 
	# density, bdamage change, and bfactor change. The barplots show separate bars for 
	# unbound and bound TRAP rings, to distinguish the different dynamics between residues
	# in the 2 different rings

	# determine the locations of residues in the atomsbychain_present list (sorted into 
	# sublists of equivalent chain atoms) corresponding to atomtype and resitype
	residuenums = [8,16,17,29,36,39,42,50,71,73]

	# write raw end data to file
	rawDataFile = open('CarbonDlossValues_{}.csv'.format(i+2),'w')
	
	counter = -1
	counter_list = []
	for atomset in atomsbychain_present:
		counter += 1
		if (atomset[0].atomtype in ['CD'] and
		   atomset[0].basetype in ['GLU'] and
		   atomset[0].residuenum in residuenums):
			counter_list.append(counter)
		elif (atomset[0].atomtype in ['CG'] and
		   atomset[0].basetype in ['ASP'] and
		   atomset[0].residuenum in residuenums):
			counter_list.append(counter)

	# loop over each equivalent atom type and determine mean and std of metrics 
	# specified in loop over each atom in an equivalent atom type
	# FIRST FOR UNBOUND RING CASE:
	mean_minchange_unbound,xTickMarks_unbound,std_minchange_unbound = [],[],[]
	confInt_minchange_unbound = []
	rawDataFile.write('For unbound TRAP ring:\n')
	for counter in counter_list:
		atomgroup = atomsbychain_present[counter][0:11]

		# find list of min density changes for these equivalent atoms --> find gradient wrt dataset number
		mindensity = [atom.mindensity[i] for atom in atomgroup]

		# calculate means of above list
		mean_minchange_unbound.append(np.mean(mindensity))

		# calculate standard deviations of above lists
		std_minchange_unbound.append(np.std(mindensity))

		# calculate 95% confidence intervals for above lists
		confInt_minchange_unbound.append(mean_confidence_interval(mindensity))

		# determine the reference name of the current residue type,
		# and append this to list of x-axis labels
		resitype = str(atomgroup[0].basetype)+str(atomgroup[0].residuenum)+str(atomgroup[0].atomtype)
		xTickMarks_unbound.append(resitype)

		rawDataFile.write('{},{},{},{}\n'.format(resitype,np.mean(mindensity),np.std(mindensity),mean_confidence_interval(mindensity)))

	# NEXT FOR BOUND RING CASE:
	# loop over each equivalent atom type and determine mean and std of metrics 
	# specified in loop over each atom in an equivalent atom type
	mean_minchange_bound,xTickMarks_bound,std_minchange_bound = [],[],[]
	confInt_minchange_bound = []
	rawDataFile.write('For bound TRAP ring:\n')
	for counter in counter_list:
		atomgroup = atomsbychain_present[counter][11:22]

		# find list of min density changes for these equivalent atoms --> find gradient wrt dataset number
		mindensity = [atom.mindensity[i] for atom in atomgroup]

		# calculate means of above list
		mean_minchange_bound.append(np.mean(mindensity))

		# calculate standard deviations of above list
		std_minchange_bound.append(np.std(mindensity))

		# calculate 95% confidence intervals for above lists
		confInt_minchange_bound.append(mean_confidence_interval(mindensity))

		# determine the reference name of the current residue type,
		# and append this to list of x-axis labels
		resitype = str(atomgroup[0].basetype)+str(atomgroup[0].residuenum)+str(atomgroup[0].atomtype)
		xTickMarks_bound.append(resitype)

		rawDataFile.write('{},{},{},{}\n'.format(resitype,np.mean(mindensity),np.std(mindensity),mean_confidence_interval(mindensity)))

	# give option to not plot output barplot
	if plot == False:
		return

	# Create a figure instance
	sns.set_palette("deep", desat=.6)
	sns.set_context(rc={"figure.figsize": (30, 12)})
	fig = plt.figure()

	# width of bars in plot
	width = 0.35 

	# Create an axes instance
	ax = plt.subplot(1, 1, 1)
	x = np.arange(len(xTickMarks_bound))
	unboundplt = plt.bar(x, mean_minchange_unbound,width,
					     yerr=std_minchange_unbound,color='#6897bb',
					     error_kw=dict(elinewidth=2,ecolor='#31698a'))
	boundplt = plt.bar(x+width, mean_minchange_bound,width,
					   yerr=std_minchange_bound,color='#c0d6e4',
					   error_kw=dict(elinewidth=2,ecolor='#31698a'))

	## Custom x-label,y-label
	ax.set_xlim(-width,len(x)+width)                       
	plt.xlabel('Residue', fontsize=18)
	plt.ylabel('Min density change', fontsize=18)
	ax.set_xticks(x+width)
	xtickNames = ax.set_xticklabels(xTickMarks_bound)
	plt.setp(xtickNames, rotation=90, fontsize=10)
	# add a legend
	ax.legend( (unboundplt[0], boundplt[0]), ('unbound', 'bound'),loc='best')
	
	
	plt.subplots_adjust(top=0.90)
	fig.subplots_adjust(hspace=.4)

	# Save the figure
	fig.savefig('DAMAGEvariability_per_chain_damage%s.png' %(str(i)),bbox_inches='tight')