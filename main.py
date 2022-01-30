from Signal import Signal, SignalType, SignalSetting
from PIL import Image, ImageDraw, ImageFont
import numpy as np


HEIGHT = 600
RED = "red"
GREEN = (95, 232, 77)
YELLOW = "yellow"
BLACK = "black"
WHITE = "white"


def drawNotImplemented(d, i):
	d.text((i + 20, 100), "No Signal", fill=BLACK)


def drawSignals(signals):
	img = Image.new("RGB", (len(signals) * (HEIGHT // 2), HEIGHT), color=(255, 255, 255))

	d = ImageDraw.Draw(img)
	font = ImageFont.truetype("C:/WINDOWS/FONTS/COUR.ttf", 10)

	for index, signal in enumerate(signals):
		i = index * (HEIGHT // 2)
		d.text((i + 10, 10), SignalType(signal.signalType).name, fill=BLACK)
		d.text((i + 10, 30), SignalSetting(signal.signalSetting).name, fill=BLACK)

		d.line([(i, 0), (i, HEIGHT)], fill="purple")

		if signal.signalType == SignalType.UK_RAIL:
			d.rectangle([(i + 35, 95), (i + 65, 185)], fill="black", outline="black")
			if signal.signalSetting == SignalSetting.PROCEED:
				d.ellipse([(i + 40, 120), (i + 60, 140)], fill=GREEN, outline=GREEN)
			elif signal.signalSetting == SignalSetting.PRE_CAUTION:
				d.ellipse([(i + 40, 100), (i + 60, 120)], fill=YELLOW, outline=YELLOW)
				d.ellipse([(i + 40, 140), (i + 60, 160)], fill=YELLOW, outline=YELLOW)
			elif signal.signalSetting == SignalSetting.CAUTION:
				d.ellipse([(i + 40, 140), (i + 60, 160)], fill=YELLOW, outline=YELLOW)
			elif signal.signalSetting == SignalSetting.DANGER:
				d.ellipse([(i + 40, 160), (i + 60, 180)], fill=RED, outline=RED)

		if signal.signalType == SignalType.UK_SEMAPHORE:
			if signal.signalSetting == SignalSetting.PRE_CAUTION:
				drawNotImplemented(d, i)
				continue

			d.rectangle([(i + 60, 60), (i + 70, 180)], fill=WHITE, outline=BLACK)
			if signal.signalSetting == SignalSetting.DANGER:
				# Red signal
				d.rectangle([(i + 10, 70), (i + 60, 90)], fill=RED, outline=BLACK)  # Draw red signal base
				d.rectangle([(i + 20, 70), (i + 30, 90)], fill=WHITE, outline=BLACK)  # Draw white stripe

				d.ellipse([(i + 70, 75), (i + 85, 90)], fill=RED, outline=BLACK)

				# Yellow signal
				d.polygon([(i + 10, 135), (i + 20, 145), (i + 10, 155), (i + 60, 155), (i + 60, 135)], fill=YELLOW, outline=BLACK)  # Yellow base
				d.polygon([(i + 20, 135), (i + 30, 145), (i + 20, 155), (i + 30, 155), (i + 40, 145), (i + 30, 135)], fill=BLACK, outline=BLACK)  # Yellow stripe

	img.save("output.png")


if __name__ == '__main__':
	outsideSignals = []
	for item in [SignalType.UK_RAIL, SignalType.UK_SEMAPHORE]:
		outsideSignals.append(Signal(item, SignalSetting.PROCEED))
		outsideSignals.append(Signal(item, SignalSetting.PRE_CAUTION))
		outsideSignals.append(Signal(item, SignalSetting.CAUTION))
		outsideSignals.append(Signal(item, SignalSetting.DANGER))
	drawSignals(outsideSignals)
