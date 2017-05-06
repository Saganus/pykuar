#!/usr/bin/python3
import argparse
import hashids
import time
import string
import pyqrcode
import base64

# Random UUID
hashids = hashids.Hashids(salt='7b3a2738-b33d-4c1e-89aa-d6fb9dd40fdd')

def parse_args():
	parser = argparse.ArgumentParser(description='PyKuar: A tool to generate a series of QR codes from aribrary-length text')
	parser.set_defaults(default=lambda x: parser.print_help())

	parser.add_argument('-o', '--output-file', nargs=1, help='Specifies the name and path of the output file. Default is \'./qr_<hashid>.<png/svg>')
	parser.add_argument('-t', '--type', default='png', help='Specifies the type of the output file. Valid options are \'png\' or \'svg\'. Default is \'png\'')
	parser.add_argument('-i', '--input-file', help='Specifies a text file to get the string from')
	parser.add_argument('-c', '--error-correction', nargs=1, default='H', choices=['L', 'H'], help='Specifies the error correction level. Valid options are \'L\' or \'H\'. Default is \'H\'')
	parser.add_argument('-v', '--qr-code-version', nargs=1, default='20', choices=['20', '40'], help='Specifies the QR code version to use. Valid options are  \'20\', \'40\'. Default is \'40\'')
	

	return parser.parse_args();

def main():

	args = parse_args()

	if args.input_file != None:
		with open(args.input_file, 'r') as file:
			plaintext = file.read()
	else:
		plaintext = input('Enter text to encode: ').strip()

	max_bytes = 0

	if args.error_correction[0] == 'L' and  args.qr_code_version[0] == '40':
		max_bytes = 2953
	elif args.error_correction[0] == 'H' and  args.qr_code_version[0] == '40':
		max_bytes = 1273
	elif args.error_correction[0] == 'L' and  args.qr_code_version[0] == '20':
		max_bytes = 858
	elif args.error_correction[0] == 'H' and  args.qr_code_version[0] == '20':
		max_bytes = 382

	num_codes = 1
	plaintext_bytes = base64.b64encode(plaintext.encode('utf-8'))

	if len(plaintext_bytes) > max_bytes:
		num_codes = len(plaintext_bytes) // max_bytes
		if len(plaintext_bytes) % max_bytes > 0:
			num_codes += 1

	print('Generating {} QR codes from an input text of {} bytes (base64 encoded)'.format(num_codes, len(plaintext_bytes)))

	for code in range(num_codes):
	
		offset = code * max_bytes
		if offset + max_bytes > len(plaintext_bytes):
			end = len(plaintext_bytes)
		else:
			end = offset + max_bytes
		 
		print('Generating code {}: From byte {} to {}'.format(code, offset, end))
		#print(plaintext_bytes[offset:end].decode())
		data = plaintext_bytes[offset:end]
		qr_code = pyqrcode.create(data, error=args.error_correction[0], version=int(args.qr_code_version[0]), mode='binary')

	
		if code < 1:
			timestamp = int(time.time())
			id = hashids.encode(timestamp)

		if args.output_file != None:
			output_file = args.output_file[0]
		else:
			output_file = 'qr_' + id + '.' + args.type

		if num_codes > 1 :
			output_file += '-' + str(code)

		if args.type == 'svg':
			qr_code.svg(output_file, scale=4, module_color='#000000', background='#ffffff')
			
		elif args.type == 'png':
			qr_code.png(output_file, scale=4, module_color=(0, 0, 0, 128), background=(0xff, 0xff, 0xff))

		print('Generated: ', output_file)
if __name__ == '__main__':
	main()