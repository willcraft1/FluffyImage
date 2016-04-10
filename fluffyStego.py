#!/usr/bin/python3.4

from PIL import Image, ImageMath
from fluffyCrypto import *
import re

#used to define header values, group seperator ~ group seperator
marker = "00011101011111100001110101111110"

def checkSizeOK(sourceIMG, covertIMG):
	sourceW = sourceIMG.width
	sourceH = sourceIMG.height
	covertW = covertIMG.width
	covertH = covertIMG.height
	sourcePixelTotal = int(sourceW) * int(sourceH)
	covertPixelTotal = int(covertW) * int(covertH)
	#TD_9-1 checkSize 8 pixels in source per 1 pixel in covert plus header
	print("sourceImage:",sourceW,"x",sourceH,"Total:",sourcePixelTotal,"Capacity:",sourcePixelTotal/8)
	print("covertImage:",covertW,"x",covertH,"Total:",covertPixelTotal,"With Header:",covertPixelTotal+512)


	if sourcePixelTotal/8 >= covertPixelTotal+512:
		return True 
	else:
		return False

def crypto(msg):
	data = ""
	counter = 0

	v1 = "00"
	v2 = "01"
	v3 = "10"
	v4 = "11"

	#encrypt logic
	'''
	00 becomes 10
	01 becomes 11
	10 becomes 01
	11 becomes 00
	'''

	for c in msg:
		num = int(c)
		if counter < 5:
			if num == 0:
				data += str(1)
				counter += 1
			else:
				data += str(0)
				counter += 1

		elif counter == 6:
			#reset counter
			data += str(c)
			counter = 0
		else:
			data += str(c)
			counter += 1
	return data

#test doc string translation (TD_2-1)
'''
def string_bin(string):
    return ''.join(format(ord(c), 'b') for c in string)

def bin_string(binary):
    bingen = (binary[i:i+7] for i in range(0, len(binary), 7))
    return ''.join(chr(eval('0b'+n)) for n in bingen)
'''

#------------------------------------------------------------------------
#---------------            Hide image         --------------------------
#------------------------------------------------------------------------

def hideIMG(sourceIMG, covertIMG, covertName, sourceName):
	rgbCovert	= covertIMG.convert("RGB")
	rgbSource	= sourceIMG.convert("RGB")
				
	rBitArray = ""
	
	#collect covert image size
	h, w = covertIMG.size
	#TD_1
	print("name:",covertName)
	print("size:",h, "x", w)

	rBitArray += str(bin(h)[+2:]).zfill(8)
	rBitArray += marker
	rBitArray += str(bin(w)[+2:]).zfill(8)
	rBitArray += marker

	#convert name to binary and add to header
	#TD_2-0 invalid in python 3.4
	'''
	name = map(bin, bytearray(covertName))
	for byte in name:
		rBitArray += str(byte[+2:]).zfill(8)
	rBitArray += marker
	'''
	
	#TD_2-1 certain characters fail translation
	'''
	print(covertName)
	name = string_bin(covertName)
	print(name)
	binaryName = bin_string(name)
	print(binaryName)
	'''

	name = bytearray(covertName[0:(len(covertName))], 'ascii')
	splitName = list(name)
	for c in splitName:
		rBitArray += str(bin(c)[+2:]).zfill(8)
	rBitArray += marker


	#header fill to 512 bits
	header = len(rBitArray)
	while header < 512:
		rBitArray += "0"
		header += 1
	#TD_3 compiled header
	print("header:",rBitArray[:512])


	#add header to all channels to make them the same length
	gBitArray = rBitArray
	bBitArray = rBitArray

	covertPixels = list(rgbCovert.getdata())

	#TD_8-1 red.bmp (250,1,2)					
	'''
	print(covertPixels)
	'''

	for p in covertPixels:
		pR, pG, pB = p
		rBitArray += str(bin(pR)[+2:]).zfill(8)
		gBitArray += str(bin(pG)[+2:]).zfill(8)
		bBitArray += str(bin(pB)[+2:]).zfill(8)


	#encoding
	rSplit = list(rBitArray)
	gSplit = list(gBitArray)
	bSplit = list(bBitArray)

	rEncode = crypto (rSplit)
	gEncode = crypto (gSplit)
	bEncode = crypto (bSplit)

	#TD_4 proof of changes
	print("sample source:",rBitArray[:16])
	print("sample split:", rSplit[:16])
	print("sample encoded:",rEncode[:16])
	
	#test doc - using transposition and using without python 3.4
	#TD_5-0
	'''
	rEncode = encryptMessage (24, rBitArray)
	gEncode = encryptMessage (24, gBitArray)
	bEncode = encryptMessage (24, bBitArray)
	'''

	#test doc - using smaller values work for transposition
	#TD_6-0	
	'''
	print(rBitArray[:2048])
	testIn = encryptMessage (15, rBitArray[:2048])
	'''
	#TD_6-1
	'''
	print(testIn)
	testOut = decryptMessage (15, testIn)
	'''
	#TD_6-2
	'''
	print(testOut)
	'''

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

	#remove the extension
	common = sourceName[:-4]
	name = "".join(("new_", common, ".bmp"))
	print("new file name:",name)

	return stegoIMG, name


