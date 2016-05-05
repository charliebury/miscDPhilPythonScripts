import os
import sys

class batchImageProcessing():

  def __init__(self,
               title           = 'GH7',
               totalImages     = 9999,
               wedgeSize       = 900,
               spaceGroup      = 'C121',
               unitCell        = '128.290,47.020,173.500,90.00,108.23,90.00',
               imageDir        = '/Users/charlie/DPhil/YEAR2/APR/GH7/SAMPLE_5_2/',
               imagePrefix     = 'SAMPLE_5_2_',
               imFileType      = '.cbf',
               useJsonTemplate = False,
               highResolution  = '',
               lowResolution   = '',
               quickRunAIMLESS = False,
               startWedge      = 1,
               dirNaming       = 'dataset#-batch/'):

    numBatches = totalImages/wedgeSize

    for i in range(startWedge,numBatches+1):

      d = dialsImageProcessing(title           = title,
                               location        = dirNaming.replace('#',str(i)),
                               spaceGroup      = spaceGroup,
                               unitCell        = unitCell,
                               imageDir        = imageDir,
                               imagePrefix     = imagePrefix,
                               imFileType      = imFileType,
                               wedgeNumber     = i,
                               useJsonTemplate = useJsonTemplate,
                               wedgeSize       = wedgeSize,
                               highResolution  = highResolution,
                               lowResolution   = lowResolution,
                               quickRunAIMLESS = quickRunAIMLESS)

class dialsImageProcessing():

  def __init__(self,
               title           = 'GH7',
               location        = 'dataset1/',
               spaceGroup      = 'C121',
               unitCell        = '128.290,47.020,173.500,90.00,108.23,90.00',
               imageDir        = '/Users/charlie/DPhil/YEAR2/APR/CCCT/SAMPLE_3_15/',
               imagePrefix     = 'SAMPLE_3_15_2_',
               imFileType      = '.cbf',
               wedgeNumber     = 1,
               wedgeSize       = 450,
               autoRun         = True,
               useJsonTemplate = False,
               highResolution  = '',
               lowResolution   = '',
               quickRunAIMLESS = True):

    self.location 	    = location
    self.spaceGroup	    = spaceGroup
    self.unitCell       = unitCell
    self.imageDir       = imageDir
    self.imagePrefix    = imagePrefix
    self.wedgeSize      = wedgeSize
    self.wedgeNumber    = wedgeNumber
    self.useTemplate    = useJsonTemplate
    self.imFileType     = imFileType
    self.lowResolution  = lowResolution
    self.highResolution = highResolution
    self.quickRun       = quickRunAIMLESS

    if autoRun is True:
      self.runAll()

  def runAll(self):
    self.makeWorkingDir()
    self.calculateStartStop()
    self.writeJsonFile()
    self.moveJsonFile()
    self.switchWorkingDirectory()
    self.runDials()

    if self.quickRun is True:
      self.quickRunAimless(program='pointless')
      self.quickRunAimless(program='aimless')

    self.switchWorkingDirectory(way='out')

  def calculateStartStop(self):
    self.imageStart = 1+self.wedgeSize*(self.wedgeNumber-1)
    self.imageStop   = self.imageStart-1+self.wedgeSize

  def switchWorkingDirectory(self,way='in'):
    if way == 'in':
      os.chdir(self.location)
    elif way == 'out':
      os.chdir('../')

  def runDials(self,nproc=4):
    # run dials now

    os.system('dials.find_spots min_spot_size=3 datablock.json nproc={}'.format(nproc))
    self.checkFileInDir(fileName='strong.pickle')

    os.system('dials.index datablock.json strong.pickle space_group={} unit_cell={}'.format(self.spaceGroup,self.unitCell)) 
    self.checkFileInDir(fileName='indexed.pickle')

    os.system('dials.refine experiments.json indexed.pickle') 
    self.checkFileInDir(fileName='refined.pickle')

    os.system('dials.refine refined_experiments.json refined.pickle scan_varying=true')
    self.checkFileInDir(fileName='refined.pickle')

    os.system('dials.integrate refined_experiments.json refined.pickle') 
    self.checkFileInDir(fileName='integrated.pickle')

    os.system('dials.export integrated.pickle refined_experiments.json mtz.hklout=integrated.mtz')
    self.checkFileInDir(fileName='integrated.mtz')

  def quickRunAimless(self,program='pointless'):
    if program == 'pointless':
      os.system('pointless hklin integrated.mtz hklout sorted.mtz > pointless.log')
    elif program == 'aimless':
      inputFile = open('AIMLESSinputs.txt','w')

      if self.highResolution != '':
        if self.lowResolution != '':
            str = 'resolution {} {}\nanomalous off'.format(self.lowResolution,self.highResolution)
        else:
            str = 'resolution {}\nanomalous off'.format(self.highResolution)
      else:
        str = 'anomalous off'
      inputFile.write(str)
      inputFile.close()
      os.system('aimless hklin sorted.mtz hklout scaled.mtz < AIMLESSinputs.txt > aimless.log')

  def writeJsonFile(self):
    print 'Writing .json file for job'

    if self.useTemplate is True:
      # write json file for current processing using a template json file
      template = open('datablockTemplate.json','r')
      jsonFile = open('datablock.json','w')

      for line in template.readlines():

        if '$1$' in line:
          newLine = line.replace('$1$',self.imageDir+self.imagePrefix)
          jsonFile.write(newLine)

        elif '$2$' in line:
          newLine = line.replace('$2$',str(self.imageStart))
          jsonFile.write(newLine)

        elif '$3$' in line:
          newLine = line.replace('$3$',str(self.imageStop))
          jsonFile.write(newLine)

        else:
          jsonFile.write(line)

      template.close()
      jsonFile.close()

    else:
      # write json file using dials.import
      stdInFile = open('importFiles.txt','w') 
      for i in range(self.imageStart,self.imageStop+1):
        imNum = '0'*(4-len(str(i)))+str(i)
        image = '{}{}{}{}\n'.format(self.imageDir,
                                    self.imagePrefix,
                                    imNum,
                                    self.imFileType)
        stdInFile.write(image)
      stdInFile.close()  
      clInput = 'dials.import < {}'.format('importFiles.txt')
      os.system(clInput)

  def moveJsonFile(self):
    os.system('mv datablock.json {}datablock.json'.format(self.location))
    if self.useTemplate is False:
      for file in ('dials.import.log','dials.import.debug.log'):
        os.system('mv {} {}{}'.format(file,self.location,file))

  def makeWorkingDir(self):
    os.system('mkdir {}'.format(self.location))

  def checkFileInDir(self,fileName=''):
    if fileName not in os.listdir('./'):
      str = '"{}" not found in directory "{}"'.format(fileName,self.location)
      sys.exit(str)



