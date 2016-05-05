import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

class batchParseAimlessLog():

	# a class to parse a series of AIMLESS log files
	# (generated in ccp4i gui). Here the In/I1 intensity
	# statistics are retrieved for each dataset within 
	# the full series

	def __init__(self,
				 numDatasets = 22,
				 presets     = 'DNA'):

		self.numDatasets = numDatasets
		self.getPresets(type = presets)

		lists = {'AvI':[],
				 'NMeas':[],
				 'full':[]}

		for i in range(numDatasets):

			p = parseAimlessLog(location    = self.locations[i],
								datasetName = '{}{}'.format(self.datasetNamePrefix,i+1),
								printText   = False)
			output =p.getOutput()
	
			lists['AvI'].append(output[0])
			lists['NMeas'].append(output[1])
			lists['full'].append(output[2])

		self.data = lists

	def rearrangeDataByBin(self,
						   bin   = 0,
						   index = 'AvI'):

		# the dataList contains a set of dictionaries of data 
		# from each dataset - output a list of the values per 
		# dataset for a specific bin

		if index not in ('AvI','NMeas'):
			print 'Invalid index name'
			return
		if isinstance(bin,int) is False:
			print '"bin" must take integer value'
			return

		binData = []
		for data in self.data['full']:
			chosenData = data[index][bin]
			binData.append(chosenData)
		return binData

	def plotData(self,
				 bin           = 0,
				 index         = 'AvI',
				 saveFig       = False,
				 axisFontSize  = 18,
				 titleFontSize = 24):

		# plot a specific bin's values for each successive dataset

		if bin not in ('overall','all'):
			data = self.rearrangeDataByBin(bin   = bin,
										   index = index)
			title = '{} values per dataset: bin {}'.format(index,bin)
			saveName = '{}bin{}.png'.format(index,bin)
		elif bin == 'overall':
			data = self.data[index]
			title = '{} overall values per dataset'.format(index)
			saveName = '{}overall.png'.format(index)
		elif bin == 'all':
			data = []
			for i in range(self.numDatasets):
				d = self.rearrangeDataByBin(bin   = i,
											index = index)
				data.append(d)
			title = '{} values per dataset: all bins'.format(index)
			saveName = '{}AllBins.png'.format(index)

		sns.set_palette(palette  = 'hls',
						n_colors = self.numDatasets,
						desat    = .6)
		sns.set_context(rc={"figure.figsize":(10, 10)})
		fig = plt.figure()
		if bin != 'all':
			plt.plot(range(1,len(data)+1),data)
		else:
			for i in range(self.numDatasets):
				plt.plot(range(1,len(data[i])+1),data[i],label='Bin {}'.format(i))
				plt.legend()

		plt.xlabel('Dataset',fontsize=axisFontSize)
		plt.ylabel(index,fontsize=axisFontSize)
		plt.xlim(0,self.numDatasets+1)
		fig.suptitle(title,fontsize=titleFontSize)
		if saveFig is False:
			plt.show()
		else:
			fig.savefig(saveName)

	def getPresets(self,type='DNA'):

		# presets for DIALS processing. Here
		# two sets of preset values are included
		# for two processing sessions. User 
		# will need to modify accordingly

		if type == 'DNA':
			self.locations = ['dataset{}-b/'.format(i+1) for i in range(self.numDatasets)]
			self.datasetNamePrefix = 'FROMDIALS'
		elif type == 'GH7':
			self.locations = ['dataset{}/'.format(i+1) for i in range(self.numDatasets)]
			self.datasetNamePrefix = 'FROMDIALS'

class parseAimlessLog():

	# a class to parse a single specified AIMLESS log file
	# (generated within the ccp4i gui). The In/I1 intensity
	# information is retrieved for this dataset

	def __init__(self,
				 location    = './',
				 logName     = 'aimless-logfile.log',
				 datasetName = 'FROMDIALS1',
				 run         = True,
				 printText   = True):
	
		self.location  = location
		self.printText = printText

		if logName in os.listdir(self.location):
			self.logName = logName
		else:
			self.logName = self.findLogInDir()
		if self.logName is False:
			return 

		self.datasetName = datasetName

		if run is True:
			self.output = self.parseInFromLog()

	def getOutput(self):

		# return the output

		return self.output

	def findLogInDir(self):

		# rather than explicitly provide a log 
		# file name, find a .log file in directory

		for file in os.listdir(self.location):
			if file.endswith('.log') is True:
				return file
		print 'No .log file found in location specified'
		return False

	def parseInFromLog(self):

		# parse the output log file to find relevant 
		# In/I1 statistics for current batch

		aimlessLog = open('{}{}'.format(self.location,self.logName),'r')

		tableFound = False
		readNextLine = False
		data = {'NMeas':[],'AvI':[]}
		for l in aimlessLog.readlines():
			if '$TABLE:  Analysis against resolution, {}'.format(self.datasetName) in l:
				tableFound = True
				continue
			if tableFound is True:
				if l.split()[0] == 'N':
					# start reading next line
					readNextLine = True
					continue
				if readNextLine is True:
					if l.split()[0] == '$$':
						break
					else:
						data['NMeas'].append(int(l.split()[8]))
						data['AvI'].append(int(l.split()[9]))
		aimlessLog.close()

		# calculate In metric here
		In = np.dot(data['NMeas'],data['AvI'])
		totMeas = np.sum(data['NMeas'])
		if self.printText is True:
			print data
			print 'In={} #Meas={}'.format(In,totMeas)
			
		return (In,totMeas,data)
