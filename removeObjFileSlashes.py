
class removeObjFileSlashes():
	
	# remove unwanted slashes from 'f' lines in
	#a blender .obj file ready to be read by RD3D

	def __init__(self,
				 fileName = 'untitled.obj',
				 fileType = '.obj'
				 ):
	
		newFile = fileName.strip(fileType)+'_fixed'+fileType
		f       = open(fileName,'r')
		fnew    = open(newFile,'w')
		for l in f.readlines():
			if len(l) == 0:
				continue
			elif l[0] == 'f':
				newl = 'f '+ ' '.join([q.split('//')[0] for q in l.split(' ')[1:]])+'\n'
			else:
				newl = l 
			fnew.write(newl)
		f.close()
		fnew.close()
		print 'New file: {}'.format(newFile)

