#!/usr/bin/env python3
#trimo
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from functools import partial
import json
import threading
import sys

OSWIDTH = 2 if sys.platform == 'linux' else 5
SIZE = 20 if sys.platform == 'linux' else 21
COLOROCCUPIED = 'royal blue'
COLORGOAL 	  = 'orange'
COLORAVOID	  = 'tomato'
COLORDEFAULT  = 'gray83'
COLORGREY	  = 'grey'

class Solver(object):
	"""docstring for Solver"""
	def __init__(self, GameBoardApp=None):
		super().__init__()
		self.GameBoardApp = GameBoardApp

	def imageCache(self):
		pass
	
	def ClearNode(self, e):
		pass
	
	def MakeImage(self, name):
		o  = self.imageCache[name]
		if (o): return o
	
	#not yet
	def HandleFieldClick(self, x ,y):
		#print(x, y)
		self.GameBoardApp.TakeAcion(x, y)
	

	#Class Object
	class BlockPos(object):
		"""docstring for BlockPos"""
		def __init__(self, x0, y0, x1, y1):
			super().__init__()
			self.Solver = Solver()
			if ((x0 < x1) or ((x0 == x1) and (y0 < y1))):
				self.x0 = x0;
				self.y0 = y0;
				self.x1 = x1;
				self.y1 = y1;
			else:		
				self.x0 = x1;
				self.y0 = y1;
				self.x1 = x0;
				self.y1 = y0;
		
		def Joined(self):
			if((self.x0 == self.x1) and (abs(self.y0-self.y1) == 1)):
				return True
			if((self.y0 == self.y1) and (abs(self.x0-self.x1) == 1)):
				return True
			return False
		
		def EqualP(self, rhs):
			return ((self.x0 == rhs.x0) and
					(self.y0 == rhs.y0) and
					(self.x1 == rhs.x1) and
					(self.y1 == rhs.y1))
		
		def MakeKey(self):
			return '_'.join([str(self.x0), str(self.x1), str(self.y0), str(self.y1)])
		
		def NextPositions(self):
			rv=[]
			if((self.x0 == self.x1) and (self.y0 == self.y1)):
				rv.append(self.Solver.BlockPos(self.x0,self.y0+1,self.x0,self.y0+2))
				rv.append(self.Solver.BlockPos(self.x0,self.y0-1,self.x0,self.y0-2))
				rv.append(self.Solver.BlockPos(self.x0+1,self.y0,self.x0+2,self.y0))
				rv.append(self.Solver.BlockPos(self.x0-1,self.y0,self.x0-2,self.y0))
			elif(self.x0 == self.x1):
				rv.append(self.Solver.BlockPos(self.x0+1,self.y0,self.x1+1,self.y1))
				rv.append(self.Solver.BlockPos(self.x0-1,self.y0,self.x1-1,self.y1))
				rv.append(self.Solver.BlockPos(self.x0,self.y0-1,self.x1,self.y1-2))
				rv.append(self.Solver.BlockPos(self.x0,self.y0+2,self.x1,self.y1+1))	
			elif(self.y0==self.y1):
				rv.append(self.Solver.BlockPos(self.x0,self.y0+1,self.x1,self.y1+1))
				rv.append(self.Solver.BlockPos(self.x0,self.y0-1,self.x1,self.y1-1))
				rv.append(self.Solver.BlockPos(self.x0-1,self.y0,self.x1-2,self.y1))
				rv.append(self.Solver.BlockPos(self.x0+2,self.y0,self.x1+1,self.y1))
			else:
				#Split cubes; we don't currently handle this
				#(Note that not all split-cube cases will be detected here)
				return None
			return rv

		def Render(self, gameId, blockId):
			Erase(blockId)
			img; x = 0; y = 0
			if((self.x0 == self.x1) and (self.y0 == self.y1)):
				img = MakeImage('block_v')
				x=self.x0, y=self.y0
			elif(self.x0 == self.x1):
				img = MakeImage('block_ns')
				x=self.x1, y=self.y1
			elif(self.y0 == self.y1):
				img = MakeImage('block_ew')
				x=self.x1, y=self.y1
			if not img: return
			#img.id = blockId
			#img.style.left	= m.bvP[0][0]*x + m.bvP[0][1]*y + m.bvP[0][2] + 'px';
			#img.style.top	= m.bvP[1][0]*x + m.bvP[1][1]*y + m.bvP[1][2] + 'px';
			#add(img)
		#remove something
		def Erase(self, blockId):
			pass
	
	#Class Object
	class Cell(object):

		"""docstring for Cell"""
		def __init__(self, x, y, ttype, bOccupied, bAvoid, bGoal):
			super().__init__()
			self.x = x
			self.y = y
			self.ttype=ttype
			self.bOccupied=bOccupied
			self.bAvoid=bAvoid
			self.bGoal=bGoal
			

		def Load(self, data):
			#print("hehe", data[0], data[1])
			code = int(data[1])
			self.ttype = data[0]
			self.bOccupied = (code&4)
			self.bAvoid = (code&2)
			self.bGoal = (code&1)
			return self
		
		def Save(self):
			return self.ttype + str(4 if self.bOccupied else 0) + str(2 if self.bAvoid else 0) + str(1 if self.bGoal else 0) 
	
		def Render(self, btn):
			className = ''
			if(self.bOccupied):
				className += 'occupied'
			if(self.bAvoid and (self.ttype == 'O' or (self.ttype == 'X') or (self.ttype == 'S'))):
				className += 'avoid'
			if(self.bGoal):
				className += 'goal'
			if(not className):
				className = 'normal'	
			if(btn):
				color = COLOROCCUPIED if(self.bOccupied) \
								else COLORAVOID if (self.bAvoid) \
								else COLORGOAL if(self.bGoal) \
								else COLORDEFAULT
				btn.config(text=self.ttype, command=None, bg=color)
			else:
				self.getImages()
		
		def getImages(self):
			pass
		
		def LegalP(self, pressure):
			if(self.ttype == 'O'):
				return not self.bAvoid
			elif(self.ttype == 'X' or self.ttype == 'S'):
				return ((pressure<=1) or not self.bAvoid)
			elif(self.ttype == 'N'):
				return True
			elif(self.ttype == 'W'):
				return (pressure<=1)
			elif(self.ttype == '#'):
				return True
			else:
				return False
			
	#Class Object
	class Board(object):

		"""docstring for Boar"""
		def __init__(self, GameBoard=None, Solver=None):
			super().__init__()
			
			self.Solver = Solver
			self.GameBoard = GameBoard
			self.data = json.load(open('maps.json'))
			self.maps = self.data['maps']

			self.Cttype=None
			self.CbOccupied=None
			self.CbAvoid=None
			self.CbGoal=None
			self.ListenerChange=False
				
			self.size = len(self.maps[0]['data'])
			
			self.cells = [[0 for x in range(self.size)] for y in range(self.size)] 

			self.arrayButton = [[0 for x in range(self.size)] for y in range(self.size)] 

			#def initArrayButton():
			#	if(self.arrayButton[self.size-1][self.size-1] == 0):			
			#print("bg")
			for y in range(self.size):
				frBtn= Frame(self.GameBoard)
				for x in range(self.size):
					self.cells[y][x] = self.Solver.Cell(x, y, '.', False, False, False)
					
					setAction=partial(self.Solver.HandleFieldClick, x, y)
					
					self.arrayButton[y][x] = Button(frBtn, text=".", command=setAction, bg=COLORDEFAULT, width=OSWIDTH)
					self.arrayButton[y][x].pack(side=LEFT)
					#self.GetCell(x, y).Render(self.arrayButton[y][x])
				frBtn.pack()
			#print("en")
			#self.initArray.cancel()				
			#self.initArray = setInterval(initArrayButton, 1)
			#self.initArray.start()

		def CalcOrdinal(self, x, y):
			return (y+1)*self.size-x
		
		def GetCell(self, x, y):
			if (self.cells[y] and self.cells[y][x]):				
				return self.cells[y][x]
			else:				
				return self.Solver.Cell(x, y, '.', False, False, False)	

		def SetAttr(self, x, y, name, value):
			if value == None:
				setattr(self.GetCell(x,y), name, not getattr(self.GetCell(x, y), name))
			else:
				setattr(self.GetCell(x,y), name, value)
			#self.GetCell(x,y).SetAttr(name,value)
		
		def DrawLevel(self, level):
			self.GameBoard.config(text="[Game Board: ] - "+" ["+level+"]")
			for i in range(len(self.maps)):
				if self.maps[i]['name'] == level:
					for row in range(len(self.maps[i]['data'])):
						for col in range(len(self.maps[i]['data'][0])):
							"""get data to cell"""
							self.cells[row][col].Load(self.maps[i]['data'][row][col])
							st = self.cells[row][col].ttype
							color = COLOROCCUPIED if(self.cells[row][col].bOccupied) \
								else COLORAVOID if (self.cells[row][col].bAvoid) \
								else COLORGOAL if(self.cells[row][col].bGoal) \
								else COLORDEFAULT
							self.arrayButton[row][col].config(text=st, bg=color)
							#self.arrayButton[row][col].pack(side=LEFT)
					return True
			return False
		
		#dontcare
		def Save(self):
			rv = [[None]*self.size]*self.size
			for y in range(self.size):
				for x in range(self.size):
					rv[y][x] = self.cells[y][x].Save()
			return rv
		
		def Render2D(self, editID):
			#btn
			#GetCell(x,y).Render(btn)
			#print("ok")
			return 0


		#get later, more UI	
		def RenderIso(self, gameId):
			#img
			#img = GetCell(x,y).Render()
			#_ord_ = CalcOrdinal(x, y)
			#print("ok")
			return 0
		
		#get later, change map
		def RenderCell2D(self,x,y):
			#btn
			#GetCell(x,y).Render(btn)
			
			btn = self.arrayButton[y][x]
			#print(x, y, btn["text"])
			self.GetCell(x,y).Render(btn)
			
		#get later
		def RenderCellIso(self,x,y):
			#img = GetCell(x, y).Render()
			#ord = CalcOrdinal(x, y)
			#print("ok")
			return 0
		
		def GetMarkedPos(self, testFxn, desc):
			cell = []
			cells = []
			for y in range(self.size):
				for x in range(self.size):
					cell = self.GetCell(x, y)
					if(testFxn(cell)):
						cells.append(cell)
			if(len(cells) == 0):
				messagebox.showinfo("Hey You!", "At least one cell must be marked as !" + desc)
			elif(len(cells) == 1):
				return self.Solver.BlockPos(cells[0].x, cells[0].y, cells[0].x, cells[0].y)
			elif(len(cells)==2):
				p = self.Solver.BlockPos(cells[0].x, cells[0].y, cells[1].x, cells[1].y)
				if(not p.Joined()):
					messagebox.showinfo("Hey You!!", "Cells marked as " + desc + " must be adjacent")
				else:
					return p
			else:
				messagebox.showinfo("Hey You!!", "No more than 2 cells may be marked as " + desc)
		
		def GetStartPos(self):
			def f(cell): return cell.bOccupied
			return self.GetMarkedPos(f,'occupied')
		
		def GetEndPos(self):
			def f(cell): return cell.bGoal
			return self.GetMarkedPos(f, 'goal')
		
		def FilterPositions(self,a):
			p = []
			rv = []
			for i in range(len(a)):
				p=a[i]
				if((p.x0 == p.x1) and (p.y0 ==p.y1)):
					if(self.GetCell(p.x0, p.y0).LegalP(2)):
						rv.append(p)
				else:
					if(self.GetCell(p.x0, p.y0).LegalP(1) and self.GetCell(p.x1, p.y1).LegalP(1)):
						rv.append(p)
			#print(len(rv))
			
			return rv
		
		def PathFindBFS(self,startPos, endPos):
			queue = []
			prevLUT = {}
			queue.append(endPos)
			prevLUT[endPos.MakeKey()] = None
			a =[[0 for x in range(self.size)] for y in range(self.size)] 
			while len(queue):
				p =  queue.pop(0)
				a = self.FilterPositions(p.NextPositions())
				for i in range(len(a)):
					np = a[i] 
					k = np.MakeKey()
					if(k in prevLUT):
						continue
					queue.append(np)
					prevLUT[k]=p
					if(np.EqualP(startPos)):
						queue = []
						break
			rv = []
			p = startPos
			k = p.MakeKey()
			rv.append(p)
			while True:
				np = prevLUT[k]
				if(np == None):
					break
				p = np
				k = p.MakeKey()
				rv.append(p)
			
			if(rv[len(rv)-1].EqualP(endPos)):
				return rv

	def get_BlockPos(self):
		return self.BlockPos(self)

	def get_Cell(self):
		return self.Cell(self)
	
	def get_Board(self):
		return self.Board(self)

