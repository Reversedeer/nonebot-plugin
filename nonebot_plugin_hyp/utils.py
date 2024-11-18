import nonebot

from pathlib import Path

class Utils:

    def __init__(self) -> None:
        self.usage = """"""
        driver = nonebot.get_driver()
        self.hypixel_apikey: int = getattr(driver, "hypixel_apikey", 114514)
        self.antisniper_apikey: int = getattr(driver, "antisniper_apikey", 114514)




utils = Utils()