#!/usr/bin/python

from PIL import Image, ImageMath
import re

#used to define header values, group seperator ~ group seperator
marker = "00011101011111100001110101111110"

def crypto(msg):
	data = ""
	counter = 0

	for c in msg:
		num = int(c)
		if counter < 5:
			if num==0:
				data += str(1)
				counter += 1
			else:
				data += str(0)
				counter += 1
		elif counter == 6:
			#reset
			data += str(c)
			counter = 0
		else:
			data += str(c)
			counter += 1
	return data


def hideIMG(sourceIMG, covertIMG, covertName, passphrase):
	rgbCovert	= covertIMG.convert("RGB")
	rgbSource	= sourceIMG.convert("RGB")
				
	rBitArray = ""
	
	#header = 512 bits each channel

	#collect covert image size
	h, w = covertIMG.size

	rBitArray += str(bin(h)[+2:]).zfill(8)
	rBitArray += marker
	rBitArray += str(bin(w)[+2:]).zfill(8)
	rBitArray += marker

	#convert name to binary and add to header
	name = map(bin, bytearray(covertName))
	for byte in name:
		rBitArray += str(byte[+2:]).zfill(8)
	rBitArray += marker

	#rBitArray += string_bin(covertName)
	#rBitArray += marker


	#header fill to 512 bits
	header = len(rBitArray)
	while header < 512:
		rBitArray += "0"
		header += 1

	print(rBitArray[:512])
	#add header to all channels to make them the same length
	gBitArray = rBitArray
	bBitArray = rBitArray

	covertPixels = list(rgbCovert.getdata())

	for p in covertPixels:
		pR, pG, pB = p
		rBitArray += str(bin(pR)[+2:]).zfill(8)
		gBitArray += str(bin(pG)[+2:]).zfill(8)
		bBitArray += str(bin(pB)[+2:]).zfill(8)

	rSplit = list(rBitArray)
	print(rBitArray[:16])
	print(rSplit[:16])
	gSplit = list(gBitArray)
	bSplit = list(bBitArray)
	rEncode = crypto (rSplit)
	gEncode = crypto (gSplit)
	bEncode = crypto (bSplit)
	print(rEncode[:16])

	#print(rEncode)
	#rEncode = encryptMessage (15, rBitArray)
	#gEncode = encryptMessage (15, gBitArray)
	#bEncode = encryptMessage (15, bBitArray)

	#print(rBitArray[:2048])
	#testIn = encryptMessage (15, rBitArray[:2048])
	#print(testIn)
	#testOut = decryptMessage (15, testIn)
	#print(testOut)

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
					if int(rEncode[pixelIndex])==1:
						r+=1
				else:
					if int(rEncode[pixelIndex])==0:
						r-=1

				if g%2==0: 
					if int(gEncode[pixelIndex])==1:
						g+=1
				else:
					if int(gEncode[pixelIndex])==0:
						g-=1

				if b%2==0: 
					if int(bEncode[pixelIndex])==1:
						b+=1
				else:
					if int(bEncode[pixelIndex])==0:
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

	#encryption process
	print "encrypted sample:"
	print rBitArray[:256]
	rSplit = list(rBitArray)
	gSplit = list(gBitArray)
	bSplit = list(bBitArray)
	rDecode = crypto (rSplit)
	gDecode = crypto (gSplit)
	bDecode = crypto (bSplit)
	print "decoded sample:"
	print rDecode[:256]
	
	header = rDecode[:512].split(marker)
	covertX = int(header[0], 2)
	covertY = int(header[1], 2)
	print "covert image size:", int(header[0], 2),"x", int(header[1], 2)

	nameBin = re.findall('........', header[2])
	name = ""	
	for char in nameBin:
		name += chr(int(char, 2))	
	print(name)

	#name = bin_string(header[2])
	#print(name)

	#covert string into bytes, adjust for 512 bit header in red channel
	rCovert = re.findall('........', rDecode[512:])
	gCovert = re.findall('........', gDecode[512:])
	bCovert = re.findall('........', bDecode[512:])

	#build new base image
	foundIMG		= Image.new("RGB", (covertX,covertY))
	
	#grab each colour value from the Covert Arrays and assign to new image
	#note x_loc and y_loc are reversed as you assemble in the oposite direction as decompile
	pixelIndex = 0
	for y_loc in range(0,covertY):
		for x_loc in range(0,covertX):
			if pixelIndex < len(rCovert):		
				rC = int(rCovert[pixelIndex], 2)
				gC = int(gCovert[pixelIndex], 2)
				bC = int(bCovert[pixelIndex], 2)

				foundIMG.putpixel((x_loc,y_loc),(rC,gC,bC))
				pixelIndex += 1
	return foundIMG, name


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
