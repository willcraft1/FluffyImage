#!/usr/bin/python

from PIL import Image
import sys

new_image_array = []
i = 0

def get_secret_array(secret_image, array):
	for x in range(0, secret_image.size[0]):
		for y in range(0, secret_image.size[1]):
			r, g, b = secret_image.getpixel((x,y))
			print "secret array"
			array.append(bin(r)[2:].zfill(8))
			print bin(r)[2:].zfill(8)
			array.append(bin(g)[2:].zfill(8))
			print bin(g)[2:].zfill(8)
			array.append(bin(b)[2:].zfill(8))
			print bin(b)[2:].zfill(8)



def encode_bit_value(carrier, encoding_bit):
	temp = carrier[:-1]
	temp = temp + str(encoding_bit)
	return temp

def make_one_string(secret):
	i = 0
	one_string = ""
	for i in range(0, len(secret)-1):
		one_string += str(secret[i])
		i += 1
	return one_string

def set_end_point_of_secret_string(secret_string):
	new_string = ""
	new_string += secret_string + "1111111111111111111110"
	return new_string

def get_secret_image_dimensions(secret_image):
	new_array = []
	width = int(secret_image.size[0])
	height = int(secret_image.size[1])
	new_array.append(width)
	new_array.append(height)
	return new_array

def get_index():
	return i

def set_index(newi):
	global i 
	i = newi

def next_secret_bit(secret_string, original):
	i = get_index()
	print "i"
	print i
	if i < len(secret_string):
		next_bit = secret_string[i]
		print "next_bit"
		print next_bit
		i = i + 1
		set_index(i)
		return next_bit

	else:
		return original[-1:]
	
def encode_rgb(r, g, b, secret_string):
	r2 = bin(r)[2:].zfill(8)
	g2 = bin(g)[2:].zfill(8)
	b2 = bin(b)[2:].zfill(8)
	
	print "r"
	print bin(r)
	newr = encode_bit_value(r2, next_secret_bit(secret_string, r2))
	print "newr"
	print newr

	print "g"
	print bin(g)
	newg = encode_bit_value(g2, next_secret_bit(secret_string, g2))
	print "newg"
	print newg

	print "b"
	print bin(b)
	newb = encode_bit_value(b2, next_secret_bit(secret_string, b2))
	print "newb"
	print newb
	print "================================================"
	
	return newr, newg, newb

def decode_rgb(rgb_image):
	secret_string = ""
	for x in range(0, rgb_image.size[0]):
		if secret_string[-22:] == '1111111111111111111110':
				print "breaking"
				break
		for y in range(0, rgb_image.size[1]):
			print "here" + secret_string[-22:]
			if secret_string[-22:] == '1111111111111111111110':
				break
			r, g, b = rgb_image.getpixel((x,y))
			print bin(r)[2:].zfill(8)[-1:]
			print bin(g)[2:].zfill(8)[-1:]
			print bin(b)[2:].zfill(8)[-1:]
			print "^^^^^^^^^^^^^^^^^^^^^^"
			secret_string += (bin(r)[2:].zfill(8)[-1:])
			secret_string += (bin(g)[2:].zfill(8)[-1:])
			secret_string += (bin(b)[2:].zfill(8)[-1:])
			print secret_string[-22:]
	return secret_string[:-22]

def encode(carrier_image_file, secret_image_file, output_file_name, key):
	secret_array = []
	one_string = ""
	test_array = []
	
	carrier_image = Image.open(carrier_image_file)
	secret_image = Image.open(secret_image_file)
	carrier_image_rgb = carrier_image.convert("RGB")
	secret_image_rgb = secret_image.convert("RGB")
	
	new_image_rgb = carrier_image_rgb
	
	
	get_secret_array(secret_image_rgb, secret_array)
	one_string = make_one_string(secret_array)
	test_array = get_secret_image_dimensions(secret_image_rgb)

	print test_array[0]
	print test_array[1]
	print one_string
	print len(secret_array)
	print "secret array index length ^"
	print secret_array[0][-1]
	for x in range(0, carrier_image_rgb.size[0]):
		for y in range(0, carrier_image_rgb.size[1]):
			i = get_index()
			if i < len(one_string):
				r, g, b = carrier_image_rgb.getpixel((x,y))
				r2, g2, b2 = encode_rgb(r, g, b, one_string)
				new_image_rgb.putpixel((x,y), (int(r2, 2), int(g2, 2), int(b2, 2)))
			else:
				break
	new_image_rgb.save(output_file_name)

def decode(encoded_image_file, key):
	encoded_image = Image.open(encoded_image_file)
	encoded_image_rgb = encoded_image.convert("RGB")
	secret_image_string = ""
	secret_image_string = decode_rgb(encoded_image_rgb)

	set_index(0)
	data = ""
	im = Image.new("RGB", (256, 256))
	print secret_image_string
	print len(secret_image_string)
	for x in range(0, im.size[0]):
		for y in range(0, im.size[1]):
			i = get_index()
			print i
			f = i
			i += 8
			r = secret_image_string[f:i]
			print r
			f = i
			i += 8
			g = secret_image_string[f:i]
			print g
			f = i
			i += 8
			b = secret_image_string[f:i]
			print b

			im.putpixel((x,y), (int(r, 2), int(g, 2), int(b, 2)))
			set_index(i)
	im.save("decoded.bmp")
	
def help():
	print "Proper usage:"
	print "%s decode <encoded_image> <key>" % sys.argv[0]
	print "%s encode <carrier_image> <hidden_image> <output_file_name> <key>" % sys.argv[0]
	

def main():
	if len(sys.argv) != 4 and len(sys.argv) != 6:
		help()
	elif sys.argv[1] == "decode":
		decode(sys.argv[2], sys.argv[3])
		print "Done decoding"
	elif sys.argv[1] == "encode":
		encode(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
		print "Done encoding"
	elif sys.argv[1] == "help":
		help()
	else:
		help()
	

main()

