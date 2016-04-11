#!/usr/bin/python3.4
#requires "python3" "redhat-rpm-confirm" packages and "pip3" module "pycryptodome"

import argparse
from PIL import Image
from fluffyStego import *

def getArgs():
	prs = argparse.ArgumentParser(prog="fluffyImage")
	prs.add_argument("-s", "--sourcePath", metavar="source_image_path", required=True, help="\"source\" image will have the covert image hidden in it or removed from it.")
	prs.add_argument("-c", "--covertPath", metavar="covert_image_path", default=None, help="If supplied, this image will be hidden in the source image.")
	prs.add_argument("-k", "--key", metavar="crypto_key", default=None, help="If supplied, the key will be used to encrypt the hidden image and message.")
	prs.add_argument("-m", "--msg", metavar="secret_msg", default="NONE", help="Adds a secret text message to the hidden image.")
	return prs.parse_args()

def main(args):
	sourceIMG 	= Image.open(args.sourcePath)

	if args.covertPath is not None:
		covertIMG = Image.open(args.covertPath)
		if checkSizeOK(sourceIMG, covertIMG) is True:
			print("Hiding covert image...")
			stegoIMG = hideIMG(sourceIMG, covertIMG, args.covertPath, args.sourcePath, args.key, args.msg)
			img, name = stegoIMG
			img.save(name)
			print("Saved stego'd image as: "+name)
			return
		else:
			print("The image to hide in the source image is too large. It must be less than 1/8th the size.")
			return		
	else:
		print("Finding hidden image...")
		covertIMG = findImg(sourceIMG, args.key)
		img, name, msg = covertIMG
		img.save(name)
		print("Saved extracted image as: "+name)
		print("The secret message is: "+msg)	
		return
	print("Something went wrong. :D")
	return

main(getArgs())
