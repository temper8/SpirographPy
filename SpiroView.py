import tkinter as tk
import math
import aggdraw
import random
import timeit

from PIL import Image, ImageDraw, ImageTk
from math import sin, cos, pi
from Render import Spiro

class SpiroView:
	width = 700
	height = 700
	radius = 450
    
	def make_slider(self, parent, cmd):
		var = tk.DoubleVar()
		slider = tk.Scale( parent, variable = var, orient = tk.HORIZONTAL, length = 200, command = cmd )
		slider.pack(anchor=tk.CENTER)
		return var		

	def __init__(self, root):
		frame_a = tk.Frame()
		frame_b = tk.Frame()
		self.canvas = tk.Canvas(frame_a, width=self.width, height=self.height)
		self.canvas.pack()


		var = self.make_slider( frame_b, cmd = self.Slider1Moved)


		var2= self.make_slider( frame_b, cmd = self.Slider2Moved)


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
		
		self.RenderVar = tk.IntVar()
		self.RenderVar.set(0)
		tk.Radiobutton(frame_b, text="IggDraw", variable=self.RenderVar, value = 0, command=lambda : self.update()).pack(side="top")
		tk.Radiobutton(frame_b, text="Cairo", variable=self.RenderVar, value = 1, command=lambda : self.update()).pack(side="top")

		frame_a.pack(side="left")
		frame_b.pack(side="left")
		self.spiro = Spiro(self.width,self.height)  
		self.draw(0)

	def update(self):
		t = self.ani_count/400
		self.draw(t)


	def draw(self,t):
		print(self.RenderVar.get())
		if self.RenderVar.get() == 0:
			pim = self.spiro.RenderMap(t)
		else:	
			pim = self.spiro.RenderCairo(t)
		self.FPS()
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
		t = self.ani_count/200
		self.draw(t)
		self.label_a["text"] = "t = " + "{:5.3f}".format(t)
		self.ani_count = self.ani_count + 1
		if not self.stop_flag and (self.ani_count<4000):
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


	time_pos = 0
	shift = 0
	def Slider1Moved(self, v):
		print("s1 =" ,  v)
		t = int(v)/100.0
		self.time_pos = t
		self.DrawEx(t, self.shift)
		self.label_a["text"] = "t = " + "{:5.3f}".format(t)	

	def Slider2Moved(self, v):
		#print(v)
		self.shift =  int(v)/150.0
		self.DrawEx( self.start_time, self.shift)
		self.label_a["text"] = "t = " + "{:5.3f}".format(self.time_pos)	
	
	def DrawEx(self, t, shift):
		pim = self.spiro.Render2(t, shift)
		self.SaveImage(pim)
		self.photo = ImageTk.PhotoImage(pim)
		self.im = self.canvas.create_image(0,0, image=self.photo, anchor='nw')
