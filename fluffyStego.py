#!/usr/bin/python3.4

from PIL import Image, ImageMath
from fluffyCrypto import *
import re

#used to define header values, group seperator ~ 4 bytes
marker = "000000111111000000111111"

def checkSizeOK(sourceIMG, covertIMG):
	sourceW = sourceIMG.width
	sourceH = sourceIMG.height
	covertW = covertIMG.width
	covertH = covertIMG.height
	sourcePixelTotal = int(sourceW) * int(sourceH)
	covertPixelTotal = int(covertW) * int(covertH)
	#TD_9-1 checkSize 8 pixels in source per 1 pixel in covert plus header
	print("sourceImage:",sourceW,"x",sourceH,"Total:",sourcePixelTotal,"Capacity:",sourcePixelTotal/8)
	print("covertImage:",covertW,"x",covertH,"Total:",covertPixelTotal,"With Header:",covertPixelTotal+2048)


	if sourcePixelTotal/8 >= covertPixelTotal+2048:
		return True 
	else:
		return False

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

def hideIMG(sourceIMG, covertIMG, covertName, sourceName, key, covertmsg):
	rgbCovert	= covertIMG.convert("RGB")
	rgbSource	= sourceIMG.convert("RGB")
				
	rBitArray = ""
	
	#collect covert image size
	h, w = covertIMG.size
	#TD_1
	'''
	print("name:",covertName)
	print("size:",h, "x", w)
	'''
	
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
	
	msg = bytearray(covertmsg[0:(len(covertmsg))], 'ascii')
	splitmsg = list(msg)
	for m in splitmsg:
		rBitArray += str(bin(m)[+2:]).zfill(8)
	rBitArray += marker
	
	#header fill to 2048 bits
	header = len(rBitArray)
	while header < 2048:
		rBitArray += "0"
		header += 1
	#TD_3 compiled header
	print("Full header:",rBitArray[:2048])


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

	if key is not None:
		#encryption
		rSplit = list(rBitArray)
		gSplit = list(gBitArray)
		bSplit = list(bBitArray)
		rEncode = enCrypto(rSplit, key)
		gEncode = enCrypto(gSplit, key)
		bEncode = enCrypto(bSplit, key)
	else: 
		rEncode = rBitArray
		gEncode	= gBitArray
		bEncode = bBitArray

	#TD_4 proof of changes
	'''
	print("sample source:",rBitArray[:16])
	print("sample split:", rSplit[:16])
	print("sample encoded:",rEncode[:16])
	'''
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
	name = "".join((common, "_STEGO.bmp"))
	print("Stego image name: ",name)

	return stegoIMG, name


#------------------------------------------------------------------------
#------------            Find hidden image        -----------------------
#------------------------------------------------------------------------

def findImg(rgbSource, key):
	tX, tY, bX, bY 	= rgbSource.getbbox()

	rBitArray = ""
	gBitArray = ""
	bBitArray = ""
	msgEX = 	"NO MESSAGE FOUND"

	#retrieve and assemble last bit of each pixel
	for x_loc in range(0,bX):
		for y_loc in range(0,bY):
			r, g, b = rgbSource.getpixel((x_loc,y_loc))
			rBitArray += (bin(r)[2:].zfill(8)[-1:])
			gBitArray += (bin(g)[2:].zfill(8)[-1:])
			bBitArray += (bin(b)[2:].zfill(8)[-1:])
	
	
	if key is not None:
		#decryption process
		rSplit = list(rBitArray)
		gSplit = list(gBitArray)
		bSplit = list(bBitArray)
		rDecode = str(deCrypto(rSplit, key))
		gDecode = str(deCrypto(gSplit, key))
		bDecode = str(deCrypto(bSplit, key))
	else:
		rDecode = rBitArray
		gDecode = gBitArray
		bDecode = bBitArray
	'''
	
	rSplit = list(rBitArray)
	gSplit = list(gBitArray)
	bSplit = list(bBitArray)
	rDecode = crypto (rSplit)
	gDecode = crypto (gSplit)
	bDecode = crypto (bSplit)
	'''
	#test doc, using transpostion
	'''
	rDecode = decryptMessage (24, rBitArray)
	gDecode = decryptMessage (24, gBitArray)
	bDecode = decryptMessage (24, bBitArray)


	#TD_7
	print("encrypted sample:")
	print(rBitArray[:2048])
	print("decoded sample:")
	print(rDecode[:2048])
	'''

	#get Header Information
	header = rDecode[:2048].split(marker)
	covertX = int(header[0], 2)
	covertY = int(header[1], 2)
	print("covert image size:", int(header[0], 2),"x", int(header[1], 2))

	nameBin = re.findall('........', header[2])
	name = ""	
	for char in nameBin:
		name += chr(int(char, 2))	
	print("original name:",name)
	
	msgBin = re.findall('........', header[3])
	msgEX = ""	
	for m in msgBin:
		msgEX += chr(int(m, 2))

	#covert string into bytes, adjust for 2048 bit header in red channel
	rCovert = re.findall('........', rDecode[2048:])
	gCovert = re.findall('........', gDecode[2048:])
	bCovert = re.findall('........', bDecode[2048:])
	
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
	print("encrypted:",rBitArray[:2048])
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
	return foundIMG, nameEX, msgEX

