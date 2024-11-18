from .config import api


class Message:
    @staticmethod
    async def send_bw_msg(data, uid) -> str:
        """构建/bw回复消息"""
        mcdata = await api.get_mc_data(uid)
        name = mcdata.get("name")
        msg = "\n".join(
            [
                f"[{data.bw_level}] {data.Rank} {name} 的起床战争数据:",
                f"经验: {data.bw_experience} | 硬币: {format(data.bw_coin, ',d')} | 连胜: {format(data.winstreak, ',d')}",
                f"拆床: {format(data.break_bed, ',d')} | 被拆床: {format(data.lost_bed, ',d')} | BBLR: {data.BBLR}",
                f"胜场: {format(data.bw_win, ',d')} | 败场: {format(data.bw_losses, ',d')} | W/L: {data.W_L}",
                f"击杀: {format(data.bw_kill, ',d')} | 死亡: {format(data.bw_death, ',d')} | K/D: {data.K_D}",
                f"终杀: {format(data.bw_final_kill, ',d')} | 终死: {format(data.bw_final_death, ',d')} | FKDR: {data.FKDR}",
                f"收集铁锭: {format(data.bw_iron, ',d')} | 收集金锭: {format(data.bw_gold, ',d')}",
                f"收集钻石: {format(data.bw_diamond, ',d')} | 收集绿宝石: {format(data.bw_emerald, ',d')}",
            ]
        )
        return msg

    @staticmethod
    async def send_hyp_msg(data) -> str:
        """构建/hyp回复消息"""
        msg = (
            f"[{data['rank']}] {api.name} 的Hypixel信息:\n"
            f"在线情况: {data['online']} | Hypixel大厅等级: {data['level']}\n"
            f"最后登录时间: {data['last_login']}"
        )
        return msg

    @staticmethod
    async def send_mc_msg(data) -> str:
        """构建/mc回复消息"""
        name = data.get("name")
        uuid = data.get("id")
        msg = f"名称:{name}\n" f"UUID: {uuid}"
        return msg


msg = Message()
