#!/usr/bin/python

from PIL import Image, ImageMath

class fluffyStego:
	def hideIMG(sourceIMG, covertIMG, passphrase):
		rgbSource	= sourceIMG.convert("RGB")
		rgbCovert	= covertIMG.convert("RGB")

		tX, tY, bX, bY 	= rgbSource.getbbox()
		stegoImg	= Image.new("RGB", (bX,bY))

		for x_loc in range(0,int(bX)):
			for y_loc in range(0,int(bY)):
				r, g, b = rgb_image.getpixel((x_loc,y_loc))
				r = int(bin(r|1) , 2)
				g = int(bin(g|1) , 2)
				b = int(bin(b|1) , 2)	
				out.putpixel((x_loc,y_loc),(r,g,b))
		
		return stegoIMG 

	def findImg(sourceIMG, passphrase):


