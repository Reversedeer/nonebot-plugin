import contextlib
import nonebot
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11.permission import GROUP_OWNER, GROUP_ADMIN
from nonebot.plugin import on_notice, on_command
from nonebot.rule import Rule
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

from .utils import *

# 获取戳一戳状态
async def _is_poke(event: Event) -> bool:
    return isinstance(event, PokeNotifyEvent) and event.is_tome()
# 获取群荣誉变更
async def _is_rongyu(event: Event) -> bool:
    return isinstance(event, HonorNotifyEvent)
# 获取文件上传
async def _is_checker(event: Event) -> bool:
    return isinstance(event, GroupUploadNoticeEvent)
# 群成员减少
async def _is_del_user(event: Event) -> bool:
    return isinstance(event, GroupDecreaseNoticeEvent)
# 群成员增加
async def _is_add_user(event: Event) -> bool:
    return isinstance(event, GroupIncreaseNoticeEvent)
# 管理员变动
async def _is_admin_change(event: Event) -> bool:
    return isinstance(event, GroupAdminNoticeEvent)
# 红包运气王
async def _is_red_packet(event: Event) -> bool:
    return isinstance(event, LuckyKingNotifyEvent)

# 戳一戳
chuo = on_notice(
    Rule(_is_poke),
    priority=50,
    block=True
)
# 群荣誉
qrongyu = on_notice(
    Rule(_is_rongyu),
    priority=50,
    block=True
)
# 群文件
files = on_notice(
    Rule(_is_checker),
    priority=50,
    block=True
)
# 群员减少
del_user = on_notice(
    Rule(_is_del_user),
    priority=50,
    block=True
)
# 群员增加
add_user = on_notice(
    Rule(_is_add_user),
    priority=50,
    block=True
)
# 群管理
group_admin = on_notice(
    Rule(_is_admin_change),
    priority=50,
    block=True
)
# 红包
red_packet = on_notice(
    Rule(_is_red_packet),
    priority=50,
    block=True
)
# 功能开关
switch_command = on_command(
    "开启",
    aliases={"关闭"}, 
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    priority=10,
    block=True
)
#功能状态
state = on_command(
    "event配置",
    aliases={"event状态"},
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    priority=10,
    block=True
)

with contextlib.suppress(Exception):
    from nonebot.plugin import PluginMetadata

    __plugin_meta__ = PluginMetadata(
        name="eventmonitor",
        description="监控群事件的插件，支持戳一戳，成员变动，群荣誉变化等提示的插件",
        usage=utils.usage,
        type="application",
        homepage="https://github.com/Reversedeer/nonebot_plugin_eventmonitor",
        supported_adapters={"onebot.v11"},
        extra={
            "author": "Reversedeer",
            "version": "0.2.0",
            "priority": 50,
        },
    )