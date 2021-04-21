import tkinter as tk
import math
import aggdraw
import random
import timeit
import time
import cairo

from PIL import Image, ImageDraw, ImageTk

from math import sin, cos, pi




def Spirograph(parameters, vars):
	w = parameters["Width"]
	h = parameters["Height"]
	r = parameters["Radius"]
	#renderType = vars["RenderType"].get()
	t = vars["Time"].get()
	shift = math.pi * vars["Shift"].get()
	M = vars["M"].get()
	K = vars["K"].get()
	K1 = vars["K1"].get()
	K2 = vars["K2"].get()
	pim = Image.new('RGBA', (w, h), (0, 0, 64, 255))
	drw = aggdraw.Draw(pim)
	drw.setantialias(True)
	Z = (2*math.pi*i/M for i in range(0, int(M)))
	lines = ([FF(z, t, K, K1, K2), FF(z + shift, t, K, K1, K2)] for z in Z)
	lines = ([Fit(w,h,r,li[0]), Fit(w,h,r,li[1])] for li in lines)

	a = math.exp(0.6*math.log(100/M))
	alpha = int(a*255)
	thickness= 1.0*a + 0.7
	pen = aggdraw.Pen("blue", thickness, alpha)
	for li in lines:
		drw.line((li[0][0], li[0][1], li[1][0], li[1][1]), pen)
	
	drw.flush()
	return pim

def Fit(w, h, r, xy):
	return (w/2 + r*xy[0], h/2 + r*xy[1])	

def FF(z, t, k = 3, k1 = -5, k2 = 17):
	l =  0.5
	a =  0.4*sin(2*pi*t)
	b =  0.4*cos(2*pi*t)
	u = 0.4*cos(k*z) + a*cos(k1*z+2*pi*t) + b*cos(k2*z-2*pi*t) 
	v = 0.4*sin(k*z) + a*sin(k1*z+2*pi*t) + b*sin(k2*z-2*pi*t) 
	return (u,v)

