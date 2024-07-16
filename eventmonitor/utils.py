
import nonebot

from pathlib import Path

class Utils:
    def __init__(self) -> None:
        self.usage = """
            指令1：戳一戳(戳一戳bot获取文案)
            指令2：群荣誉监测(检测群聊中龙王，群聊之火，快乐源泉的获得并发送提示，当 bot获得群荣誉时有特殊消息)
            指令3：群文件检测(检测所有人发送群文件并发送提示)
            指令4：群成员减少检测(当有人退群时，发送退群消息；当主人/superuser退群有特殊回复)
            指令5：群成员增加检测(当有人入群时，发送入群欢迎，当bot首次入群会乞讨管理，当主人/superuser入群会有特殊回复)
            指令6：管理员变动检测(当新增管理员或取消管理员时发送消息提示，当bot自身被上/下管理时有特殊回复)
            指令7：运气王检测(检测抢红包检测后的运气王并发送提示消息)"""
        self.notAllow = '功能未开启'
        self.path = {
            'chuo': ['戳一戳'],
            'honor': ['群荣誉检测'],
            'files': ['群文件检测'],
            'del_user': ['群成员减少检测'],
            'add_user': ['群成员增加检测'],
            'admin': ['管理员变动检测'],
            'red_package': ['运气王检测']
            }
        self.g_temp = {}
        self.chuo_CD_dir = {}
        self.config_path = Path() / 'data/eventmonitor'
        self.address = self.config_path / 'config.json'
        config = nonebot.get_driver().config
        self.superusers = {int(uid) for uid in config.superusers}
        self.nickname = next(iter(config.nickname))
        self.chuo_cd: int = getattr(config, "chuo_cd", 0)




    @staticmethod
    #检查戳一戳是否允许
    async def check_chuo(g_temp, gid: str) -> bool: 
        if gid in g_temp and not g_temp[gid]["chuo"]:
            return False
        return g_temp[gid]["chuo"]

    @staticmethod
    #检查群荣誉是否允许 
    async def check_honor(g_temp, gid: str) -> bool:
        if gid in g_temp and not g_temp[gid]["honor"]:
            print(g_temp)
            return False
        return g_temp[gid]["honor"]

    @staticmethod
    #检查群文件是否允许 
    async def check_file(g_temp, gid: str) -> bool:
        if gid in g_temp and not g_temp[gid]["files"]:
            return False
        return g_temp[gid]["files"]

    @staticmethod
    #检查群成员减少是否允许 
    async def check_del_user(g_temp, gid: str) -> bool:
        if gid in g_temp and not g_temp[gid]["del_user"]:
            return False
        print(g_temp)
        return g_temp[gid]["del_user"]

    @staticmethod
    #检查群成员增加是否允许
    async def check_add_user(g_temp, gid: str) -> bool:
        if gid in g_temp and not g_temp[gid]["add_user"]:
            return False
        print(g_temp)
        return g_temp[gid]["add_user"]
        
    @staticmethod
    #检查管理员是否允许
    async def check_admin(g_temp, gid: str) -> bool:
        if gid in g_temp and not g_temp[gid]["admin"]:
            return False
        return g_temp[gid]["admin"]

    @staticmethod
    #检查运气王是否允许
    async def check_red_package(g_temp, gid: str) -> bool:
        if gid in g_temp and not g_temp[gid]["red_package"]:
            return False
        return g_temp[gid]["red_package"]
    
    @staticmethod
    #根据关键词获取对应功能名称
    def get_function_name(key: str, self) -> str:
        return self.path[key][0]

    @staticmethod
    #根据指令内容获取开关类型
    def get_command_type(command: str, self) -> str:
        return next(
            (
                key
                for key, keywords in self.path.items()
                if any(keyword in command for keyword in keywords)
            ),
            "",
        )


    


utils = Utils()