import os

class solventAccessibility(object):
	# determine solvent accessibility for each atom within a pdb file using CCP4 suite
	# program 'areaimol'
	def __init__(self,inputPDBfile="",outPDBfile=""):
		self.inputPDBfile 	= inputPDBfile
		self.outPDBfile 	= outPDBfile

	def runAREAIMOL(self):
		# run the ccp4 suite program AREAIMOL to calculate solvent accessibility for 
		# each atom with PDB file
		commandLineInput = "/Applications/ccp4-6.4.0/bin/areaimol "+\
				 		   "XYZIN {} ".format(self.inputPDBfile) +\
				 		   "XYZOUT {} ".format(self.outPDBfile)
		os.system(commandLineInput)

		

