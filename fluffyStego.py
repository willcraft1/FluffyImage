#!/usr/bin/python

from PIL import Image, ImageMath

class fluffyStego:
	def hideIMG(sourceIMG, covertIMG, passphrase):
		rgbCovert	= covertIMG.convert("RGB")
						
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
		rgbSource	= sourceIMG.convert("RGB")

		for x_loc in range(0,int(bX)):
			for y_loc in range(0,int(bY)):
				r, g, b = rgb_Source.getpixel((x_loc,y_loc))
				r = int(bin(r|int(rBitArray[pixelIndex])) , 2)
				g = int(bin(g|int(gBitArray[pixelIndex])) , 2)
				b = int(bin(b|int(bBitArray[pixelIndex])) , 2)					
														
				stegoIMG.putpixel((x_loc,y_loc),(r,g,b))

				pixelIndex+1
		
		return stegoIMG 

	def findImg(sourceIMG, passphrase):


