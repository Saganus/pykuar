#!/usr/bin/python3
import argparse
import hashids

import time

import qrcode
import qrcode.image.svg
from qrcode.image.pure import PymagingImage

white_bg_factory 		= qrcode.image.svg.SvgPathFillImage
transparent_bg_factory 	= qrcode.image.svg.SvgPathImage

# Random UUID
hashids = hashids.Hashids(salt='7b3a2738-b33d-4c1e-89aa-d6fb9dd40fdd')

def parse_args():
	parser = argparse.ArgumentParser(description='PyKuar: A tool to generate a series of QR codes from aribrary-length text')
	parser.set_defaults(default=lambda x: parser.print_help())

	parser.add_argument('-o', '--output-file', nargs=1, help='Specifies the name and path of the output file. Default is \'./qr_<hashid>.<png/svg>')
	parser.add_argument('-t', '--type', default='png', help='Specifies the type of the output file. Valid options are \'png\' or \'svg\'. Default is \'png\'')
	parser.add_argument('-i', '--input-file', help='Specifies a text file to get the string from')
	
	return parser.parse_args();

def main():

	args = parse_args()

	qr = qrcode.QRCode(
	    version=None,
	    error_correction=qrcode.constants.ERROR_CORRECT_H,
	    box_size=10,
	    border=4,
	)
	
	if args.input_file != None:
		with open(args.input_file, 'r') as file:
			plaintext = file.read()
	else:
		plaintext = input('Enter text to encode').strip()

	qr.add_data(plaintext)
	qr.make(fit=True)
	#qr.make()

	if args.type == 'svg':
		qr_image = qr.make_image(image_factory = white_bg_factory)
		
	else:
		qr_image = qr.make_image(image_factory = PymagingImage)


	timestamp = int(time.time())
	id = hashids.encode(timestamp)

	if args.output_file != None:
		output_file = args.output_file[0]
	else:
		output_file = 'qr_' + id + '.' + args.type

	img_file = open(output_file, 'wb')
	qr_image.save(img_file)
	img_file.close()

	print('Generated: ', output_file)

if __name__ == '__main__':
	main()