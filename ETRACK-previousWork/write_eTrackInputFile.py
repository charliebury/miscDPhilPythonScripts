# little script to write an eTrack input file
def writeInputFile(runDirectory):
	inputFile = open('eTrackInput{}.txt'.format(ind),'w')
	inputfile.write('END')
			inputfile.close()

	"""#
	# e_Track input file for current run
	#
	# location of map and pdb files required
	where {}
	#
	# dataset names -> prefix only needed here. eg: '3clcdamage1' for 
	# '3clcdamage.pdb','3clcdamage_atoms.map','3clcdamage_density.map'
	# To further assist, specify number 'damageset_num' of each damage set
	# separately to damage series name:
	damageset_name {}
	damageset_num 2,3,4,5,6,7,8,9,10
	#
	# optional pkl file names for post processing pipeline step. If input below
	# these will be read in only in map_processing step is not included within 
	# pipeline run, otherwise map_processing output used instead
	PKLFILE 13830_TRAPRNAdamage2_data.pkl
	PKLFILE 13830_TRAPRNAdamage3_data.pkl
	PKLFILE 13830_TRAPRNAdamage4_data.pkl
	PKLFILE 13830_TRAPRNAdamage5_data.pkl
	PKLFILE 13830_TRAPRNAdamage6_data.pkl
	PKLFILE 13830_TRAPRNAdamage7_data.pkl
	PKLFILE 13830_TRAPRNAdamage8_data.pkl
	PKLFILE 13830_TRAPRNAdamage9_data.pkl
	PKLFILE 13830_TRAPRNAdamage10_data.pkl
	#
	# post_processing initial pdb file specified here
	initialPDB TRAPRNA1.pdb
	#
	# graph_analysis variables to be specified here
	topN 500
	densmet min
	#
	# PDBmulti multi dataset list of objects pkl file name 
	PKLMULTIFILE 13830_TRAPRNAdamage_data.pkl""".format(runDirectory,runDirectory.split('/')[0])