import tkinter as tk
import math
import aggdraw
import random
import timeit
import time

from PIL import Image, ImageDraw, ImageTk
from cairo import ImageSurface, Context, FORMAT_ARGB32
from math import sin, cos, pi

class Spiro:
	width = 640
	height = 640
	radius = 300

	COLORS_NUMBER = 512
	Pens = []
	Colors = []

	def GeneratePalette(self):
		bi = 64.0/256
		for i in range(0, self.COLORS_NUMBER):
			alpha = 30
			r = int((random.random()*(1.0 - bi) + bi) * 256)
			g = int((random.random()*(1.0 - bi) + bi)*256)
			b = int((random.random()*(1.0 - bi) + bi)*256)
			# print(r,g,b)
			self.Colors.append((r, g, b))
			self.Pens.append(aggdraw.Pen((r, g, b), 0.5, alpha))


	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.GeneratePalette()

	def RenderCairo(self, t):
		self.surface = ImageSurface(FORMAT_ARGB32, self.width, self.height)
		self.context = Context(self.surface)
		# Draw something
		self.t = t
		tt = 1.5*t
		M = 5000
		Z = (2*math.pi*i/M for i in range(0, int(M)))
		lines = ([self.FF(z,tt), self.FF(z + 1.2*math.pi,tt)] for z in Z)
		#self.draw_cr_lines(lines)
		self.draw_cr_polygons(lines)
		self.context.fill()
		pim = Image.frombuffer("RGBA", (self.width, self.height), self.surface.get_data(), "raw", "RGBA", 0, 1)
		return pim

	def Render(self, t):
		self.t = t
		pim = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 64))
		self.drw = aggdraw.Draw(pim)
		M = 1000
		for i in range(0, int(M)):
			z =2*math.pi*i/M
			xy0 = self.FF(z,t)
			xy1 = self.FF(z + math.pi, t)
			self.draw_line(xy0, xy1)
		self.drw.flush()
		return pim

	def RenderMap(self, t):
		self.t = 1.5*t
		pim = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 64))
		self.drw = aggdraw.Draw(pim)
		self.drw.setantialias(True)
		M = 6000
		Z = (2*math.pi*i/M for i in range(0, int(M)))
		lines = ([self.FF(z,t), self.FF(z + 1.9*math.pi,t)] for z in Z)
		#lines = map(lambda z:[self.Simple(z,t), self.Simple(z + math.pi/2,t)], Z)
		#lines = map(lambda z:[self.Rect(z,t), self.Rect(-z,t)], Z)
		self.draw_lines(lines)
		#self.draw_polygons(lines)
		self.drw.flush()
		return pim

	def Render2(self, t, phi):
		self.t = 1.5*t
		pim = Image.new('RGBA', (self.width, self.height), (255,255, 255, 255))
		self.drw = aggdraw.Draw(pim)
		self.drw.setantialias(True)
		M = 5500
		Z = (2*math.pi*i/M for i in range(0, int(M)))
		lines = ([self.FF(z,t), self.FF(z + phi*math.pi,t)] for z in Z)
		#self.draw_lines(lines)
		self.draw_polygons(lines)
		#Z = (2*math.pi*i/M for i in range(0, int(M)))
		#dots = (self.FF(z,t) for z in Z)
		#self.draw_dots(dots)
		self.drw.flush()
		return pim



	def FF(self, z, t):
		k = 1
		k1 =  math.trunc(2*t) -7
		k2 =12
		k3 = 8
		l = 0.5
		a =  0.5*sin(2*pi*t)
		b = 3/4#*cos(pi*t)
		c = 1/4
		x = cos(k*z) + a*cos(k1*z ) + b*cos(k2*z +7*pi*t) 
		y = sin(k*z) + a*sin(k1*z ) + b*sin(k2*z +7*pi*t) 
		r = 0.4
		return (self.width/2 + r*self.radius*x, self.height/2 + r*self.radius*y)	

	def Circle(self, z, t):
		k = 1
		x = cos(k*z)
		y = sin(k*z)
		r = 0.3#*math.fabs(sin(2*pi*t))
		return (self.width/2 + r*self.radius*x, self.height/2 + r*self.radius*y)	

	def Rect(self, z, t):
		k = 1
		x = z
		if z<0 : x = 1-z
		x = x - 2.0
		y = math.fabs(z) - 2.0
		r = 0.3
		return (self.width/2 + r*self.radius*x, self.height/2 + r*self.radius*y)	


	def draw_line(self,xy0, xy1):	
		pen = aggdraw.Pen("blue", 1.0, 10)
		self.drw.line((xy0[0], xy0[1], xy1[0], xy1[1]), pen)
		dot = aggdraw.Pen("blue", 1.0, 100)
		self.drw.line((xy0[0], xy0[1], xy0[0]+1, xy0[1]+1),dot)


	def avg_clr(self, i, d):
		c1 = self.Colors[i]
		c2=  self.Colors[i+1]
		r = int(c1[0]*(1-d) + c2[0]*d)
		g = int(c1[1]*(1-d) + c2[1]*d)
		b = int(c1[2]*(1-d) + c2[2]*d)
		return (r,g,b)

	penIndex = 0
	count = 0
	def GetPen(self):
		penIndex = (int)(self.penIndex / 25)
		d = self.penIndex / 25 - penIndex
		self.penIndex += 1
		return aggdraw.Pen(self.avg_clr(penIndex, d), 0.5, 80)
		

	def draw_dots(self,dots):	
		#pen = aggdraw.Pen("red", 0.5, 30)
		pen = aggdraw.Pen("blue", 1.0, 100)
		for d in dots:
			self.drw.rectangle((d[0], d[1], d[0]+1, d[1]+1), pen)

	

	def draw_cr_lines(self, lines):
		#self.context.rectangle(100, 50, 200 + t*100, 100 + t*100)
		for li in lines:
			self.context.move_to(li[0][0], li[0][1])
			self.context.line_to(li[1][0], li[1][1])				
			self.context.set_source_rgba(0.8, 0, 0, 0.1)
			self.context.set_line_width(2.0)
			self.context.stroke()

	def draw_cr_polygons(self, lines):
		#self.context.rectangle(100, 50, 200 + t*100, 100 + t*100)
		l = list(lines)
		for i, j in zip(l[0::], l[-1::]+l[0::1]):
			self.context.move_to(i[0][0], i[0][1])
			self.context.line_to(i[1][0], i[1][1])	
			self.context.line_to(j[1][0], j[1][1])	
			self.context.line_to(j[1][0], j[1][1])										
			self.context.set_source_rgba(0.8, 0, 0, 0.1)
			self.context.fill()


	def draw_lines(self,lines):	
		#pen = aggdraw.Pen("red", 0.5, 30)
		pen = self.GetPen()
		for l in lines:
			self.drw.line((l[0][0], l[0][1], l[1][0], l[1][1]), pen)
			#dot = aggdraw.Pen("blue", 1.0, 100)
			#self.drw.line((xy0[0], xy0[1], xy0[0]+1, xy0[1]+1),dot)

	def draw_polygons(self,lines):	
		pen = aggdraw.Pen("red",0.5, 0)
		l = list(lines)
		#for li in l:
		#	self.drw.line((li[0][0], li[0][1], li[1][0], li[1][1]), pen)
		br = aggdraw.Brush("red", 30)
		for i, j in zip(l[0::], l[-1::]+l[0::1]):
			p = aggdraw.Path([i[1][0], i[1][1], j[1][0], j[1][1], j[0][0], j[0][1], i[0][0], i[0][1]])
			self.drw.polygon(p, pen, br)
			#p = aggdraw.Path([j[0][0], j[0][1], j[1][0], j[1][1], i[0][0], i[0][1]])
			#self.drw.polygon(p, br)
		
	
