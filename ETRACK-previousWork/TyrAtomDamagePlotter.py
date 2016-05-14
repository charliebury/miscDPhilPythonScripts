# plot bound vs non-bound density change plots for all Tyr atoms in a typical Tyr residue
from retrieveAtomList import retrieveAtomList

def tyrDensityPlotter():
	# retrieve list of processed atom objects
	atoms = retrieveAtomList()

	atomTypes = ['CA','C','O','N','CB','CG','CD1','CE1','CZ','OH','CE2','CD2']
	where = 'TyrAtomDamage'

	for aType in atomTypes:
		atoms.atomType 	= aType
		atoms.baseType 	= 'TYR'
		atoms.residueNum = 62
		atoms.densMetricErrorbarGraphs(True,where,2)


