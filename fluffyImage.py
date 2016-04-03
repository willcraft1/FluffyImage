#!/usr/bin/python

import argparse
from PIL import Image
from fluffyStego import *
#import ./fluffyCrypto.py 

def getArgs():
	prs = argparse.ArgumentParser(prog="fluffyImage")
	prs.add_argument("-s", "--sourcePath", metavar="source_image_path", required=True, help="\"source\" image will have the covert image hidden in it or removed from it.")
	prs.add_argument("-c", "--covertPath", metavar="covert_image_path", default=None, help="If supplied, this image will be hidden in the source image.")
	prs.add_argument("-p", "--passphrase", required=True, help="Passphrase for encrypting the or decrypting the covert image.")
	#	prs.add_argument("-e", "--cryptoType", choices=["SHA256", "SOMETHING_ELSE", "AES_ETC"]), \
	#				help="Select the cipher to be used.")
	#	prs.add_argument("-privK", 
	#	prs.add_argument("-pubK", 
	return prs.parse_args()

def main(args):
	sourceIMG 	= Image.open(args.sourcePath)
	passphrase 	= args.passphrase
	#cryptoType 	= args.cryptoType
	#PGP_PrivKey 	= args.PGP_PrivKey
	#PGP_PubKey	= args.PGP_PubKey

	if args.covertPath is not None:
		covertIMG = Image.open(args.covertPath)
		if checkSizeOK(sourceIMG, covertIMG) is True:
			print("Hiding covert image...")
			stegoIMG = hideIMG(sourceIMG, covertIMG, passphrase)
			stegoIMG.save(r"./not_stego.bmp")
			return
		else:
			print("The image to hide in the source image is too large. It must be 1/8th the size.")			
	else:
		print("Finding hidden image...")
		covertIMG = findImg(sourceIMG, passphrase)
		covertIMG.save(r"./found.bmp")		
		return
	print("Something went wrong. :D")
	return

main(getArgs())
