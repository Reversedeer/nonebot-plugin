import contextlib
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11.permission import GROUP_OWNER, GROUP_ADMIN
from nonebot.plugin import on_notice, on_command
from nonebot import get_driver

from .handle import eventmonitor
from .utils import utils


# 获取 Nonebot 驱动实例
driver = get_driver()

@driver.on_bot_connect
async def _() -> None:
    await utils.init()
    await utils.config_check()

#戳一戳
chuo = on_notice(
    rule=utils._is_poke,
    priority=10,
    block=False,
    handlers=[eventmonitor.chuo]
)
# 群荣誉
qrongyu = on_notice(
    rule=utils._is_rongyu,
    priority=50,
    block=True,
    handlers=[eventmonitor.qrongyu]
)
# 群文件
files = on_notice(
    rule=utils._is_checker,
    priority=50,
    block=True,
    handlers=[eventmonitor.files]
)
# 群员减少
del_user = on_notice(
    rule=utils._is_del_user,
    priority=50,
    block=True,
    handlers=[eventmonitor.del_user]
)
# 群员增加
add_user = on_notice(
    rule=utils._is_add_user,
    priority=50,
    block=True,
    handlers=[eventmonitor.add_user]
)
# 群管理
group_admin = on_notice(
    rule=utils._is_admin_change,
    priority=50,
    block=True,
    handlers=[eventmonitor.admin_chance]
)
# 红包
red_packet = on_notice(
    rule=utils._is_red_packet,
    priority=50,
    block=True,
    handlers=[eventmonitor.hongbao]
)


on_command(
    "开启",
    aliases={"关闭"},
    priority=10,
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    block=True,
    handlers=[eventmonitor.switch]
)

on_command(
    "event配置",
    aliases={"event状态"},
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    priority=10,
    block=True,
    handlers=[eventmonitor.state]
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