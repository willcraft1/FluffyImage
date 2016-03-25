#!/usr/bin/python

import argparse
from PIL import Image
import fluffyStego.py
#import ./fluffyCrypto.py 

def getArgs():
	prs = argparse.ArguementParser(prog="fluffyImage")
	prs.add_arguement("-s", "--sourcePath", metavar="source_image_path", required=True, \
				help="\"source\" image will have the covert image hidden in it or removed from it.")
	prs.add_arguement("-c", "--covertPath", metavar="covert_image_path", default=None, \
				help="If supplied, this image will be hidden in the source image.")
	prs.add_arguement("-p", "--passphrase", required=True, \
				help="Passphrase for encrypting the or decrypting the covert image.")
#	prs.add_arguement("-e", "--cryptoType", choices=["SHA256", "SOMETHING_ELSE", "AES_ETC"]), \
#				help="Select the cipher to be used.")
#	prs.add_arguement("-privK", 
#	prs.add_arguement("-pubK", 
	return prs.parse_args()

def main(args):
	sourceIMG 	= Image.open(args.sourcePath)
	passphrase 	= args.passphrase
	#cryptoType 	= args.cryptoType
	#PGP_PrivKey 	= args.PGP_PrivKey
	#PGP_PubKey	= args.PGP_PubKey

	if args.covertPath is not None:
		print("Hiding covert image...")
		covertIMG = Image.open(args.covertPath)
		stegoIMG = fluffyStego.hideIMG(sourceIMG, covertIMG, passphrase)
		stegoIMG.save(r"./not_stego.bmp")
		return
	else:
		print("Finding hidden image...")
		covertIMG = fluffyStego.findIMG(sourceIMG, passphrase)
		covertIMG.save(r"./found.bmp")		
		return

	print("Something went wrong. :D")
	return

main(getArgs())
