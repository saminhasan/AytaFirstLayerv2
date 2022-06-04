import board
import digitalio
from time import time, sleep
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
"""
	TODO : calculate font size from number of lines -> declare self.display_data usng loops -> add loops in show_data()
"""
class OLED:
	def __init__(self):
		self.oled_reset = digitalio.DigitalInOut(board.D4)

		# Display Parameters
		self.WIDTH = 128
		self.HEIGHT = 64
		self.i2c = board.I2C()
		self.oled = adafruit_ssd1306.SSD1306_I2C(self.WIDTH, self.HEIGHT, self.i2c, addr=0x3C, reset=self.oled_reset)
		self.clear_oled()
		# Create blank image for drawing.
		# Make sure to create image with mode '1' for 1-bit color.
		self.image = Image.new("1", (self.oled.width, self.oled.height))
		# Get drawing object to draw on image.
		self.draw = ImageDraw.Draw(self.image)
		# Draw a white background
		self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=255, fill=255)
		self.font_size = 16
		self.font_name = 'PixelOperator.ttf'
		self.font = ImageFont.truetype(self.font_name, self.font_size)
		self.display_data = {'1': 'Line1', '2': 'Line2', '3': 'Line3', '4': 'Line4'}

	def show_data(self):
		self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
		self.draw.text((0, 0 * self.font_size), self.display_data['1'], font=self.font, fill=255)
		self.draw.text((0, 1 * self.font_size), self.display_data['2'], font=self.font, fill=255)
		self.draw.text((0, 2 * self.font_size), self.display_data['3'], font=self.font, fill=255)
		self.draw.text((0, 3 * self.font_size), self.display_data['4'], font=self.font, fill=255)
		self.oled.image(self.image)
		self.oled.show()

	def text_size(self, text):
		font_size=self.font_size
		font_name=self.font_name
		font = ImageFont.truetype(font_name, font_size)
		size = font.getsize(text)
		return size

	def clear_oled(self):
		self.oled.fill(0)
		self.oled.show()

if __name__ == '__main__':
	import sys
	oled = OLED()
	try:
		while True:
			data1 = str('012345678901234567')
			data2 = str('abcdefghijklmnopqr')
			data3 = str('ABCDEFGHIJKLMNOPQR')
			data4 = str('_||______________||_')
			oled.display_data = {'1': data1, '2': data2, '3': data3, '4': data4}
			oled.show_data()
			print(oled.display_data)
			print(oled.text_size(data1))
			print(oled.text_size(data2))
			print(oled.text_size(data3))
			print(oled.text_size(data4))
			sleep(1.0)
			break
	except KeyboardInterrupt:
		print("\nUser Interrupt")
		sys.exit(0)
	finally:
		oled.clear_oled()
		pass
