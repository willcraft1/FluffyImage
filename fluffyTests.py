#!/usr/bin/python3.4

from PIL import Image, ImageMath
from fluffyStego import *

def test():
	sourceIMG = Image.open("./large.jpg")
	toHide = Image.open("./hide.bmp")
	fileName = "filename"
	key	= "SECRETKEYSARESECRET"
	msg	= "Hello World"
	
	stegoIMG, name = hideIMG(sourceIMG, toHide, fileName, fileName, key, msg)
	
	stegoIMG.save(r"./TESTstego.bmp")
	
	stegoIMG = Image.open("./TESTstego.bmp")
	
	foundIMG, nameX, msgX = findImg(stegoIMG, key)
	
	foundIMG.save(r"./TESTfound.bmp")
	
	#do comparison stuff
	

test()
