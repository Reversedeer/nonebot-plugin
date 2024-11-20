import asyncio
from typing import NoReturn

from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message

from .config import api
from .message import msg


class Hyp:
	@staticmethod
	async def hyp(
		matcher: Matcher,
		arg: Message = CommandArg(),
	) -> NoReturn:
		"""hypixel"""
		args = str(arg).strip().split()
		if len(args) < 1:
			await matcher.finish(
				'请提供一个有效的ID'
			)
		uid: str = args[0]
		players_data = await api.player_data(uid)
		data_a = players_data['player_data']
		data_b = players_data['player_status']
		tasks = [
			api.get_player_online(data_b),
			api.get_player_rack(data_a),
			api.get_lastest_join(data_a),
			api.get_player_level(data_a),
		]
		(
			online,
			rank,
			last_login,
			level,
		) = await asyncio.gather(*tasks)
		data = {
			'online': online,
			'rank': rank,
			'last_login': last_login,
			'level': level,
		}
		reply = await msg.send_hyp_msg(data)
		await matcher.finish(reply)

	@staticmethod
	async def mc(
		matcher: Matcher,
		arg: Message = CommandArg(),
	):
		"""minecraft"""
		args = str(arg).strip().split()
		if len(args) < 1:
			await matcher.finish(
				'请提供一个有效的ID'
			)
		uid: str = args[0]
		data = await api.get_mc_data(uid)
		reply = await msg.send_mc_msg(data)
		await matcher.finish(reply)

	@staticmethod
	async def bw(
		matcher: Matcher,
		arg: Message = CommandArg(),
	):
		"""bw"""
		args = str(arg).strip().split()
		if len(args) < 1:
			await matcher.finish(
				'请提供一个有效的ID'
			)
		uid = args[0]
		players_data = await api.player_data(uid)
		data_a = players_data['player_data']
		tasks = [
			api.get_players_bedwars(data_a),
			api.get_player_rack(data_a),
		]
		(
			data_b,
			rank,
		) = await asyncio.gather(*tasks)
		data = {'data_b': data_b, 'rank': rank}
		reply: str = await msg.send_bw_msg(
			data, data_a
		)
		await matcher.finish(reply)


hyp = Hyp()