#------------------------------------------------------------------------
#------------            Find hidden image        -----------------------
#------------------------------------------------------------------------

def findImg(rgbSource):
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

	#decryption process
	
	rSplit = list(rBitArray)
	gSplit = list(gBitArray)
	bSplit = list(bBitArray)
	rDecode = crypto (rSplit)
	gDecode = crypto (gSplit)
	bDecode = crypto (bSplit)
	
	#test doc, using transpostion
	'''
	rDecode = decryptMessage (24, rBitArray)
	gDecode = decryptMessage (24, gBitArray)
	bDecode = decryptMessage (24, bBitArray)
	'''

	#TD_7
	print("encrypted sample:")
	print(rBitArray[:512])
	print("decoded sample:")
	print(rDecode[:512])
	

	#get Header Information
	header = rDecode[:512].split(marker)
	covertX = int(header[0], 2)
	covertY = int(header[1], 2)
	print("covert image size:", int(header[0], 2),"x", int(header[1], 2))

	nameBin = re.findall('........', header[2])
	name = ""	
	for char in nameBin:
		name += chr(int(char, 2))	
	print("original name:",name)


	#covert string into bytes, adjust for 512 bit header in red channel
	rCovert = re.findall('........', rDecode[512:])
	gCovert = re.findall('........', gDecode[512:])
	bCovert = re.findall('........', bDecode[512:])
	
	#proof of cryptography working (hard code values for PoC)
	#PoC_1
	'''
	covertX = 448
	covertY = 448
	name = "crypto_POC.png"
	print("crypto name:",name)
	rCovert = re.findall('........', rBitArray)
	gCovert = re.findall('........', gBitArray)
	bCovert = re.findall('........', bBitArray)
	print("encrypted:",rBitArray[:512])
	'''

	#build new base image
	foundIMG		= Image.new("RGB", (covertX,covertY))
	
	#grab each colour value from the Covert Arrays and assign to new image
	#TD_8 x_loc and y_loc are reversed as you assemble in the oposite direction as decompile
	pixelIndex = 0
	for y_loc in range(0,covertY):
		for x_loc in range(0,covertX):
			if pixelIndex < len(rCovert):		
				rC = int(rCovert[pixelIndex], 2)
				gC = int(gCovert[pixelIndex], 2)
				bC = int(bCovert[pixelIndex], 2)

				foundIMG.putpixel((x_loc,y_loc),(rC,gC,bC))
				pixelIndex += 1
	nameEX = "".join(("extracted_", name))
	print("new name:",nameEX)	
	return foundIMG, nameEX

