#!/usr/bin/python
from __future__ import division
from PIL import Image, ImageMath
import re
from itertools import izip_longest

def hideIMG(sourceIMG, covertIMG, passphrase):
	rgbSource	= sourceIMG.convert("RGB")
	rgbCovert	= covertIMG.convert("RGB")

	soX, soY, smX, smY	= rgbSource.getbbox()
	sourcePixelCount 	= int(smX*smY)

	coX, coY, cmX, cmY	= rgbCovert.getbbox()
	covertBitTotal		= int(cmX*cmY*8)
	
	covertRpixVals = list(rgbCovert.getdata(0))
	covertGpixVals = list(rgbCovert.getdata(1))
	covertBpixVals = list(rgbCovert.getdata(2))

	rBitString = ""
	gBitString = ""
	bBitString = ""

	for val in covertRpixVals:
		rBitString += str(bin(val)[2:]).zfill(8)

	for val in covertGpixVals:
		gBitString += str(bin(val)[2:]).zfill(8)

	for val in covertBpixVals:
		bBitString += str(bin(val)[2:]).zfill(8)

	stegoIMG		= rgbSource
	covertBitIndex		= 0

	for stegoX in range(0,int(smX)):
		for stegoY in range(0,int(smY)):
			if covertBitIndex < covertBitTotal:
				r, g, b = stegoIMG.getpixel((stegoX,stegoY))
				
				rList = list(bin(r)[2:])
				gList = list(bin(g)[2:])
				bList = list(bin(b)[2:])
				
				rList[-1] = rBitString[covertBitIndex]
				gList[-1] = gBitString[covertBitIndex]			
				bList[-1] = bBitString[covertBitIndex]

				newRbin= ''.join(rList)
				newGbin= ''.join(gList)
				newBbin= ''.join(bList)

				newRval = int(newRbin, 2)
				newGval = int(newGbin, 2)
				newBval = int(newBbin, 2)

				stegoIMG.putpixel((stegoX,stegoY),(newRval,newGval,newBval))
				#print bin(r), bin(g), bin(b)
				covertBitIndex += 1
	return stegoIMG 

def findIMG(rgbStego, passphrase):
	covertMaxX = 512 #TODO:
	covertMaxY = 512 #pull this from image
	covertTotalPixels = covertMaxX*covertMaxY
	covertTotalBits = covertTotalPixels*8

	soX, soY, smX, smY	= rgbStego.getbbox()

	stegoRpixVals = list(rgbStego.getdata(0))
	stegoGpixVals = list(rgbStego.getdata(1))
	stegoBpixVals = list(rgbStego.getdata(2))

	rBitString = ""
	gBitString = ""
	bBitString = ""

	for covertBit in range (0, covertTotalBits):
		rBitString += str(bin(stegoRpixVals[covertBit])[-1:])

	for covertBit in range (0, covertTotalBits):	
		gBitString += str(bin(stegoGpixVals[covertBit])[-1:])

	for covertBit in range (0, covertTotalBits):
		bBitString += str(bin(stegoBpixVals[covertBit])[-1:])

	rPixelList = pixelizer(rBitString, 8)
	gPixelList = pixelizer(gBitString, 8)
	bPixelList = pixelizer(bBitString, 8)

	foundIMG = Image.new("RGB", (covertMaxX,covertMaxY))

	pixelsSaved = 0

	for found_x in range(0,covertMaxX):
		for found_y in range(0,covertMaxY):
			r = int(rPixelList.next(), 2)
			g = int(gPixelList.next(), 2)
			b = int(bPixelList.next(), 2)
			foundIMG.putpixel( (found_x,found_y) , (r,g,b) )
			pixelsSaved += 1
	return foundIMG

def pixelizer(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

def checkSizeOK(sourceIMG, covertIMG):
	sourceW = sourceIMG.width
	sourceH = sourceIMG.height
	covertW = covertIMG.width
	covertH = covertIMG.height
	sourcePixelTotal = int(sourceW) * int(sourceH)
	covertPixelTotal = int(covertW) * int(covertH)

	if sourcePixelTotal >= covertPixelTotal*8:
		return True 
	else:
		return False
