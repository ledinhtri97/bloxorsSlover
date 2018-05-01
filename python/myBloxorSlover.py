import pygame, math

class Solver(object):
	"""docstring for Solver"""
	def __init__(self, p):
		super(Solver, self).__init__()
		self.p = p
		self.mvP = [[32, 10, -77], [-5, 16, 62]]
		self.bvP = [[32, 10, -153], [-5, 16, -28]]

	class imageCache(object):
		"""docstring for imageCache"""
		def __init__(self, arg):
			super(imageCache, self).__init__()
			self.arg = arg
		
			self.images = {
				'N': 'NormalCell.png',
			 	'O': 'SoftPlate.png', 
			 	'X': 'HardPlate.png',
				'#': 'DestinationCell.png', 
				'W': 'WeakCell.png', 
				'S': 'Splitter.png',
				'goal': 'goal.png',
				'avoid': 'avoid.png',
				'avoidgoal': 'avoidgoal.png',
				'occupied': 'occupied.png',
				'occupiedgoal': 'occupiedgoal.png',
				'occupiedavoid': 'occupiedavoid.png',
				'occupiedavoidgoal': 'occupiedavoidgoal.png',
				'block_v': 'block_v.png',
				'block_ew': 'block_ew.png',
				'block_ns': 'block_ns.png'
			}
			self.imageCache = {}

			for imgName in images:
				if imgName in images:
					imageCache[imgName] = self.makeImage(imgName)

		def makeImage(self, imgName):
			    """loads and prepares image from data directory"""
			file = os.path.join(main_dir, 'images', imgName)
			try:
    			surface = pygame.image.load(file)
			except pygame.error:
    			raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
			return surface.convert()

	def get_imageCache(self):
		return self.imageCache(self)

	def ClearnNode(self, e):
		while len(e):
			def e[0]


	def MakeImage(self, imgName):
		    """loads and prepares image from data directory"""
		o = self.get_imageCache.imageCache[imgName]
		if o: return o

	def HandleFieldClick(self):
		return

	def BlockPos(self, x0, y0, x1, y1):
		if (x0 < x1) or ((x0 == x1) and (y0 < y1)):
			self.x0 = x0
			self.x1 = x1
			self.y0 = y0
			self.y1 = y1
		else:
			self.x0 = x1
			self.x1 = x0
			self.y0 = y1
			self.y1 = y0

	def Board(self, size):
		self.size = size
		