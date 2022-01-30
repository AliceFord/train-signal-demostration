from math import sin, cos, degrees, radians, sqrt

from Signal import Signal, SignalType, SignalSetting
from PIL import Image, ImageDraw, ImageFont
import numpy as np


HEIGHT = 600
RED = "red"
GREEN = (95, 232, 77)
YELLOW = "yellow"
BLACK = "black"
WHITE = "white"
font = ImageFont.truetype("C:/WINDOWS/FONTS/COUR.ttf", 30)


def drawNotImplemented(d, i, j):
	d.text((i + 60, j + 300), "No Signal", fill=BLACK, font=font)


def rotatePoint(x, y, theta, oX, oY):
	# s = sin(radians(theta))
	# c = cos(radians(theta))
	# oX -= x
	# oY -= y
	# xNew = oX * c - oY * s
	# yNew = oX * s - oY * c
	#
	# oX = xNew + x
	# oY = yNew + y
	# return oX, oY
	return cos(radians(theta)) * (x-oX) - sin(radians(theta)) * (y-oY) + oX, sin(radians(theta)) * (x-oX) + cos(radians(theta)) * (y-oY) + oY


def drawStopSemaphore(d, i, j, rotate=False):
	if rotate:
		rot = lambda x, y: rotatePoint(x, y, -45, i + 180, j + 240)
	else:
		rot = lambda x, y: (x, y)

	d.polygon([rot(i + 30, j + 210), rot(i + 180, j + 210), rot(i + 180, j + 270), rot(i + 30, j + 270)], fill=RED, outline=BLACK)  # Draw red signal base
	d.polygon([rot(i + 60, j + 210), rot(i + 90, j + 210), rot(i + 90, j + 270), rot(i + 60, j + 270)], fill=WHITE, outline=BLACK)  # Draw white stripe


def drawCautionSemaphore(d, i, j, rotate=False):
	if rotate:
		rot = lambda x, y: rotatePoint(x, y, -45, i + 180, j + 435)
	else:
		rot = lambda x, y: (x, y)

	d.polygon([rot(i + 30, j + 405), rot(i + 60, j + 435), rot(i + 30, j + 465), rot(i + 180, j + 465), rot(i + 180, j + 405)], fill=YELLOW, outline=BLACK)  # Yellow base
	d.polygon([rot(i + 60, j + 405), rot(i + 90, j + 435), rot(i + 60, j + 465), rot(i + 90, j + 465), rot(i + 120, j + 435), rot(i + 90, j + 405)], fill=BLACK, outline=BLACK)  # Yellow stripe


def drawSignals(signals):
	img = Image.new("RGB", (4 * (HEIGHT // 2), (len(signals) // 4) * HEIGHT + 60), color=(255, 255, 255))

	d = ImageDraw.Draw(img)

	signalSettings = [SignalSetting.PROCEED, SignalSetting.PRE_CAUTION, SignalSetting.CAUTION, SignalSetting.DANGER]
	for i in range(0, HEIGHT * 2, HEIGHT // 2):
		d.text((i + 30, 20), SignalSetting(signalSettings[i // (HEIGHT // 2)]).name, fill=BLACK, font=font)

	for index, signal in enumerate(signals):
		i = (index % 4) * (HEIGHT // 2)
		j = (index // 4) * HEIGHT + 60
		d.text((i + 30, j + 30), SignalType(signal.signalType).name, fill=BLACK, font=font)

		d.line([(i, j), (i, HEIGHT + j)], fill="purple")
		d.line([(i, j), (i + HEIGHT, j)], fill="purple")

		if signal.signalType == SignalType.UK_RAIL:
			d.rectangle([(i + 105, j + 285), (i + 195, j + 555)], fill=BLACK, outline=BLACK)
			if signal.signalSetting == SignalSetting.PROCEED:
				d.ellipse([(i + 120, j + 360), (i + 180, j + 420)], fill=GREEN, outline=GREEN)
			elif signal.signalSetting == SignalSetting.PRE_CAUTION:
				d.ellipse([(i + 120, j + 300), (i + 180, j + 360)], fill=YELLOW, outline=YELLOW)
				d.ellipse([(i + 120, j + 420), (i + 180, j + 480)], fill=YELLOW, outline=YELLOW)
			elif signal.signalSetting == SignalSetting.CAUTION:
				d.ellipse([(i + 120, j + 420), (i + 180, j + 480)], fill=YELLOW, outline=YELLOW)
			elif signal.signalSetting == SignalSetting.DANGER:
				d.ellipse([(i + 120, j + 480), (i + 180, j + 540)], fill=RED, outline=RED)

		if signal.signalType == SignalType.UK_SEMAPHORE:
			if signal.signalSetting == SignalSetting.PRE_CAUTION:
				drawNotImplemented(d, i, j)
				continue

			d.rectangle([(i + 180, j + 180), (i + 210, j + 540)], fill=WHITE, outline=BLACK)
			if signal.signalSetting == SignalSetting.DANGER:
				drawStopSemaphore(d, i, j)
				drawCautionSemaphore(d, i, j)
			elif signal.signalSetting == SignalSetting.CAUTION:
				drawStopSemaphore(d, i, j, True)
				drawCautionSemaphore(d, i, j)
			elif signal.signalSetting == SignalSetting.PROCEED:
				drawStopSemaphore(d, i, j, True)
				drawCautionSemaphore(d, i, j, True)

		if signal.signalType == SignalType.UK_LU:
			if signal.signalSetting == SignalSetting.PRE_CAUTION:
				drawNotImplemented(d, i, j)
				continue

			d.rectangle([(i + 105, j + 285), (i + 195, j + 555)], fill=BLACK, outline=BLACK)
			if signal.signalSetting == SignalSetting.PROCEED:
				d.ellipse([(i + 120, j + 300), (i + 180, j + 360)], fill=GREEN, outline=GREEN)
				d.ellipse([(i + 120, j + 420), (i + 180, j + 480)], fill=GREEN, outline=GREEN)
			elif signal.signalSetting == SignalSetting.CAUTION:
				d.ellipse([(i + 120, j + 300), (i + 180, j + 360)], fill=GREEN, outline=GREEN)
				d.ellipse([(i + 120, j + 480), (i + 180, j + 540)], fill=YELLOW, outline=YELLOW)
			elif signal.signalSetting == SignalSetting.DANGER:
				d.ellipse([(i + 120, j + 360), (i + 180, j + 420)], fill=RED, outline=RED)

	img.save("output.png")


if __name__ == '__main__':
	outsideSignals = []
	for item in [SignalType.UK_RAIL, SignalType.UK_SEMAPHORE, SignalType.UK_LU, SignalType.DE_SEMAPHORE]:
		outsideSignals.append(Signal(item, SignalSetting.PROCEED))
		outsideSignals.append(Signal(item, SignalSetting.PRE_CAUTION))
		outsideSignals.append(Signal(item, SignalSetting.CAUTION))
		outsideSignals.append(Signal(item, SignalSetting.DANGER))
	drawSignals(outsideSignals)
