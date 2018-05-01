import threading, random

class setInterval():
    def __init__(self, func, sec):
        def func_wrapper():
            self.t = threading.Timer(sec, func_wrapper)
            self.t.start()
            func()
        self.t = threading.Timer(sec, func_wrapper)
        self.t.start()

    def cancel(self):
        self.t.cancel()

class ClassName(object):
	"""docstring for ClassName"""
	def __init__(self):
		super(ClassName, self).__init__()
		self.timer = setInterval(self.roll6, 3)

	def roll6(self):
		roll = random.randint(1, 6)
		print("You rolled: " + str(roll))
		if roll == 6:
			self.timer.cancel() # doesn't seem to cancel though
			print("Finally, a 6! We can stop rolling.")

a = ClassName()