#!/usr/bin/python

<<<<<<< HEAD
import argparse
from PIL import image

def getArgs():
	prs = argparse.ArguementParser(prog="fluffyImage")
	prs.add_arguement("-s", "--sourcePath", help="\"source\" image will have the covert image hidden in it or removed from it.", metavar="source_image_path", required=True)
	prs.add_arguement("-c", "--covertPath", help="If supplied, this image will be hidden in the source image.", metavar="covert_image_path", default=None)
	prs.add_arguement("-p", "--passphrase", help="Passphrase for encrypting the or decrypting the covert image.", required=True)
#	prs.add_arguement("-e", "--cipherType", help="Select the cipher to be used.", choices=["SHA256", "SOMETHING_ELSE", "ETC"])
	return prs.parse_args()

def main(args):
	if args.covertPath != None:
		covertIMG = Image.open(args.covertPath)
	sourceIMG = Image.open(args.sourcePath)
	passphrase = args.passphrase
	#cipherType = args.cipherType

	print(sourceIMG.format, sourceIMG.size, sourceIMG.mode)
	return

main(getArgs())
=======
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

>>>>>>> 9d2c5b88b2ddc743122d1ebc318cf42f0173b52b
