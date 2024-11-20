import contextlib

from nonebot.plugin import on_command
from nonebot import require

from .handle import hyp
from .utils import utils

require('nonebot_plugin_localstore')


on_command(
	'hyp',
	aliases={'hypixel'},
	priority=10,
	block=True,
	handlers=[hyp.hyp],
)

on_command(
	'mc',
	aliases={'minecraft'},
	priority=10,
	block=True,
	handlers=[hyp.mc],
)

on_command(
	'bw',
	aliases={'bedwars'},
	priority=10,
	block=True,
	handlers=[hyp.bw],
)

with contextlib.suppress(Exception):
	from nonebot.plugin import PluginMetadata

	__plugin_meta__ = PluginMetadata(
		name='hyp',
		description='查询hypixel游戏数据插件',
		usage=utils.usage,
		type='application',
		homepage='https://github.com/Reversedeer/nonebot_plugin_hyp',
		supported_adapters={'~onebot.v11'},
		extra={
			'author': 'Reversedeer',
			'version': '0.0.1',
			'priority': 10,
		},
	)
