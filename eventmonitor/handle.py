
import json
import nonebot

from typing import NoReturn
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import (
    Bot, Event, Message,
    PokeNotifyEvent,
    HonorNotifyEvent,
    GroupUploadNoticeEvent,
    GroupDecreaseNoticeEvent,
    GroupIncreaseNoticeEvent,
    GroupAdminNoticeEvent,
    LuckyKingNotifyEvent,
    MessageSegment,
    GroupMessageEvent
)

from .utils import utils
from .config import config

class Eventmonitor:
    @staticmethod
    async def chuo(matcher: Matcher, event: PokeNotifyEvent) -> NoReturn:
        if not (await utils.check_chuo(utils.g_temp, str(event.group_id))):
            await matcher.finish(utils.notAllow)
        # 获取用户id    
        uid: str = event.get_user_id()
        try:
            cd = event.time - utils.chuo_CD_dir[uid]                                          
        except KeyError:
            # 没有记录则cd为cd_time+1
            cd: int = utils.chuo_cd + 1                                                            
        if cd > utils.chuo_cd or event.get_user_id() in nonebot.get_driver().config.superusers:
            utils.chuo_CD_dir.update({uid: event.time})
            rely_msg: str = await config.chuo_send_msg()
            await matcher.finish(message=Message(rely_msg))

    @staticmethod
    async def switch(event: GroupMessageEvent, matcher: Matcher):
        # 获取开关指令的参数，即用户输入的指令内容
        command = str(event.get_message()).strip()
        # 获取群组ID
        gid = str(event.group_id)
        # 判断指令是否包含"开启"或"关闭"关键字
        if "开启" in command or "开始" in command:
            if key := utils.get_command_type(command):
                utils.g_temp[gid][key] = True
                utils.write_group_data(utils.g_temp)
                name = utils.get_function_name(key)
                await matcher.finish(f"{name}功能已开启喵")
        elif "禁止" in command or "关闭" in command:
            if key := utils.get_command_type(command):
                utils.g_temp[gid][key] = False
                utils.write_group_data(utils.g_temp)
                name = utils.get_function_name(key)
                await matcher.finish(f"{name}功能已禁用喵")
    
    @staticmethod
    async def state(event:GroupMessageEvent, matcher: Matcher):
        gid = str(event.group_id)
        with open(utils.address, "r", encoding="utf-8") as f:
            group_status = json.load(f)
        if gid not in group_status:
            await utils.config_check()
        else:
            await matcher.finish(f"群{gid}的Event配置状态：\n" + "\n".join
            (
                [f"{utils.path[func][0]}: {'开启' if group_status[gid][func] else '关闭'}" 
                 for func in utils.path]
            )
        )
    #群荣誉事件
    @staticmethod                                                         
    async def qrongyu(matcher: Matcher, event: HonorNotifyEvent, bot: Bot):
        if not (await utils.check_honor(utils.g_temp, str(event.group_id))):
            return
        bot_qq = int(bot.self_id)
        rely_msg: str = await config.monitor_rongyu(event.honor_type, event.user_id, bot_qq)
        await matcher.finish(message=Message(rely_msg))

    #群文件事件
    @staticmethod                                                                    
    async def files(matcher: Matcher, event: GroupUploadNoticeEvent):
        if not (await utils.check_file(utils.g_temp, str(event.group_id))):
            return
        rely: Message = MessageSegment.at(event.user_id) + '\n' + \
            MessageSegment.image(f'https://q4.qlogo.cn/headimg_dl?dst_uin={event.user_id}&spec=640') + \
            '\n 上传了新文件，感谢你一直为群里做贡献喵~' + MessageSegment.face(175)
        await matcher.finish(message=rely)

    #退群事件
    @staticmethod
    async def del_user(matcher: Matcher, event: GroupDecreaseNoticeEvent):
        if not (await utils.check_del_user(utils.g_temp, str(event.group_id))):
            return
        rely_msg: str | None = await config.del_user_bye(event.time, event.user_id)
        await matcher.finish(message=Message(rely_msg))

    #入群事件
    @staticmethod
    async def add_user(matcher: Matcher, event: GroupIncreaseNoticeEvent, bot: Bot):
        await utils.config_check()
        if not (await utils.check_add_user(utils.g_temp, str(event.group_id))):
            return
        bot_qq = int(bot.self_id)
        rely_msg = await  config.add_user_wecome(event.time, event.user_id, bot_qq)
        await matcher.finish(message=Message(rely_msg))

    #管理员变动
    @staticmethod
    async def admin_chance(matcher: Matcher, event: GroupAdminNoticeEvent, bot: Bot):
        if not (await utils.check_admin(utils.g_temp, str(event.group_id))):
            return
        bot_qq = int(bot.self_id)
        rely_msg: str = await config.admin_changer(event.sub_type, event.user_id, bot_qq)
        await matcher.finish(message=Message(rely_msg))
        
    #红包运气王
    @staticmethod
    async def hongbao(matcher: Matcher, event: LuckyKingNotifyEvent, bot: Bot):
        if not (await utils.check_red_package(utils.g_temp, str(event.group_id))):
            return
        bot_qq = int(bot.self_id)
        rely_msg = await config.rad_package_change(event.target_id, bot_qq)
        await matcher.finish(message=Message(rely_msg))

eventmonitor = Eventmonitor()