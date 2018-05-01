import pygame, math, os

class myBoardApp():

	"""docstring for myBoardApp"""
	def __init__(self, size, font="monospace", font_size=15,
                    font_color=(255, 255, 255)):
		super(myBoardApp, self).__init__()
		pygame.font.init()
		self._running = True
		self._display_surf = None
		self._size = self.weight, self.height = size*45, size*25
		self._image_surf = None
		self._items = None
		self._font = pygame.font.SysFont(font, font_size) #color and size
		self._font_color = font_color
		self._listitems = []
	
	def on_init(self):
		os.environ['SDL_VIDEO_CENTERED'] = '1'
		
		items = ('Edit View', 'Game View', 'Quickload')
		for idx, item in enumerate(items):
			label = self._font.render(item, 1, self._font_color)
			width = label.get_rect().width
			height = label.get_rect().height
			posx = 0;
			# t_h: total height of text block
			t_h = len(self._listitems) * height
			posy = (self.height / 2) - (t_h / 2) + (idx * height)
			self._listitems.append([item, label, (width, height), (posx, posy)])
			print([item, label, (width, height), (posx, posy)])
		pygame.display.set_caption('My Board Bloxor')
		pygame.init()
		self._display_surf = pygame.display.set_mode(self._size, pygame.HWSURFACE | pygame.DOUBLEBUF)
		self._running = True
		self._image_surf = pygame.image.load("images/background.jpg").convert()

	def on_event(self, event):
		if event.type == pygame.QUIT:
			self._running = False
	
	def on_loop(self):
		pass
	
	def on_render(self):
		w_img, h_img = self._image_surf.get_size()

		self._display_surf.blit(self._image_surf, ((self.weight-w_img)/2,(self.height-h_img)/2))
		for name, label, (width, height), (posx, posy) in self._listitems:
			self._display_surf.blit(label, (posx, posy))
		
		pygame.display.flip()
	
	def on_cleanup(self):
		pygame.quit()
 
	def on_execute(self):
		if self.on_init() == False:
			self._running = False
 
		while(self._running):
			for event in pygame.event.get():
				self.on_event(event)
			self.on_loop()
			self.on_render()
		self.on_cleanup()

if __name__ == "__main__":
	myBoard = myBoardApp(17)
	myBoard.on_execute()