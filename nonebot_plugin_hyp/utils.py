import nonebot


class Utils:
	def __init__(self) -> None:
		self.usage = """"""
		self.path = {'bw', 'sw', 'skb', 'guild'}
		driver = nonebot.get_driver().config
		self.hypixel_apikey: int = getattr(
			driver, 'hypixel_apikey', 114514
		)
		self.antisniper_apikey: int = getattr(
			driver, 'antisniper_apikey', 114514
		)


utils = Utils()
