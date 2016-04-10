#!/usr/bin/python3.4

import argparse
from PIL import Image
from fluffyStego import *

def getArgs():
	prs = argparse.ArgumentParser(prog="fluffyImage")
	prs.add_argument("-s", "--sourcePath", metavar="source_image_path", required=True, help="\"source\" image will have the covert image hidden in it or removed from it.")
	prs.add_argument("-c", "--covertPath", metavar="covert_image_path", default=None, help="If supplied, this image will be hidden in the source image.")
	return prs.parse_args()

def main(args):
	sourceIMG 	= Image.open(args.sourcePath)

	if args.covertPath is not None:
		covertIMG = Image.open(args.covertPath)
		if checkSizeOK(sourceIMG, covertIMG) is True:
			print("Hiding covert image...")
			stegoIMG = hideIMG(sourceIMG, covertIMG, args.covertPath, args.sourcePath)
			img, name = stegoIMG
			img.save(name)
			return
		else:
			print("The image to hide in the source image is too large. It must be 1/8th the size.")			
	else:
		print("Finding hidden image...")
		covertIMG = findImg(sourceIMG)
		img, name = covertIMG
		img.save(name)		
		return
	print("Something went wrong. :D")
	return

main(getArgs())
