import tkinter as tk
import math
import aggdraw
import random
import timeit
import time
import cairo

from PIL import Image, ImageDraw, ImageTk
from cairo import ImageSurface, Context, FORMAT_ARGB32
from math import sin, cos, pi
from shapely.geometry import LineString


class Spiro:
	width = 440
	height = 440
	radius = 200

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
		M =1000
		Z = (2*math.pi*i/M for i in range(0, int(M)))
		lines = ([self.FF(z,tt), self.FF(z + 1.8*math.pi,tt)] for z in Z)
		self.draw_cr_test()
		self.draw_cr_polygons(lines)
		#self.draw_cr_lines(lines)
		self.context.fill()
		pim = Image.frombuffer("RGBA", (self.width, self.height), self.surface.get_data(), "raw", "RGBA", 0, 1)
		return pim

	def Render(self, t):
		self.t = t
		pim = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 64))
		self.drw = aggdraw.Draw(pim)
		M = 400
		for i in range(0, int(M)):
			z =2*math.pi*i/M
			xy0 = self.FF(z,t)
			xy1 = self.FF(z + math.pi, t)
			self.draw_line(xy0, xy1)
		self.drw.flush()
		return pim

	def RenderMap(self, t):
		self.t = t
		tt = 1.5*t
		pim = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 64))
		self.drw = aggdraw.Draw(pim)
		self.drw.setantialias(True)
		M = 5000
		Z = (2*math.pi*i/M for i in range(0, int(M)))
		lines = ([self.FF(z,tt), self.FF(z + 1.8*math.pi,tt)] for z in Z)
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
		k = 2
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

	def CreateLinearPattern(self, p):	
		linpat = cairo.LinearGradient(p[0][0],  p[0][1], p[1][0], p[1][1])
		d1 = math.dist(p[0],p[1])
		d2 = math.dist(p[2],p[3])
		#print(d1/d2)
		if d1>d2:
			linpat.add_color_stop_rgba(0.0, 0.0, 0.0, 1.0, 0.1)
			linpat.add_color_stop_rgba(1.0, 0.0, 0.0, 1.0, 0.3*d1/d2)
		else:
			linpat.add_color_stop_rgba(0.0, 0.0, 0.0, 1.0, 0.3*d2/d1)
			linpat.add_color_stop_rgba(1.0, 0.0, 0.0, 1.0, 0.1)		
		return linpat

	def draw_cr_lines(self, lines):
		#self.context.rectangle(100, 50, 200 + t*100, 100 + t*100)
		for li in lines:
			self.context.move_to(li[0][0], li[0][1])
			self.context.line_to(li[1][0], li[1][1])		
			self.context.set_source_rgba(0.8, 0, 0, 0.1)
			self.context.set_line_width(2.0)
			self.context.stroke()

	def poly(self, a, b):
		line1 = LineString([a[0], a[1]]) 
		line2 = LineString([b[0], b[1]]) 
		p = line1.intersection(line2)
		if p:
			#print(p.x,p.y) 
			pn = [a[0], b[0], (p.x, p.y) ,a[1], b[1]]
		else:
			pn = [a[0], a[1], b[1], b[0]]

		return pn

	def draw_cr_test(self):
		for i in range(100):
			for j in range(3):
				self.context.rectangle( i*5.0, j*30.0, 500 - i*5, 25)
				self.context.set_source_rgba( 0, 0, 1.0, 0.05)
				self.context.fill()


	def CreateLinearPattern2(self, p):	
		x = (p[0][0] + p[1][0])/2
		y = (p[0][1] + p[1][1])/2
		linpat = cairo.LinearGradient(x,  y, p[2][0], p[2][1])
		linpat.add_color_stop_rgba(0.0, 0.0, 0.0, 1.0, 0.1)
		linpat.add_color_stop_rgba(0.7, 0.0, 0.0, 1.0, 0.2)
		linpat.add_color_stop_rgba(0.8, 0.0, 0.0, 1.0, 0.3)
		linpat.add_color_stop_rgba(1.0, 0.0, 0.0, 1.0, 0.9)
		return linpat

	def draw_cr_triangle(self, p):
		self.context.move_to(p[0][0], p[0][1])
		self.context.line_to(p[1][0], p[1][1])
		self.context.line_to(p[2][0], p[2][1])
		self.context.close_path()
		lp = self.CreateLinearPattern2(p)
		self.context.set_source(lp)
		self.context.fill()

	def draw_cr_polygons(self, lines):

		#self.context.rectangle(100, 50, 200 + t*100, 100 + t*100)
		l = list(lines)
		x = 0.0
		dx = 1.0/len(l)
		#self.context.set_source_rgba(0.0, 0.0, 0.0, 1.0)					
		for i, j in zip(l[0::], l[-1::]+l[0::1]):
			
			p = self.poly(i,j)
			if len(p)>4:
				self.draw_cr_triangle(p[:3:])
				self.draw_cr_triangle([p[3],p[4],p[2]])
				self.context.set_source_rgba(1.0 , 0, 0.0, 0.1)
			else:
				self.context.move_to(p[0][0], p[0][1])
				self.context.line_to(p[1][0], p[1][1])
				#self.context.stroke()	
				self.context.line_to(p[2][0], p[2][1])	
				self.context.line_to(p[3][0], p[3][1])	
				#self.context.line_to(i[0][0], i[0][1])
				self.context.close_path()				
				self.context.set_source_rgba(0.0 , 0, 1.0, 0.1)	
				self.context.fill()
			x = x + 0
			#self.context.set_source_rgba(1.0 , 0, 0, 0.1)
			#self.context.stroke_preserve()
			#self.context.set_source_rgba(0.0 , 0, 1.0, 0.1)
			#lp = self.CreateLinearPattern(p)
			#self.context.set_source(lp)
			#self.context.fill()

		#self.context.move_to(l[0][0][0], l[0][0][1])
		#for li in l:
		#	self.context.line_to(li[0][0], li[0][1])
		#self.context.close_path()	
		#self.context.set_source_rgba(0.0, 0.0, 0.9, 1.0)
		#self.context.set_line_width(1.0)
		#self.context.stroke()			



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
		
	
