import httpx

class Api:
    def __init__(self) -> None:
        self.mojang_profile= "https://api.mojang.com/users/profiles/minecraft/%s"
        self.mojang_session = "https://sessionserver.mojang.com/session/minecraft/profile/%s"
        self.hypixel_key = "https://api.hypixel.net/key?key=%s"
        self.hypixel_player = "https://api.hypixel.net/player?key=%s&uuid=%s"
        self.hypixel_status = "https://api.hypixel.net/status?key=%s&uuid=%s"
        self.hypixel_guild_player = "https://api.hypixel.net/guild?key=%s&player=%s"
        self.hypixel_guild_name = "https://api.hypixel.net/guild?key=%s&name=%s"
        self.hypixel_friends = "https://api.hypixel.net/friends?key=%s&uuid=%s"
        self.hypixel_recentgames = "https://api.hypixel.net/recentgames?key=%s&uuid=%s"
        self.hypixel_punishmentstats = "https://api.hypixel.net/punishmentstats?key=%s"
        self.hypixel_counts = "https://api.hypixel.net/counts?key=%s"
        self.antisniper_denick = "https://api.antisniper.net/denick?key=%s&nick=%s"
        self.antisniper_findnick = "https://api.antisniper.net/findnick?key=%s&name=%s"
        self.antisniper_winstreak = "https://api.antisniper.net/winstreak?key=%s&name=%s"
        self.optifine_cape = "http://s.optifine.net/capes/%s.png"
        self.optifine_banner = "http://optifine.net/showBanner?format=%s&valign=%s"
        self.optifine_format = "https://optifine.net/banners&&%s"


    async def get_latest_version_data(self):
        for _ in range(3):
            try:
                async with httpx.AsyncClient() as client:
                    res = await client.get(self.mojang_profile + player, timeout=10)
                    if res.status_code == 200:
                        return res.json()
                    if res.status_code == 400:
                        return NameError("不存在此玩家数据或丢失")
                    if res.status_code == 403:
                        return KeyError("少密钥或此密钥无效")
                    if res.status_code == 429:
                        return TimeoutError("超出API请求次数限制")
            except Exception as error:
                return error
        return {}
    
api = Api()