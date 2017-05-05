#!/usr/bin/python3
import argparse
import hashids

import time
import string

import qrcode
import qrcode.image.svg
from qrcode.image.pure import PymagingImage
from qrcode.exceptions import DataOverflowError

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
	parser.add_argument('-c', '--error-correction', nargs=1, default='H', choices=['l', 'L', 'h', 'H'], help='Specifies the error correction level. Valid options are \'L\' or \'H\'. Default is \'H\'')
	parser.add_argument('-v', '--qr-code-version', nargs=1, default='40', choices=['20', '40'], help='Specifies the QR code version to use. Valid options are  \'20\', \'40\'. Default is \'40\'')
	
	parsed_args = parser.parse_args();
	parsed_args.error_correction[0] = parsed_args.error_correction[0].lower()

	if parsed_args.qr_code_version == 'auto' or parsed_args.qr_code_version == 'AUTO':
		parsed_args.qr_code_version = None
	else:
		parsed_args.qr_code_version[0] = int(parsed_args.qr_code_version[0])


	return parsed_args

def main():

	args = parse_args()

	if args.error_correction[0] == 'l':
		correction_level = qrcode.constants.ERROR_CORRECT_L
	else:
		correction_level = qrcode.constants.ERROR_CORRECT_H

	qr = qrcode.QRCode(
	    version=args.qr_code_version[0],
	    error_correction=correction_level,
	    box_size=10,
	    border=4,
	)
	
	if args.input_file != None:
		with open(args.input_file, 'r') as file:
			plaintext = file.read()
	else:
		plaintext = input('Enter text to encode: ').strip()

	max_chars = 1110

	if args.error_correction[0] == 'l' and  args.qr_code_version[0] == 40:
		max_chars = 2960
	elif args.error_correction[0] == 'h' and  args.qr_code_version[0] == 40:
		max_chars = 1110
	elif args.error_correction[0] == 'l' and  args.qr_code_version[0] == 20:
		max_chars = 600

	num_codes = 1

	if len(plaintext) > max_chars:
		num_codes = len(plaintext) // max_chars
		if len(plaintext) % max_chars > 0:
			num_codes += 1

	print('Generating {} QR codes from an input text of {} chars'.format(num_codes, len(plaintext)))

	for code in range(num_codes):
		qr.clear()

		offset = code * max_chars
		if offset + max_chars > len(plaintext):
			end = len(plaintext)
		else:
			end = offset + max_chars
		 
		print('Generating code {}: From char {} to {}'.format(code, offset, end))
		qr.add_data(plaintext[offset:end])	
		qr.make(fit=False)
		#qr.make()
	
		if args.type == 'svg':
			qr_image = qr.make_image(image_factory = white_bg_factory)
			
		else:
			qr_image = qr.make_image(image_factory = PymagingImage)

		if num_codes > 1 and code < 1:
			timestamp = int(time.time())
			id = hashids.encode(timestamp)

		if args.output_file != None:
			output_file = args.output_file[0]
		else:
			output_file = 'qr_' + id + '.' + args.type

		if num_codes > 1 :
			output_file += '-' + str(code)

		img_file = open(output_file, 'wb')
		qr_image.save(img_file)
		img_file.close()

		print('Generated: ', output_file)
if __name__ == '__main__':
	main()