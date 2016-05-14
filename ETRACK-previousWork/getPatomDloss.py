def writeCSV(atoms):

	csvOut = open('PatomDloss.csv','w')
	atomLists = {'G1':[],'A2':[],'G3':[],'U4':[],'GLU CD': [],'GLY CA':[]}

	# get list of glu C side-chain atoms
	for atom in atoms:
		if atom.basetype == 'GLU' and atom.atomtype in ['CD']:
			atomLists['GLU CD'].append(atom)

	# get list of RNA P atoms for each nucleotide type
	bases = ['G1','A2','G3','U4']
	for base in bases:
		for atom in atoms:
			if atom.basetype == base[0] and atom.atomtype in ["P"] and atom.residuenum%5 == int(base[1]):
				atomLists[base].append(atom)

	# get a control list of gly CA atoms
	for atom in atoms:
		if atom.basetype == 'GLY' and atom.atomtype in ['CA']:
			atomLists['GLY CA'].append(atom)

	for key in atomLists.keys():
		csvOut.write('{} atoms:\n'.format(key))
		for atom in atomLists[key]:
			densVals = atom.densMetric['loss']['Standard']['values']
			densSlope = atom.densMetric['loss']['Standard']['lin reg']['slope']			
			csvOut.write(','.join([str(val) for val in densVals]))
			csvOut.write(',{}'.format(densSlope))
			csvOut.write('\n')

	csvOut.close()