import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def batchPlotDensMetSubplots(atoms):
	# this function determines which atom types have signifcant differences in density
	# metrics between unbound and bound and then plots the set of density metric subplots 
	# for these atom types
	testStats,rnaDistList = atoms.calculateSigDiffsForList('net','Standard','values')
	for key in testStats.keys():
		if float(testStats[key]['p value']) < 0.05:
			atoms.atomType 	= key.split()[2]
			atoms.baseType 	= key.split()[0]
			atoms.residueNum = int(key.split()[1])
			atoms.densMetricErrorbarGraphs(True)

def batchRun(atoms):
	for densMet in ('loss','net'):
		for valType in ('values','lin reg'):
			h,l = atoms.calculateSigDiffsForList(densMet,'Calpha normalised',valType)
			print '-------------------------------------------------------'
			print 'Plotting D{} {} statistics....'.format(densMet,valType)
			rnaDistDistn(h,l,densMet,valType)		

def rnaDistDistn(h_loss,dist_loss,densMet,valType):
	sns.set(style="white", palette="muted", color_codes=True)

	distList = {}
	distList['Stabilising'] = []
	distList['Destabilising'] = []
	for key in h_loss.keys():
		if float(h_loss[key]['p value']) < 0.05:
			if h_loss[key]['stabilising?'] == True:
				distList['Stabilising'].append(dist_loss[key])
			else:
				distList['Destabilising'].append(dist_loss[key])
			print '{}... p-value: {}, stabilising: {}, RNA dist:{}'.format(key,h_loss[key]['p value'],h_loss[key]['stabilising?'],dist_loss[key])

	sns.set(style="white", palette="muted")

	# Set up the matplotlib figure
	f, axes = plt.subplots(1, 1, figsize=(8, 8))	
	sns.distplot(np.array(distList['Stabilising']),hist=False,kde=True,rug=True,kde_kws={"shade": True}, color="b",label="Stabilising")
	sns.distplot(np.array(distList['Destabilising']),hist=False, kde=True,rug=True,kde_kws={"shade": True}, color="r",label="Destabilising")
	plt.xlabel('Min distance from RNA (Angstrom)', fontsize=18)
	plt.ylabel('Probability density', fontsize=18)
	f.suptitle('Significant unbound/bound difference: {} {}'.format(densMet,valType),fontsize=24)
	f.savefig('SignifUnboundBoundDiff_{}_{}_kde.png'.format(densMet,valType))

	# Set up the matplotlib figure
	g, axes = plt.subplots(1, 1, figsize=(8, 8))
	sns.distplot(np.array(distList['Stabilising']), hist=True,kde=False,rug=True,hist_kws={"color": "b"}, color="b",label="Stabilising")
	sns.distplot(np.array(distList['Destabilising']),hist=True, kde=False,rug=True,hist_kws={"color": "r"}, color="r",label="Destabilising")
	plt.xlabel('Min distance from RNA (Angstrom)', fontsize=18)
	plt.ylabel('Frequency', fontsize=18)
	plt.legend()
	g.suptitle('Significant unbound/bound difference: {} {}'.format(densMet,valType),fontsize=24)
	g.savefig('SignifUnboundBoundDiff_{}_{}_hist.png'.format(densMet,valType))






