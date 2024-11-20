from .config import api


class Message:
	@staticmethod
	async def send_bw_msg(data, data_a) -> str:
		"""构建/bw回复消息"""
		data_c = data.get('data_b')
		msg = (
			f"[{data_c['bw_level']}] {data['rank']} {data_a['displayname']} 的起床战争数据:\n"
			f"经验: {data_c['bw_experience']} | 硬币: {data_c['bw_coin']} | 连胜: {data_c['winstreak']}\n"
			f"拆床: {data_c['break_bed']} | 被拆床: {data_c['lost_bed']} | BBLR: {data_c['BBLR']}\n"
			f"胜场: {data_c['bw_win']} | 败场: {data_c['bw_losses']} | W/L: {data_c['W_L']}\n"
			f"击杀: {data_c['bw_kill']} | 死亡: {data_c['bw_death']} | K/D: {data_c['K_D']}\n"
			f"终杀: {data_c['bw_final_kill']} | 终死: {data_c['bw_final_death']} | FKDR: {data_c['FKDR']}\n"
			f"收集铁锭: {data_c['bw_iron']} | 收集金锭: {data_c['bw_gold']}\n"
			f"收集钻石: {data_c['bw_diamond']} | 收集绿宝石: {data_c['bw_emerald']}\n"
		)
		return msg

	@staticmethod
	async def send_hyp_msg(data) -> str:
		"""构建/hyp回复消息"""
		msg = (
			f"{data['rank']} {api.name} 的Hypixel信息:\n"
			f"在线情况: {data['online']} | Hypixel大厅等级: {data['level']}\n"
			f"最后登录时间: {data['last_login']}"
		)
		return msg

	@staticmethod
	async def send_mc_msg(data) -> str:
		"""构建/mc回复消息"""
		name = data.get('name')
		uuid = data.get('id')
		msg = f'ID: {name}\n' f'UUID: {uuid}'
		return msg


msg = Message()
