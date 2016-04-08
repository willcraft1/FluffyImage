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
		rBitArray += str(bin(pR)[+2:]).zfill(8)
		gBitArray += str(bin(pG)[+2:]).zfill(8)
		bBitArray +=str(bin(pB)[+2:]).zfill(8)
	print rBitArray

	tX, tY, bX, bY 	= rgbSource.getbbox()

	#copy source/carrier image so you don't have to recreate unaltered pixels
	stegoIMG = rgbSource
	
	#increase/decrease by 1 bit to encode the value
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
				break				
	
	return stegoIMG 

def findImg(rgbSource, passphrase):
	tX, tY, bX, bY 	= rgbSource.getbbox()

	rBitArray = ""
	gBitArray = ""
	bBitArray = ""

	#retrieve and assemble last bit of each pixel
	for x_loc in range(0,bX):
		for y_loc in range(0,bY):
			r, g, b = rgbSource.getpixel((x_loc,y_loc))
			rBitArray += (bin(r)[2:].zfill(8)[-1:])
			gBitArray += (bin(g)[2:].zfill(8)[-1:])
			bBitArray += (bin(b)[2:].zfill(8)[-1:])
	
	#combine 8 bits into one value										
	rCovert = re.findall('........', rBitArray)
	gCovert = re.findall('........', gBitArray)
	bCovert = re.findall('........', bBitArray)
	
	print rCovert[:128]

	#build new base image
	foundIMG		= Image.new("RGB", (512,512))
	
	#grab each colour value from the Covert Arrays and assign to new image
	#note x_loc and y_loc are reversed as you assemble in the oposite direction as decompile
	pixelIndex = 0
	for y_loc in range(0,512):
		for x_loc in range(0,512):
			if pixelIndex < len(rCovert):		
				rC = int(rCovert[pixelIndex], 2)
				gC = int(gCovert[pixelIndex], 2)
				bC = int(bCovert[pixelIndex], 2)

				foundIMG.putpixel((x_loc,y_loc),(rC,gC,bC))
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
		return True
