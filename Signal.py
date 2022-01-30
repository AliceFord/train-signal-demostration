import enum


class SignalType(enum.Enum):
	UK_RAIL = 1
	UK_SEMAPHORE = 2
	UK_LU = 3
	DE_SEMAPHORE = 4


class SignalSetting(enum.Enum):
	PROCEED = 1
	PRE_CAUTION = 2
	CAUTION = 3
	DANGER = 4


class Signal:
	signalType = None
	signalSetting = None

	def __init__(self, signalType, signalSetting=None):
		self.signalType = signalType
		self.signalSetting = signalSetting
