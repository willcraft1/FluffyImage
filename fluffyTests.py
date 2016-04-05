#!/usr/bin/python

from PIL import Image, ImageMath
from fluffyStego import *

def test():
	sourceIMG = Image.open("./source.bmp")
	hidingIMG = Image.open("./hide.bmp")
	passphrase = "test"
	
	stegoIMG = hideIMG(sourceIMG, hidingIMG, passphrase)
	
	stegoIMG.save(r"./stego.bmp")
	
	stegoIMG = Image.open("./stego.bmp")
	
	foundIMG = findIMG(stegoIMG, passphrase)
	
	foundIMG.save(r"./found.bmp")

	if checkStegoIMG() == "OK":
		print "Stego image has stored image correctly."
	else:
		print "Stego image does not have storage correct."

def checkStegoIMG():
	testResultMSG = "OK"
	
	stegoIMG = Image.open("./stego.bmp")
	hiddenIMG = Image.open("./hide.bmp")
	
	stegoPixels = list(stegoIMG.getdata())
	
	for p in stegoPixels:
		y = 1
				

	return testResultMSG
	
def main():
	test()

main()
