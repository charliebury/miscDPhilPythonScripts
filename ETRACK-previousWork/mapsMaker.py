class mapsMaker:
    def __init__(self):

    	self.inputTxtFile = 'inputfile_ccp4jobs.txt'

	def get_atomanddensmaps():
		# read in inputfile
		inputlines = open(self.inputTxtFile,'r').readlines()

		sfall_GRID = []
		for line in inputlines:
			if 'pdbIN' == line.split()[0]:
				self.pdbname = line.split()[1]
			if 'runname' == line.split()[0]:
				self.runname = line.split()[1]
			if 'dataset' == line.split()[0]:
				self.N = line.split()[1]
			if 'sfall_symm' == line.split()[0]:
				self.sfall_symmetrygroup = line.split()[1]
			if 'sfall_GRID' == line.split()[0]:
				sfall_GRIDnx = line.split()[1]
				sfall_GRIDny = line.split()[2]
				sfall_GRIDnz = line.split()[3]
				self.sfall_GRID = line.split()[1:4]
			if 'mtzIN' == line.split()[0]:
				self.fft_inputmergedmtzfile = line.split()[1]
			if 'fft_Fobs_dam' == line.split()[0]:
				self.Fobs_dam = line.split()[1]
			if 'fft_SIGobs_dam' == line.split()[0]:
				self.SIGobs_dam = line.split()[1]
			if 'fft_Fobs_init' == line.split()[0]:
				self.Fobs_init = line.split()[1]
			if 'fft_SIGobs_init' == line.split()[0]:
				self.SIGobs_init = line.split()[1]
			if 'fft_PHIC_dam' == line.split()[0]:
				self.PHIC_dam = line.split()[1]
			if 'fft_FOM_dam' == line.split()[0]:
				self.FOM_dam = line.split()[1]
			if 'fft_FOM_init' == line.split()[0]:
				self.FOM_init = line.split()[1]
			if 'foldername' == line.split()[0]:
				self.where = line.split()[1]
			if 'END' == line.split()[0]:
				break

		pdbcur_inputpdbfile = pdbname
		pdbcur_outputpdbfile = where+'pdbcur_'+runname+N+'.pdb'
		pdbreorder_outpdbfile = where+'pdbreorder_'+runname+N+'.pdb'
		sfall_outputmapfile = where+runname+N+'_atoms.map'
		FFT_outputmapfile = where+runname+N+'_density.map'

		# sfall_outputmapfileCROPPED = where+runname+N+'_atoms_CROPPED.map'

		# run pdbcur job
		pdbcur_runoutput = pdbCUR_run(pdbcur_inputpdbfile,pdbcur_outputpdbfile)

		# run my own reordering script
		inputpdbfile = pdbcur_runoutput.outputpdbfile
		reorderedpdb = renumber_pdbfile(inputpdbfile,pdbreorder_outpdbfile)

		# run sfall job
		SFALL_runoutput = SFALL_run(reorderedpdb,sfall_outputmapfile,sfall_symmetrygroup,sfall_GRID)

		# run fft job
		mtzlabels = [Fobs_dam,SIGobs_dam,Fobs_init,SIGobs_init,PHIC_dam,FOM_dam,FOM_init]
		FFT_runoutput = FFT_run(SFALL_runoutput,fft_inputmergedmtzfile,FFT_outputmapfile,mtzlabels)

		# crop to asymmetric unit:
		mapmask_run_confine2AS(SFALL_runoutput.outputmapfile,SFALL_runoutput.outputmapfile)
		# mapmask_run_confine2AS(SFALL_runoutput.outputmapfile,sfall_outputmapfileCROPPED)

		mapmask_run_confine2AS(FFT_runoutput.outputmapfile,FFT_runoutput.outputmapfile)
		
		# run MAPMASK job to crop FFT density map to same grid 
		# sampling dimensions as SFALL atom map
		mapmask_run(FFT_runoutput.outputmapfile,SFALL_runoutput.outputmapfile,FFT_runoutput.outputmapfile)
		# mapmask_run(FFT_runoutput.outputmapfile,sfall_outputmapfileCROPPED,FFT_runoutput.outputmapfile)

		# check consistency between atom and density maps generated
		atmmap_densmap_check(SFALL_runoutput,FFT_runoutput)











		

