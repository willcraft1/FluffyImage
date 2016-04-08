#!/usr/bin/python

from PIL import Image, ImageMath
from fluffyStego import *
from fluffyImage import *

def test():
	sourceIMG = Image.open("./source.jpg")
	hideIMG = Image.open("./hide.jpg")
	passphrase = "test"
	
	stegoIMG = hideImg(sourceIMG, hideIMG, passphrase)
	
	stegoIMG.save(r"./stego.bmp")
	
	stegoIMG = Image.open("./stego.bmp")
	
	foundIMG = findImg(stegoIMG, passphrase)
	
	foundIMG.save(r"./found.bmp)
	
	#do comparison stuff
	

main():
	test()
