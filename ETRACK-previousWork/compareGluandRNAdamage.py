def writeCSV(atoms):

	csvOut = open('GLUCO2vRNAcomparison.csv','w')
	atomLists = {'glu CD':[],'asp CG':[],'RNA O3':[],'RNA O5':[],'RNA P': [],'GLY CA':[]}

	# get list of glu C side-chain atoms
	for atom in atoms:
		if atom.basetype == 'GLU' and atom.atomtype in ['CD']:
			atomLists['glu CD'].append(atom)

	# get list of asp C side-chain atoms
	for atom in atoms:
		if atom.basetype == 'ASP' and atom.atomtype in ['CG']:
			atomLists['asp CG'].append(atom)

	# get list of RNA C-O phosphodiester bond O3' oxygen atoms
	for atom in atoms:
		if atom.basetype in ['G','A','U'] and atom.atomtype in ["O3'"]:
			atomLists['RNA O3'].append(atom)

	# get list of RNA C-O phosphodiester bond O5' oxygen atoms
	for atom in atoms:
		if atom.basetype in ['G','A','U'] and atom.atomtype in ["O5'"]:
			atomLists['RNA O5'].append(atom)

	# get list of RNA P atoms
	for atom in atoms:
		if atom.basetype in ['G','A','U'] and atom.atomtype in ['P']:
			atomLists['RNA P'].append(atom)

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