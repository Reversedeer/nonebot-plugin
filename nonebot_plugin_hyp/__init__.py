import nonebot
import contextlib

from nonebot.plugin import on_command
from nonebot import get_driver, require
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN

from .utils import utils
from .handle import hyp

require("nonebot_plugin_localstore")

import nonebot_plugin_localstore as store

on_command(
    "hyp",
    aliases={"hypixel"},
    priority=10,
    block=True,
    handlers=[hyp.hyp]
)

with contextlib.suppress(Exception):
    from nonebot.plugin import PluginMetadata

    __plugin_meta__ = PluginMetadata(
        name="hyp",
        description="查询hypixel游戏数据插件",
        usage=utils.usage,
        type="application",
        homepage="https://github.com/Reversedeer/nonebot_plugin_hyp",
        supported_adapters={"~onebot.v11"},
        extra={
            "author": "Reversedeer",
            "version": "0.0.1",
            "priority": 10,
        },
    )