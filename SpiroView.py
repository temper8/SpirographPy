import tkinter as tk
import math
import aggdraw
import random
import timeit

from PIL import Image, ImageDraw, ImageTk
from math import sin, cos, pi
from Render import Spiro
def my_callback(var, indx, mode):
	print(var)
	#print("Traced variable {}".format(var.get()))

class SpiroView:

	Parameters ={"Width": 700, "Height": 700, "Radius" : 350, "Time": 0.0, "Shift": 1.0}
	Vars = {}

	def UpdateVar(self, var):
		print(var + " = {}".format(self.Vars[var].get()))
		self.Draw()

	def make_slider(self, parent, var, interval, label, cmd = None):
		#var = tk.DoubleVar(name = VarName)
		self.Vars[var._name] = var
		var.trace_add('write', lambda var, indx, mode: self.UpdateVar(var))
		#res = (interval[1] - interval[0])/100
		slider = tk.Scale( parent, variable = var, orient = tk.HORIZONTAL, from_=interval[0], to=interval[1], resolution=interval[2], length = 250, command = cmd )
		slider.pack(anchor=tk.CENTER)
		label = tk.Label(master=parent, text=label)
		label.pack(side = 'top')
		return var		

	def __init__(self, root):
		w = self.Parameters["Width"]
		h = self.Parameters["Height"]
		frame_a = tk.Frame()
		frame_b = tk.Frame()
		self.canvas = tk.Canvas(frame_a, width=w, height=h)
		self.canvas.pack()

		v = tk.IntVar(name = "K")
		self.make_slider( frame_b, label ="K", var = v, interval = (1, 30, 1))

		v = tk.IntVar(name = "K1")
		self.make_slider( frame_b, label ="K1", var = v, interval = (-20, 20, 1))

		v = tk.IntVar(name = "K2")
		self.make_slider( frame_b, label ="K2", var = v, interval = (1, 30, 1))

		v = tk.IntVar(name = "M")
		self.make_slider( frame_b, label ="Number of lines", var = v, interval = (100, 10000, 100))

		v = tk.DoubleVar(name = "Shift")
		self.make_slider( frame_b, label ="shift slider", var = v, interval = (0.01, 1.0, 0.01))

		v = tk.DoubleVar(name = "Time")
		self.make_slider( frame_b, label ="time slider", var = v, interval = (0.0, 1.0, 0.01))

		self.saveFlag = tk.BooleanVar()
		self.saveFlag.set(0)
		chk1 = tk.Checkbutton(frame_b, text="Save",
                 variable=self.saveFlag,
                 onvalue=1, offvalue=0)
		chk1.pack(side = 'top')

		self.label_fps = tk.Label(master=frame_b, text="fps")
		self.label_fps.pack(side = 'top')

		self.label_a = tk.Label(master=frame_b, text="time")
		self.label_a.pack(side = 'top')
		
		tk.Button(frame_b, text = " start ",  command = self.start).pack(side="top")
		tk.Button(frame_b, text = " stop ",  command = self.stop).pack(side="top")
		tk.Button(frame_b, text = " plus ",  command = self.plus).pack(side="top")
		#self.GeneratePalette()
		#self.draw_init()
		
		self.RenderVar = tk.IntVar(name = "RenderType")
		self.Vars[self.RenderVar._name] = self.RenderVar
		self.RenderVar.set(0)
		tk.Radiobutton(frame_b, text="IggDraw", variable=self.RenderVar, value = 0, command=lambda : self.update()).pack(side="top")
		tk.Radiobutton(frame_b, text="Cairo", variable=self.RenderVar, value = 1, command=lambda : self.update()).pack(side="top")

		frame_a.pack(side="left")
		frame_b.pack(side="left")
		self.spiro = Spiro(self.Parameters)  
		self.Draw()

	def update(self):
		t = self.ani_count/400
		#self.draw(t)


	def Draw(self):
		pim = self.spiro.Render2(self.Vars)
		self.SaveImage(pim)
		self.photo = ImageTk.PhotoImage(pim)
		self.im = self.canvas.create_image(0,0, image=self.photo, anchor='nw')


	def SaveImage(self, pim):
		if self.saveFlag.get():
			fn = "tmp\\{0:05d}.png".format(self.ani_count)
			print(fn)
			pim.save(fn, "PNG")

	ani_count = 0
	stop_flag = False

	fc = 0
	fps = 0
	start_time = 0
	def FPS(self):
		if self.fc == 0 :
			self.start_time = timeit.default_timer()
		self.fc = self.fc + 1
		if self.fc>10:
			dt = timeit.default_timer() - self.start_time
			self.fps = self.fc / dt
			self.fc = 0
		self.label_fps["text"] = "fps = " + "{:5.2f}".format(self.fps)	
		

	def animate(self):
		self.FPS()
		t = self.ani_count/400
		self.Vars["Time"].set(t)
		self.label_a["text"] = "t = " + "{:5.3f}".format(t)
		self.ani_count +=  1
		if not self.stop_flag and (self.ani_count<8000):
			self.canvas.after(10, self.animate) 

	def start(self):
		self.stop_flag = False
		self.ani_count = 0
		self.animate()

	def plus(self):
		self.stop_flag = False
		self.ani_count += 1
		t = self.ani_count/400
		self.draw(t)
		self.label_a["text"] = "t = " + "{:5.3f}".format(t)

	def stop(self):
		self.stop_flag = True


	def Slider1Moved(self, v):
		#self.Parameters["Time"] = int(v)/100.0
		self.DrawEx()
		#self.label_a["text"] = "t = " + "{:5.3f}".format(self.Parameters["Time"])	

	def Slider2Moved(self, v):
		#self.Parameters["Shift"] = int(v)/150.0
		self.DrawEx()
		#self.label_a["text"] = "t = " + "{:5.3f}".format(self.Parameters["Time"])	
	
