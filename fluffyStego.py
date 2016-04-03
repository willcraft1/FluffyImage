#!/usr/bin/python

from PIL import Image, ImageMath
import re

def hideIMG(sourceIMG, covertIMG, passphrase):
	rgbCovert	= covertIMG.convert("RGB")
	rgbSource	= sourceIMG.convert("RGB")
					
	rBitArray = ""
	gBitArray = ""
	bBitArray = ""
	
	covertPixels = list(rgbCovert.getdata())

	for p in covertPixels:
		pR, pG, pB = p	

		singleR = str(bin(pR)[+2:]).zfill(8)
		for x in singleR.split():
			rBitArray += x

		singleG = str(bin(pG)[+2:]).zfill(8)
		for x in singleG.split():
			gBitArray += x

		singleB = str(bin(pB)[+2:]).zfill(8)
		for x in singleB.split():
			bBitArray += x

	tX, tY, bX, bY 	= rgbSource.getbbox()
	stegoIMG		= Image.new("RGB", (bX,bY))
	pixelIndex 		= 0


	for x_loc in range(0,int(bX)):
		for y_loc in range(0,int(bY)):
			r, g, b = rgbSource.getpixel((x_loc,y_loc))
			r = int(bin(r|int(rBitArray[pixelIndex])) , 2)
			g = int(bin(g|int(gBitArray[pixelIndex])) , 2)
			b = int(bin(b|int(bBitArray[pixelIndex])) , 2)					
													
			stegoIMG.putpixel((x_loc,y_loc),(r,g,b))

			pixelIndex += 1
	
	return stegoIMG 

def findImg(rgbSource, passphrase):
	tX, tY, bX, bY 	= rgbSource.getbbox()

	rBitArray = ""
	gBitArray = ""
	bBitArray = ""

	foundIMG		= Image.new("RGB", (bX,bY))

	for x_loc in range(0,int(bX)):
		for y_loc in range(0,int(bY)):
			r, g, b = rgbSource.getpixel((x_loc,y_loc))
			rBitArray += str(bin(r)[+9:])
			gBitArray += str(bin(g)[+9:])
			bBitArray += str(bin(b)[+9:])	
															
	rCovert = re.findall('........', rBitArray)
	gCovert = re.findall('........', gBitArray)
	bCovert = re.findall('........', bBitArray)

	global pixelIndex

	while pixelIndex < len(rCovert):
		print pixelIndex
		for x_loc in range(0,int(bX)):
			for y_loc in range(0,int(bY)):		
				rC = int(rCovert[pixelIndex])
				gC = int(gCovert[pixelIndex])
				bC = int(bCovert[pixelIndex])

				foundIMG.putpixel((x_loc,y_loc),(rC,gC,bC))
				#print rC,gC,bC
				#print x_loc,y_loc
				pixelIndex += 1
	
	return foundIMG

def checkSizeOK(sourceIMG, covertIMG):
	sourcePixelTotal = sourceIMG.width() * sourceIMG.height()
	covertPixelTotal = sourceIMG.width() * sourceIMG.height()
	print sourcePixelTotal + covertPixelTotal

