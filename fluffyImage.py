#!/usr/bin/python

from PIL import Image, ImageMath

image=Image.open(r"./watermark.bmp")

rgb_image=image.convert("RGB")

tX, tY, bX, bY = image.getbbox()

out=Image.new("RGB", (bX,bY))

for x in range(0,int(bX)):
	for y in range(0,int(bY)):
		r, g, b = rgb_image.getpixel((x,y))
		r = int(bin(r|1) , 2)
		g = int(bin(g|1) , 2)
		b = int(bin(b|1) , 2)	
		out.putpixel((x,y),(r,g,b))

out.save(r"./merged.bmp")

