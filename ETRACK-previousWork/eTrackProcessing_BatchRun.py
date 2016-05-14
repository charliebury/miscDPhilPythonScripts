from ccp4_jobs_Batch import runOverVDWRs
from eTrack_RUN import eTrack
import sys
from write_eTrackInputFile import writeInputFile
import os

# make overall directory for project
projectName = 'TRAPDamageRun'
if not os.path.exists(projectName):
	os.makedirs(projectName)

# prepare maps for eTrack pipeline
runOverVDWRs(projectName)

for r in np.arange(0.5,2.5,0.5):
	# make sure correct directory is present
	runDirectory = '{}/eTrackReadyFiles_{}'.format(projectName,VDWR)
	if not os.path.exists(runDirectory):
		print 'Directory not found --> unable to continue'
		sys.exit()

	# write suitable eTrack input script
	writeInputFile(runDirectory)

	# run eTrack pipeline now
	eT = eTrack()
	eT.runPipeline('y','y','n','n',inputfilename)

	# make a working directory for post processing analysis (whatever that may be)
	workDirectoryName = projectName+'/Results'
	if not os.path.exists(workDirectoryName):
		os.makedirs(workDirectoryName)

		for datasetNum in range(2,11):
			fileName = ('/13830_TRAPRNAdamage{}_data.pkl'.format(datasetNum)).split('.')[0]
			oldPlace = runDirectory+fileName+'.pkl'
			newPlace = workDirectoryName+fileName+'_VDWR'+r+'.pkl'
			os.rename(oldPlace,newPlace)

