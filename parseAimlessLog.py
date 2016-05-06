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
				 numDatasets = 11,
				 presets     = 'CCCT'):

		self.numDatasets = numDatasets
		self.getPresets(type = presets)

		lists = {'AvI'   : [],
				 'NMeas' : [],
				 'full'  : []}

		for i in range(numDatasets):
			dName = '{}{}'.format(self.datasetNamePrefix,i+1)
			p = parseAimlessLog(location    = self.locations[i],
								datasetName = dName,
								printText   = False)
			output =p.getOutput()
	
			lists['AvI'].append(output[0])
			lists['NMeas'].append(output[1])
			lists['full'].append(output[2])

		self.data = lists

	def plotGraphs(self):

		# plot and save all key graphs in one go

		self.plotDataByResBin(index    = 'NMeas',
							  saveFig  = True)
		self.plotDataByResBin(index    = 'AvI',
							  saveFig  = True)
		self.plotDataByDataset(index   = 'NMeas',
							   saveFig = True,
							   bin     = 'overall')
		self.plotDataByDataset(index   = 'AvI',
							   saveFig = True,
							   bin     = 'overall')

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

	def plotDataByResBin(self,
						 dataset       = 'all',
						 index         = 'AvI',
						 saveFig       = False,
						 axisFontSize  = 18,
						 titleFontSize = 24,
						 plotType      = '.svg'):

		# plot graph of metric against resolution bin, for each dataset.
		# 'dataset' takes 'all' to plot for all datasets or an integer n
		# to plot for dataset n

		sns.set_palette(palette  = 'hls',
						n_colors = self.numDatasets,
						desat    = .6)
		sns.set_context(rc = {"figure.figsize":(10, 10)})
		fig = plt.figure()

		if dataset != 'all':
			title = '{} values per resolution bin: dataset {}'.format(index,dataset+1)
			saveName = '{}_dataset-{}{}'.format(index,dataset,plotType)
			xData = self.data['full'][dataset]['Dmid']
			yData = self.data['full'][dataset][index]
			plt.plot(xData,
					 yData,
					 label = 'Dataset {}'.format(dataset+1))

		else:
			for d in range(self.numDatasets):
				title = '{} values per resolution bin: all datasets'.format(index)
				saveName = '{}_dataset-all{}'.format(index,plotType)
				xData = self.data['full'][d]['Dmid']
				yData = self.data['full'][d][index]
				plt.plot(xData,
						 yData,
						 label = 'Dataset {}'.format(d+1))
				plt.legend(loc = 'best')

		plt.xlabel('Resolution bin centre (Angstroms)',
			       fontsize = axisFontSize)
		plt.ylabel(index,
				   fontsize = axisFontSize)
		fig.suptitle(title, 
					 fontsize = titleFontSize)

		if saveFig is False:
			plt.show()
		else:
			fig.savefig(saveName)	

	def plotDataByDataset(self,
				 		  bin           = 0,
				 		  index         = 'AvI',
				 		  saveFig       = False,
				 		  axisFontSize  = 18,
				 		  titleFontSize = 24,
				 		  plotType      = '.svg'):

		# plot a specific bin's values for each successive dataset

		if bin !='overall':
			data = self.rearrangeDataByBin(bin   = bin,
										   index = index)
			title = '{} values per dataset: bin {}'.format(index,bin)
			saveName = '{}_bin-{}{}'.format(index,bin,plotType)
		elif bin == 'overall':
			data = self.data[index]
			title = '{} overall values per dataset'.format(index)
			saveName = '{}_overall{}'.format(index,plotType)

		sns.set_palette(palette  = 'hls',
						n_colors = self.numDatasets,
						desat    = .6)
		sns.set_context(rc={"figure.figsize":(10, 10)})
		fig = plt.figure()

		plt.plot(range(1,len(data)+1),data)

		plt.xlabel('Dataset',
				   fontsize = axisFontSize)
		plt.ylabel(index,
				   fontsize = axisFontSize)
		plt.xlim(0,self.numDatasets+1)
		fig.suptitle(title,
					 fontsize = titleFontSize)

		if saveFig is False:
			plt.show()
		else:
			fig.savefig(saveName)

	def getPresets(self,type='DNA'):

		# presets for DIALS processing

		if type == 'DNA':
			self.locations = ['dataset{}-b/'.format(i+1) for i in range(self.numDatasets)]
			self.datasetNamePrefix = 'FROMDIALS'

		elif type == 'GH7':
			self.locations = ['dataset{}/'.format(i+1) for i in range(self.numDatasets)]
			self.datasetNamePrefix = 'FROMDIALS'

		elif type == 'CCCT':
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

		# rather than explicitly provide a log file name,
		#  find a .log file in directory

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

		data = {'NMeas' : [],
				 'AvI'  : [],
				 'Dmid' : []}

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
						data['Dmid'].append(float(l.split()[2]))
		aimlessLog.close()

		# calculate In metric here
		In = np.dot(data['NMeas'],data['AvI'])
		totMeas = np.sum(data['NMeas'])
		if self.printText is True:
			print data
			print 'In={} #Meas={}'.format(In,totMeas)
			
		return (In,totMeas,data)