class GameBoardApp(Frame):

	def __init__(self, master=None, size=0, data=None):
		super().__init__(master)

		self.mvP = [[32, 10, -77], [-5, 16, 62]]
		self.bvP = [[32, 10, -153], [-5, 16, -28]]

		self.size = size
		self.width, self.height = size*49, size*25
		self.GameFrame = LabelFrame(master, text="[Game Board: ]")
		self.NoteFrame = LabelFrame(master, text="[Note: ]")
		self.ControlFrame = LabelFrame(master, text="[Control Panel: ]")
		self.master = master

		self.listDescription = {
			'O': 'Soft Plate',
			'X': 'Hard Plate',
			'S': 'Splitter',
			'N': 'Normal Cell',
			'W': 'Weak Cell',
			'#': 'Destination Cell',
			'.': 'Empty Cell',
		}
		self.listPathImage = {
			'O': 'images/SoftPlate.png',
			'X': 'images/HardPlate.png',
			'S': 'images/Splitter.png',
			'N': 'images/NormalCell.png',
			'W': 'images/WeakCell.png',
			'#': 'images/DestinationCell.png',
			'.': 'images/Empty.png',
		}

		self.listMark = {
			'1': 'Mark/Clear Occupied Flag',
			'2': 'Mark/Clear Forbidden Flag\n(Plates and Splitters only)',
			'3': 'Mark/Clear Goal Flag'
		}

		"""Variable for current index"""

		#Cursor state
		self.actionName = None
		self.actionValue = None

		#Animation Control
		self.hInterval = None
		self.msDelay = 1
		self.path = None
		self.location = 0

		#mode default
		self.mode = 'edit'

		""""""
		self.init_window()


	def init_window(self):
		
		self.master.title("My Board Bloxor AI Solver")

		#self.master.update_idletasks()
		w = self.master.winfo_screenwidth()
		h = self.master.winfo_screenheight()
		size = (self.width, self.height)
		x = w/2 - size[0]/2
		y = h/2 - size[1]/2
		self.master.geometry("%dx%d+%d+%d" % (size + (x, y)))

		self.GameFrame.pack(side = LEFT, fill="both", expand=1)
		self.NoteFrame.pack(side = TOP, fill="y")
		self.ControlFrame.pack(side = BOTTOM, fill="both")
		self.pack(fill=BOTH, expand=1)
		
		self.GetGameBoard()
		self.GetMenu()
		self.GetNote()
		self.GetControl()

		#self.RenderBoard()
		#self.RenderControls()
		

	def ShowIntro(self):
		pass

	def HideIntro(self):
		pass

	#ok
	def SetMode(self, mode):
		"""getmode of game"""
		self.mode = mode
		self.RenderBoard()
		self.RenderBlock()
		self.RenderControls()
		return False

	def GetGameBoard(self):
		self.Solver = Solver(self)
		self.board = self.Solver.Board(self.GameFrame, self.Solver)

	#ok
	def GetNote(self):
		for key in self.listDescription.keys():
			frameLb = Frame(self.NoteFrame)
			setAction=partial(self.SetAction, 'ttype', key)
			Button(frameLb, text="[ %s ] - %s"%(key, self.listDescription[key]),command=setAction, width=18).pack(side=LEFT)
			load = Image.open(self.listPathImage[key])
			render = ImageTk.PhotoImage(load)
			img = Label(frameLb, image=render, text="X")
			img.image = render
			img.pack(side=LEFT)
			frameLb.pack(anchor=W)
		
		#Label(self.NoteFrame, text="------------").pack()
		
		for key in range(1,4):
			color = COLOROCCUPIED if(key==1) else COLORAVOID if (key == 2) else COLORGOAL
			name = 'bOccupied' if(key==1) else 'bAvoid' if (key == 2) else 'bGoal'
			frameLb = Frame(self.NoteFrame)
			setAction=partial(self.SetAction, name)
			Button(frameLb, text="[@]",command=setAction, width=5, bg=color).pack(side=LEFT)
			Label(frameLb, text=self.listMark[str(key)]).pack(side=RIGHT)
			frameLb.pack(anchor=W)

	#ok
	def GetControl(self):

		frSolve = Frame(self.ControlFrame)
		btnSolve = Button(frSolve, text="Solve This Level", command=self.Solve, width= 20).pack()
		frSolve.pack(anchor=CENTER)

		frStart = Frame(self.ControlFrame)
		btnStart = Button(frStart, text="Start SBS", command=self.StartAnimation, width=20).pack()
		frStart.pack(anchor=CENTER)

		frStop = Frame(self.ControlFrame)
		btnStop = Button(frStop, text="Stop SBS", command=self.StopAnimation, width=20).pack()
		frStop.pack(anchor=CENTER)

		frCont = Frame(self.ControlFrame)
		btnCont = Button(frCont, text="Reset Game", command=self.ResetAnimation, width=20).pack()
		frCont.pack(anchor=CENTER)
		#maximum = 100
		#interval = 10
		# self.progressbar = ttk.Progressbar(self.ControlFrame, orient=HORIZONTAL,
        #                                   mode="indeterminate",
        #                                  maximum=100)
		# self.progressbar.pack(side=TOP)
		# #progressbar.destroy()
		# self.prog_bar = setInterval(self.progressbar.start(interval=10), 1)

	#ok
	def GetMenu(self):
		#creating a menu instance
		menu = Menu(self.master)
		self.master.config(menu=menu)

		#create the file object
		view = Menu(menu, tearoff=0)
		#view.add_command(label="Edit View", command=self.prog_bar.pb_start, activebackground=COLORGREY)
		#view.add_command(label="Game View", command=self.prog_bar.pb_stop, activebackground=COLORGREY)
		
		view.add_command(label="Edit View", command=self.EditView, activebackground=COLORGREY)
		view.add_command(label="Game View", command=self.GameView, activebackground=COLORGREY)
		
		loadlevel1 = Menu(menu, tearoff=0)
		for i in range(1,10):
			if (i==2):
				for c in range(ord('A'),ord('C')+1):
					st = "Level " + str(i)+chr(c)
					level=partial(self.GetLevel, st)
					loadlevel1.add_command(label=st, command=level, activebackground=COLORGREY)
				loadlevel1.add_separator()
			elif (i==5):
				for c in range(ord('A'),ord('E')+1):
					st = "Level " + str(i)+chr(c)
					level=partial(self.GetLevel, st)
					loadlevel1.add_command(label=st, command=level, activebackground=COLORGREY)
				loadlevel1.add_separator()
			elif (i==7 or i==8 or i==9):
				for c in range(ord('A'),ord('B')+1):
					st = "Level " + str(i)+chr(c)
					level=partial(self.GetLevel, st)
					loadlevel1.add_command(label=st, command=level, activebackground=COLORGREY)
				loadlevel1.add_separator()
			else:
				st = "Level " + str(i)
				level=partial(self.GetLevel, st)
				loadlevel1.add_command(label=st, command=level, activebackground=COLORGREY)
				loadlevel1.add_separator()

		loadlevel2 = Menu(menu, tearoff=0)
		for i in range(10,16):
			if (i==10 or i==12 or i==14 or i==15):
				for c in range(ord('A'),ord('C')+1):
					st = "Level " + str(i)+chr(c)
					level=partial(self.GetLevel, st)
					loadlevel2.add_command(label=st, command=level, activebackground=COLORGREY)
				loadlevel2.add_separator()
			else:
				st = "Level " + str(i)
				level=partial(self.GetLevel, st)
				loadlevel2.add_command(label=st, command=level, activebackground=COLORGREY)
				loadlevel2.add_separator()

		loadlevel3 = Menu(menu, tearoff=0)
		for i in range(16,20):
			if (i==17):
				for c in range(ord('A'),ord('E')+1):
					st = "Level " + str(i)+chr(c)
					level=partial(self.GetLevel, st)
					loadlevel3.add_command(label=st, command=level, activebackground=COLORGREY)
				loadlevel3.add_separator()
			elif(i==16):
				for c in range(ord('A'),ord('H')+1):
					st = "Level " + str(i)+chr(c)
					level=partial(self.GetLevel, st)
					loadlevel3.add_command(label=st, command=level, activebackground=COLORGREY)
				loadlevel3.add_separator()
			else:
				for c in range(ord('A'),ord('D')+1):
					st = "Level " + str(i)+chr(c)
					level=partial(self.GetLevel, st)
					loadlevel3.add_command(label=st, command=level, activebackground=COLORGREY)
				loadlevel3.add_separator()

		loadlevel4 = Menu(menu, tearoff=0)
		for i in range(20,25):
			if (i==20 or i==21):
				for c in range(ord('A'),ord('B')+1):
					st = "Level " + str(i)+chr(c)
					level=partial(self.GetLevel, st)
					loadlevel4.add_command(label=st, command=level, activebackground=COLORGREY)
				loadlevel4.add_separator()
			elif (i==22):
				for c in range(ord('A'),ord('C')+1):
					st = "Level " + str(i)+chr(c)
					level=partial(self.GetLevel, st)
					loadlevel4.add_command(label=st, command=level, activebackground=COLORGREY)
				loadlevel4.add_separator()
			elif (i==23):
				for c in range(ord('A'),ord('D')+1):
					st = "Level " + str(i)+chr(c)
					level=partial(self.GetLevel, st)
					loadlevel4.add_command(label=st, command=level, activebackground=COLORGREY)
				loadlevel4.add_separator()
			else:
				for c in range(ord('A'),ord('F')+1):
					st = "Level " + str(i)+chr(c)
					level=partial(self.GetLevel, st)
					loadlevel4.add_command(label=st, command=level, activebackground=COLORGREY)
				loadlevel4.add_separator()
		
		loadlevel5 = Menu(menu, tearoff=0)
		for i in range(25,29):
			if (i==25 or i==26):
				for c in range(ord('A'),ord('D')+1):
					st = "Level " + str(i)+chr(c)
					level=partial(self.GetLevel, st)
					loadlevel5.add_command(label=st, command=level, activebackground=COLORGREY)
				loadlevel5.add_separator()
			else:
				for c in range(ord('A'),ord('B')+1):
					st = "Level " + str(i)+chr(c)
					level=partial(self.GetLevel, st)
					loadlevel5.add_command(label=st, command=level, activebackground=COLORGREY)
				loadlevel5.add_separator()


		loadlevel6 = Menu(menu, tearoff=0)
		for i in range(29,34):
			if (i==29):
				for c in range(ord('A'),ord('G')+1):
					st = "Level " + str(i)+chr(c)
					level=partial(self.GetLevel, st)
					loadlevel6.add_command(label=st, command=level, activebackground=COLORGREY)
				loadlevel6.add_separator()
			elif (i==30):
				for c in range(ord('A'),ord('E')+1):
					st = "Level " + str(i)+chr(c)
					level=partial(self.GetLevel, st)
					loadlevel6.add_command(label=st, command=level, activebackground=COLORGREY)
				loadlevel6.add_separator()
			elif (i==31 or i==32):
				for c in range(ord('A'),ord('D')+1):
					st = "Level " + str(i)+chr(c)
					level=partial(self.GetLevel, st)
					loadlevel6.add_command(label=st, command=level, activebackground=COLORGREY)
				loadlevel6.add_separator()
			else:
				for c in range(ord('A'),ord('B')+1):
					st = "Level " + str(i)+chr(c)
					level=partial(self.GetLevel, st)
					loadlevel6.add_command(label=st, command=level, activebackground=COLORGREY)
				loadlevel6.add_separator()

		option = Menu(menu, tearoff=0)
		option.add_command(label="Reset Board", command=self.ResetBoard, activebackground=COLORGREY)
		option.add_command(label="Quit", command=self.Exit, activebackground=COLORGREY)
		
		#added "file" and "edit" to out menu
		menu.add_cascade(label="View", menu=view)
		menu.add_cascade(label="Level(1-9)", menu=loadlevel1)
		menu.add_cascade(label="Level(10-15)", menu=loadlevel2)
		menu.add_cascade(label="Level(16-20)", menu=loadlevel3)
		menu.add_cascade(label="Level(20-24)", menu=loadlevel4)
		menu.add_cascade(label="Level(25-29)", menu=loadlevel5)
		menu.add_cascade(label="Level(29-33)", menu=loadlevel6)
		menu.add_cascade(label="Option", menu=option)

	def Exit(self):
		self.StopAnimation()
		root.quit()

	#ok
	def EditView(self):
		self.SetMode('edit')
		print("EditView")

	#ok
	def GameView(self):
		self.SetMode('game')
		print("GameView")

	#not yet
	def GetLevel(self, level):
		self.StopAnimation()
		self.path = None
		self.board.DrawLevel(level)

	#dont care
	def FmtMaps(self):
		"""save map to json"""
		pass

	#ok
	def SetAction(self, name, value=None):
		#print(name, value)
		self.actionName = name
		self.actionValue = value

	#ok
	def TakeAcion(self, x, y):
		if((self.actionName != None) and (self.hInterval == None)):
			#print("board :",x, y)
			#print(self.actionName, self.actionValue)
			self.board.SetAttr(x, y, self.actionName, self.actionValue)
			self.RenderCell(x, y)
			self.path = None
			self.RenderControls()

	#ok
	def Solve(self):
		if(self.hInterval): return

		sPos = self.board.GetStartPos()
		ePos = self.board.GetEndPos()

		if(not sPos and not ePos): return
		if(len(self.board.FilterPositions([sPos, ePos])) != 2):
			messagebox.showinfo("Hey You!", "Start and/or goal positions are illegal!")

		path = self.board.PathFindBFS(sPos, ePos)

		if(not path):
			messagebox.showinfo("So Sorry!", "Destination unreachable!,\n Could not find any path")
		else:
			self.path = path
			self.location = 0
			messagebox.showinfo("Yeah Found Path!", "OKKKKK, Let's Start Step By Step Animation")
			#self.StartAnimation()

	#def Clear
	def ResetBoard(self):
		print("ResetBoard")
		self.GetLevel('Empty')
	#ok
	def StartAnimation(self):
		if(not self.hInterval and self.path):
			#self.Solve()
			o = self
			def f(): o.Animate()
			self.hInterval = setInterval(f, self.msDelay)
			self.hInterval.start()
			#self.prog_bar.start()
			self.RenderBoard()
			self.RenderControls()
		else:
			messagebox.showinfo("Dear Sir!", "You have not solved this Level yet!!")

	def ResetAnimation(self):
		if(self.path):
			cp = self.path[self.location]
			self.location = 0
			np = self.path[self.location]
			self.Move(cp, np)

	def StopAnimation(self):
		if(self.hInterval):
			#stop thread
			#self.prog_bar.cancel()
			self.hInterval.cancel()
			self.hInterval = None
			#self.path[self.location].Erase('block_img')
			self.RenderControls()
	
	def Move(self, oldPos, newPos):
		#clear current occupied position
		self.board.SetAttr(oldPos.x0, oldPos.y0, 'bOccupied', False)
		self.board.SetAttr(oldPos.x1, oldPos.y1, 'bOccupied', False)
		self.RenderCell(oldPos.x0, oldPos.y0)
		self.RenderCell(oldPos.x1, oldPos.y1)

		#draw new occupied position
		self.board.SetAttr(newPos.x0, newPos.y0, 'bOccupied', True)
		self.board.SetAttr(newPos.x1, newPos.y1, 'bOccupied', True)
		self.RenderCell(newPos.x0, newPos.y0)
		self.RenderCell(newPos.x1, newPos.y1)

		#draw the block
		self.RenderBlock()

	def Animate(self):
		if(self.path):
			cp = self.path[self.location]		
			print(cp.x0, cp.y0, cp.x1, cp.y1)		
			self.location = (self.location+1) % len(self.path)	
			np = self.path[self.location]
			self.Move(cp, np)

	def RenderBoard(self):
		if(self.mode == 'edit'):
			self.board.Render2D('field')
			#self.Render2D()
		elif(self.mode == 'game'):
			self.board.RenderIso('gameboard')

	def RenderCell(self,x,y):
		if(self.mode == 'edit'):
			#print(x, y)
			self.board.RenderCell2D(x,y)
		elif(self.mode == 'game'):
			self.board.RenderCellIso(x,y)

	def RenderBlock(self):
		if ((self.mode == 'game') and self.hInterval):	
			self.path[self.location].Render('gameboard', 'block_img');
	
	#TODO
	def RenderControls(self):
		pass

class setInterval():
	def __init__(self, func, sec):
		def func_wrapper():
			self.t = threading.Timer(sec, func_wrapper)
			self.t.start()
			func()
		self.t = threading.Timer(sec, func_wrapper)
		#self.t.start()	
    
	def cancel(self):
		self.t.cancel()

	def start(self):
		self.t.start()

if __name__ == '__main__':
	root = Tk()
	root.iconbitmap('@images/person.xbm')
	#root.resizable(False,False)
	app = GameBoardApp(master=root, size=SIZE)
	app.mainloop()