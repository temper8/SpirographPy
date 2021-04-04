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
    
	def __init__(self, root):
		frame_a = tk.Frame()
		frame_b = tk.Frame()
		self.canvas = tk.Canvas(frame_a, width=self.width, height=self.height)
		self.canvas.pack()


		var = tk.DoubleVar()
		slider1 = tk.Scale( frame_b, variable = var, orient = tk.HORIZONTAL, length = 150, command = self.Slider1Moved )
		slider1.pack(anchor=tk.CENTER)

		var2= tk.DoubleVar()
		slider2 = tk.Scale( frame_b, variable = var2, orient = tk.HORIZONTAL, length =150, command = self.Slider2Moved )
		slider2.pack(anchor=tk.CENTER)

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
		#self.GeneratePalette()
		#self.draw_init()
		frame_a.pack(side="left")
		frame_b.pack(side="left")
		self.spiro = Spiro(self.width,self.height)  
		self.draw(0)


	def draw(self,t):
		pim = self.spiro.RenderMap(t)
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
			self.canvas.after(50, self.animate) 

	def start(self):
		self.stop_flag = False
		self.ani_count = 0
		self.animate()

	def stop(self):
		self.stop_flag = True

	def Slider1Moved(self, v):
		print("s1 =" ,  v)
		t = int(v)/100.0
		self.start_time = t
		self.draw(t)
		self.label_a["text"] = "t = " + "{:5.3f}".format(t)	


	def Slider2Moved(self, v):
		#print(v)
		t = self.start_time
		phi =  int(v)/150.0
		print(phi)
		pim = self.spiro.Render2(t,phi)
		self.SaveImage(pim)
		self.photo = ImageTk.PhotoImage(pim)
		self.im = self.canvas.create_image(0,0, image=self.photo, anchor='nw')
		self.label_a["text"] = "t = " + "{:5.3f}".format(t)	