import nonebot


class Utils:
    def __init__(self) -> None:
        self.usage = """"""
        self.path = {"bw", "sw", "skb", "guild"}
        driver = nonebot.get_driver().config
        self.hypixel_apikey: int = getattr(driver, "hypixel_apikey", 114514)
        self.antisniper_apikey: int = getattr(driver, "antisniper_apikey", 114514)

    async def get_hypixel_bedwars_level(self, Exp: int):
        """起床等级算法"""
        if Exp < 500:
            level = "0✫"
            experience = str(Exp) + "/500"
        elif Exp >= 500 and Exp < 1500:
            level = "1✫"
            experience = str(Exp - 500) + "/1k"
        elif Exp >= 1500 and Exp < 3500:
            level = "2✫"
            experience = str(Exp - 1500) + "/2k"
        elif Exp >= 3500 and Exp < 7000:
            level = "3✫"
            experience = str(Exp - 3500) + "/3.5k"
        elif Exp >= 7000:
            if Exp < 487000:
                add_level = int((Exp - 7000) / 5000)
                level = str(4 + add_level) + "✫"
                experience = str(Exp - 7000 - add_level * 5000) + "/5k"
            if Exp >= 487000:
                surplus_experience = Exp - (int(Exp / 487000)) * 487000
                if surplus_experience < 500:
                    add_level = 0
                    experience = str(surplus_experience) + "/500"
                elif surplus_experience >= 500 and surplus_experience < 1500:
                    add_level = 1
                    experience = str(surplus_experience - 500) + "/1k"
                elif surplus_experience >= 1500 and surplus_experience < 3500:
                    add_level = 2
                    experience = str(surplus_experience - 1500) + "/2k"
                elif surplus_experience >= 3500 and surplus_experience < 7000:
                    add_level = 3
                    experience = str(surplus_experience - 3500) + "3.5k"
                elif surplus_experience >= 7000:
                    add_level = int((surplus_experience - 7000) / 5000)
                    experience = str(surplus_experience - 7000 - add_level * 5000)
                level = str((int(Exp / 487000)) * 100 + 4 + add_level) + "✫"
        bw_level = level
        bw_experience = experience
        return bw_experience, bw_level


utils = Utils()
