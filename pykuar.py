import argparse
import hashids

import time

import qrcode
import qrcode.image.svg
from qrcode.image.pure import PymagingImage

white_bg_factory 		= qrcode.image.svg.SvgPathFillImage
transparent_bg_factory 	= qrcode.image.svg.SvgPathImage


hashids = hashids.Hashids(salt='7b3a2738-b33d-4c1e-89aa-d6fb9dd40fdd')

def parse_args():
	parser = argparse.ArgumentParser(description='PyKuar: A tool to generate a series of QR codes from aribrary-length text')
	parser.set_defaults(default=lambda x: parser.print_help())

	parser.add_argument('-f', '--file', default='./', help='Specifies the name and path of the output file. Default is \'./qr_<hashid>.<png/svg>')
	parser.add_argument('-t', '--type', default='png', help='Specifies the type of the output file. Valid options are \'png\' or \'svg\'. Default is \'png\'')
	
	return parser.parse_args();

def main():
	# Random UUID
	

	args = parse_args()

	qr = qrcode.QRCode(
	    version=1,
	    error_correction=qrcode.constants.ERROR_CORRECT_L,
	    box_size=10,
	    border=4,
	)
	qr.add_data('Some data')
	qr.make(fit=True)

	if args.type == 'svg':
		qr_image = qr.make_image(image_factory = white_bg_factory)
		
	else:
		qr_image = qr.make_image(image_factory = PymagingImage)


	timestamp = int(time.time())
	print(str(timestamp))
	id = hashids.encode(timestamp)
	img_file = open('qr_' + id + '.' + args.type, 'wb')
	qr_image.save(img_file)
	img_file.close


if __name__ == '__main__':
	main()