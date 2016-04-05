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
			if pixelIndex < len(rBitArray):
				if r%2==0: 
					if int(rBitArray[pixelIndex])==1:
						r+=1
				else:
					if int(rBitArray[pixelIndex])==0:
						r-=1

				if g%2==0: 
					if int(gBitArray[pixelIndex])==1:
						g+=1
				else:
					if int(gBitArray[pixelIndex])==0:
						g-=1

				if b%2==0: 
					if int(bBitArray[pixelIndex])==1:
						b+=1
				else:
					if int(bBitArray[pixelIndex])==0:
						b-=1

				stegoIMG.putpixel((x_loc,y_loc),(r,g,b))
				pixelIndex += 1				
			else:								
				stegoIMG.putpixel((x_loc,y_loc),(r,g,b))
	
	return stegoIMG 

def findIMG(rgbSource, passphrase):
	tX, tY, bX, bY 	= rgbSource.getbbox()

	rBitArray = ""
	gBitArray = ""
	bBitArray = ""

	covertPixels = list(rgbSource.getdata())
	
	index = 0
	for p in covertPixels:
		pR, pG, pB = p
		rBitArray += bin(pR)[-1:]
		gBitArray += bin(pG)[-1:]
		bBitArray += bin(pB)[-1:]

		if index < 128:
			print bin(pR), bin(pR)[-1:]
			index +=1

	print rBitArray[:128]
	#print gBitArray[:128]
	#print bBitArray[:128]

	#for x_loc in range(0,int(bX)):
		#for y_loc in range(0,int(bY)):
			#r, g, b = rgbSource.getpixel((x_loc,y_loc))
			#print str(bin(r)[-1:])
			#rBitArray += str(bin(r)[-1:])
			#gBitArray += str(bin(g)[-1:])
			#bBitArray += str(bin(b)[-1:])
													
	rCovert = re.findall('........', rBitArray)
	gCovert = re.findall('........', gBitArray)
	bCovert = re.findall('........', bBitArray)
	
	#print rCovert, gCovert, bCovert	
	#print rCovert[1], gCovert[1], bCovert[1]

	#foundIMG		= Image.new("RGB", (bX,bY))
	foundIMG		= Image.new("RGB", (128,128))

	pixelIndex = 0

	for x_loc in range(0,127):
		for y_loc in range(0,127):
		#if pixelIndex < len(rCovert):		
			rC = int(rCovert[pixelIndex], 2)
			gC = int(gCovert[pixelIndex], 2)
			bC = int(bCovert[pixelIndex], 2)

			#print rC, gC, bC

			foundIMG.putpixel((x_loc,y_loc),(rC,gC,bC))
			#print foundIMG.getpixel((x_loc,y_loc))
			#print rC
			#print x_loc,y_loc
			pixelIndex += 1
	
	return foundIMG


def checkSizeOK(sourceIMG, covertIMG):
	sourceW = sourceIMG.width
	sourceH = sourceIMG.height
	covertW = covertIMG.width
	covertH = covertIMG.height
	sourcePixelTotal = int(sourceW) * int(sourceH)
	covertPixelTotal = int(covertW) * int(covertH)

	if sourcePixelTotal/8 >= covertPixelTotal+10:
		return True 
	else:
		return False
