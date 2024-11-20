import time
import httpx
import asyncio

from nonebot.log import logger
from typing import Any, Dict, Literal

from .utils import utils


class Api:
	def __init__(self) -> None:
		self.mojang_profile = 'https://api.mojang.com/users/profiles/minecraft/'
		self.mojang_session = 'https://sessionserver.mojang.com/session/minecraft/profile/'
		self.hypixel_key = (
			'https://api.hypixel.net/key?key={}'
		)
		self.hypixel_counts = 'https://api.hypixel.net/counts?key={}'
		self.hypixel_player = 'https://api.hypixel.net/player?key={}&uuid={}'
		self.hypixel_status = 'https://api.hypixel.net/status?key={}&uuid={}'
		self.hypixel_friends = 'https://api.hypixel.net/friends?key={}&uuid={}'
		self.hypixel_guild_name = 'https://api.hypixel.net/guild?key={}&name={}'
		self.hypixel_guild_player = 'https://api.hypixel.net/guild?key={}&player={}'
		self.hypixel_recentgames = 'https://api.hypixel.net/recentgames?key={}&uuid={}'
		self.hypixel_punishmentstats = 'https://api.hypixel.net/punishmentstats?key={}'
		self.antisniper_denick = 'https://api.antisniper.net/denick?key={}&nick={}'
		self.antisniper_findnick = 'https://api.antisniper.net/findnick?key={}&name={}'
		self.antisniper_winstreak = 'https://api.antisniper.net/winstreak?key={}&name={}'
		self.optifine_cape = (
			'http://s.optifine.net/capes/{}.png'
		)
		self.optifine_format = (
			'https://optifine.net/banners&&'
		)
		self.optifine_banner = 'http://optifine.net/showBanner?format={}&valign={}'

	async def player_data(
		self, uid: str
	) -> Dict[str, Any]:
		"""玩家数据"""
		mcdata = await self.get_mc_data(uid)
		self.name = mcdata.get('name')
		(
			player_data,
			player_status,
		) = await asyncio.gather(
			self.get_player_data(mcdata),
			self.get_player_status(mcdata),
		)
		return {
			'player_data': player_data,
			'player_status': player_status,
		}

	async def get_mc_data(self, uid) -> Any:
		"""获取玩家minecraft信息"""
		for attempt in range(3):
			try:
				async with httpx.AsyncClient() as client:
					res = await client.get(
						self.mojang_profile + uid,
						timeout=10,
					)
					if res.status_code == 200:
						return res.json()
					elif res.status_code == 404:
						logger.error(
							'获取玩家minecraft信息时：不存在此玩家数据或数据丢失'
						)
			except httpx.TimeoutException:
				if attempt == 2:
					logger.error(
						'获取玩家minecraft信息请求超时，请稍后再试'
					)

	async def get_player_data(
		self, mcdata
	) -> dict[Any, Any]:
		"""获取玩家hypixel游戏数据"""
		for _ in range(3):
			try:
				async with httpx.AsyncClient() as client:
					uuid = mcdata.get('id')
					apikey = utils.hypixel_apikey
					url = self.hypixel_player.format(
						apikey, uuid
					)
					res: httpx.Response = (
						await client.get(
							url, timeout=10
						)
					)
					if res.status_code == 200:
						return res.json().get(
							'player'
						)
					if res.status_code == 400:
						logger.error(
							'获取玩家hypixel游戏数据发生错误：不存在此玩家数据或丢失'
						)
					if res.status_code == 403:
						logger.error(
							'获取玩家hypixel游戏数据发生错误：少密钥或此密钥无效'
						)
					if res.status_code == 429:
						logger.error(
							'获取玩家hypixel游戏数据发生错误：超出API请求次数限制'
						)
			except Exception:
				logger.error(
					'获取玩家hypixel游戏数据发生错误：可能是网络状况不佳'
				)
		return {}

	async def get_player_status(
		self, mcdata
	) -> dict[Any, Any]:
		"""获取玩家hypixel状态信息"""
		for _ in range(3):
			try:
				async with httpx.AsyncClient() as client:
					uuid = mcdata.get('id')
					apikey = utils.hypixel_apikey
					url = self.hypixel_status.format(
						apikey, uuid
					)
					res: httpx.Response = (
						await client.get(
							url, timeout=10
						)
					)
					if res.status_code == 200:
						return (
							res.json()
							.get('session')
							.get('online')
						)
					if res.status_code == 422:
						logger.error(
							'获取玩家hypixel状态信息时发生错误：不存在此玩家数据或丢失'
						)
					if res.status_code == 403:
						logger.error(
							'获取玩家hypixel状态信息时发生错误：少密钥或此密钥无效'
						)
			except Exception:
				logger.error(
					'获取玩家hypixel状态信息时发生错误：发生意外请检查错误日志'
				)
		return {}

	async def get_player_online(self, data_b):
		"""获取玩家在线状态"""
		online = data_b
		if online:
			online = '在线'
		else:
			online = '离线'
		return online

	async def get_player_rack(self, players_data):
		"""获取玩家rank"""
		rank_id = players_data.get(
			'newPackageRank'
		)
		if rank_id == 'VIP' or rank_id == 'MVP':
			rank = f'[{rank_id}]'
		elif (
			rank_id == 'VIP_PLUS'
			or rank_id == 'MVP_PLUS'
		):
			rank = f"[{rank_id.replace('_PLUS', '+')}]"
		return rank

	async def get_lastest_join(
		self, players_data
	) -> str:
		"""获取玩家上线时间"""
		player_time = players_data.get(
			'lastLogin'
		)
		if player_time is not None:
			time_array = time.localtime(
				player_time / 1000
			)
			last_login = time.strftime(
				'%Y-%m-%d %H:%M:%S', time_array
			)
		else:
			last_login = (
				'对方隐藏了最后的上线时间'
			)
		return last_login

	async def get_player_level(
		self, players_data
	):
		"""获取玩家等级"""
		xp = players_data.get('networkExp')
		if xp is not None:
			prefix = -3.5
			const = 12.25
			divides = 0.0008
			try:
				lv = int(
					(divides * int(xp) + const)
					** 0.5
					+ prefix
					+ 1
				)
				level = lv
			except ValueError:
				level = None
		else:
			level = None
		return level

	async def get_hypixel_bedwars_level(
		self, Exp: int
	):
		"""起床等级算法"""
		if Exp < 500:
			level = '0✫'
			experience = str(Exp) + '/500'
		elif Exp >= 500 and Exp < 1500:
			level = '1✫'
			experience = str(Exp - 500) + '/1k'
		elif Exp >= 1500 and Exp < 3500:
			level = '2✫'
			experience = str(Exp - 1500) + '/2k'
		elif Exp >= 3500 and Exp < 7000:
			level = '3✫'
			experience = str(Exp - 3500) + '/3.5k'
		elif Exp >= 7000:
			if Exp < 487000:
				add_level = int(
					(Exp - 7000) / 5000
				)
				level = str(4 + add_level) + '✫'
				experience = (
					str(
						Exp
						- 7000
						- add_level * 5000
					)
					+ '/5k'
				)
			if Exp >= 487000:
				surplus_experience = (
					Exp
					- (int(Exp / 487000)) * 487000
				)
				if surplus_experience < 500:
					add_level = 0
					experience = (
						str(surplus_experience)
						+ '/500'
					)
				elif (
					surplus_experience >= 500
					and surplus_experience < 1500
				):
					add_level = 1
					experience = (
						str(
							surplus_experience
							- 500
						)
						+ '/1k'
					)
				elif (
					surplus_experience >= 1500
					and surplus_experience < 3500
				):
					add_level = 2
					experience = (
						str(
							surplus_experience
							- 1500
						)
						+ '/2k'
					)
				elif (
					surplus_experience >= 3500
					and surplus_experience < 7000
				):
					add_level = 3
					experience = (
						str(
							surplus_experience
							- 3500
						)
						+ '3.5k'
					)
				elif surplus_experience >= 7000:
					add_level = int(
						(
							surplus_experience
							- 7000
						)
						/ 5000
					)
					experience = str(
						surplus_experience
						- 7000
						- add_level * 5000
					)
				level = (
					str(
						(int(Exp / 487000)) * 100
						+ 4
						+ add_level
					)
					+ '✫'
				)
		bw_level = level
		bw_experience = experience
		return {
			'bw_experience': bw_experience,
			'bw_level': bw_level,
		}

	async def get_players_bedwars(self, data_a):
		stats_data = data_a.get('stats')
		if stats_data:
			"""起床战争数据"""
			bedwars_data = stats_data.get(
				'Bedwars'
			)
			if bedwars_data:
				# 基本信息
				data_b = await api.get_hypixel_bedwars_level(
					int(
						bedwars_data.get(
							'Experience'
						)
					)
				)  # 等级
				bw_experience = data_b.get(
					'bw_experience'
				)
				bw_level = data_b.get('bw_level')
				bw_coin = bedwars_data.get(
					'coins'
				)  # 硬币
				winstreak = bedwars_data.get(
					'winstreak'
				)  # 连胜
				# 床
				break_bed = bedwars_data.get(
					'beds_broken_bedwars'
				)  # 破坏床数
				lost_bed = bedwars_data.get(
					'beds_lost_bedwars'
				)  # 被破坏床数
				BBLR = round(
					break_bed / lost_bed, 3
				)  # 破坏床数和被破坏床数的比
				# 胜败
				bw_win = bedwars_data.get(
					'wins_bedwars'
				)  # 胜利
				bw_losses = bedwars_data.get(
					'losses_bedwars'
				)  # 失败
				W_L = round(
					bw_win / bw_losses, 3
				)  # 胜利和失败的比
				# 普通击杀/死亡
				bw_kill = bedwars_data.get(
					'kills_bedwars'
				)  # 击杀
				bw_death = bedwars_data.get(
					'deaths_bedwars'
				)  # 死亡
				K_D = round(
					bw_kill / bw_death, 3
				)  # KD值
				# 最终击杀/死亡
				bw_final_kill = bedwars_data.get(
					'final_kills_bedwars'
				)  # 最终击杀
				bw_final_death = bedwars_data.get(
					'final_deaths_bedwars'
				)  # 最终死亡
				FKDR = round(
					bw_final_kill
					/ bw_final_death,
					3,
				)  # 最终KD值
				# 矿物收集
				bw_iron = (
					bedwars_data.get(
						'iron_resources_collected_bedwars'
					)
					if bedwars_data.get(
						'iron_resources_collected_bedwars'
					)
					else 0
				)  # 铁锭收集
				bw_gold = (
					bedwars_data.get(
						'gold_resources_collected_bedwars'
					)
					if bedwars_data.get(
						'gold_resources_collected_bedwars'
					)
					else 0
				)  # 金锭收集
				bw_diamond = (
					bedwars_data.get(
						'diamond_resources_collected_bedwars'
					)
					if bedwars_data.get(
						'diamond_resources_collected_bedwars'
					)
					else 0
				)  # 钻石收集
				bw_emerald = (
					bedwars_data.get(
						'emerald_resources_collected_bedwars'
					)
					if bedwars_data.get(
						'emerald_resources_collected_bedwars'
					)
					else 0
				)  # 绿宝石收集
		return {
			'bw_level': bw_level,
			'bw_experience': bw_experience,
			'bw_coin': bw_coin,
			'winstreak': winstreak,
			'break_bed': break_bed,
			'lost_bed': lost_bed,
			'BBLR': BBLR,
			'bw_win': bw_win,
			'bw_losses': bw_losses,
			'W_L': W_L,
			'bw_kill': bw_kill,
			'bw_death': bw_death,
			'K_D': K_D,
			'bw_final_kill': bw_final_kill,
			'bw_final_death': bw_final_death,
			'FKDR': FKDR,
			'bw_iron': bw_iron,
			'bw_gold': bw_gold,
			'bw_diamond': bw_diamond,
			'bw_emerald': bw_emerald,
		}


api = Api()
