import qrcode
import qrcode.image.svg
from qrcode.image.pure import PymagingImage

white_bg_factory 		= qrcode.image.svg.SvgPathFillImage
transparent_bg_factory 	= qrcode.image.svg.SvgPathImage

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data('Some data')
qr.make(fit=True)

img = qr.make_image(image_factory = PymagingImage)
img_file = open('qr.png', 'wb')
img.save(img_file)
