from nonebot.matcher import matchers
from .utils import utils
from nonebot.adapters.onebot.v11 import (
    PokeNotifyEvent

)


class Event:
    @staticmethod
    async def chuo(event: PokeNotifyEvent):
        if not (await check_chuo(g_temp, str(event.group_id))):
            await matchers.finish(utils.notAllow, at_sender=True)
        # 获取用户id    
        uid = event.get_user_id()
        # 计算cd                                                       
        try:
            cd = event.time - chuo_CD_dir[uid]                                          
        except KeyError:
            # 没有记录则cd为cd_time+1
            cd = chuo_cd + 1                                                            
        if (
            cd > chuo_cd
            or event.get_user_id() in nonebot.get_driver().config.superusers
        ):# 记录cd                                                                                   
            chuo_CD_dir.update({uid: event.time})
        rely_msg = await chuo_send_msg()
        await chuo.finish(message=Message(rely_msg))

    #群荣誉变化
    @qrongyu.handle()                                                                       
    async def send_rongyu(event: HonorNotifyEvent, bot: Bot):
        if not (await check_honor(g_temp, str(event.group_id))):
            return
        bot_qq = int(bot.self_id)
        rely_msg = await monitor_rongyu(event.honor_type, event.user_id, bot_qq)
        await qrongyu.finish(message=Message(rely_msg))

    #上传群文件
    @files.handle()                                                                         
    async def handle_first_receive(event: GroupUploadNoticeEvent):
        if not (await check_file(g_temp, str(event.group_id))):
            return
        rely = MessageSegment.at(event.user_id) + '\n' + \
            MessageSegment.image(f'https://q4.qlogo.cn/headimg_dl?dst_uin={event.user_id}&spec=640') + \
            '\n 上传了新文件，感谢你一直为群里做贡献喵~' + MessageSegment.face(175)
        await files.finish(message=rely)

    #退群事件
    @del_user.handle()
    async def user_bye(event: GroupDecreaseNoticeEvent):
        if not (await check_del_user(g_temp, str(event.group_id))):
            return
        rely_msg = await  del_user_bye(event.time, event.user_id)
        await del_user.finish(message=Message(rely_msg))

    #入群事件
    @add_user.handle()
    async def user_welcome(event: GroupIncreaseNoticeEvent, bot: Bot):
        await config_check()
        if not (await check_add_user(g_temp, str(event.group_id))):
            return
        bot_qq = int(bot.self_id)
        rely_msg = await  add_user_wecome(event.time, event.user_id, bot_qq)
        await add_user.finish(message=Message(rely_msg))

    #管理员变动
    @group_admin.handle()
    async def admin_chance(event: GroupAdminNoticeEvent, bot: Bot):
        if not (await check_admin(g_temp, str(event.group_id))):
            return
        bot_qq = int(bot.self_id)
        rely_msg = await admin_changer(event.sub_type, event.user_id, bot_qq)
        await group_admin.finish(message=Message(rely_msg))
        
    #红包运气王
    @red_packet.handle()
    async def hongbao(event: LuckyKingNotifyEvent):
        if not (await check_red_package(g_temp, str(event.group_id))):
            return
        rely_msg = MessageSegment.at(event.user_id) + "\n" + "本次红包运气王为：" + MessageSegment.at(event.target_id)
        await red_packet.finish(message=rely_msg)

    @switch_command.handle()
    async def switch(event: GroupMessageEvent, matcher: Matcher):
        # 获取开关指令的参数，即用户输入的指令内容
        command = str(event.get_message()).strip()
        # 获取群组ID
        gid = str(event.group_id)
        # 判断指令是否包含"开启"或"关闭"关键字
        if "开启" in command or "开始" in command:
            if key := get_command_type(command):
                g_temp[gid][key] = True
                write_group_data(g_temp)
                name = get_function_name(key)
                await matcher.finish(f"{name}功能已开启喵")
        elif "禁止" in command or "关闭" in command:
            if key := get_command_type(command):
                g_temp[gid][key] = False
                write_group_data(g_temp)
                name = get_function_name(key)
                await matcher.finish(f"{name}功能已禁用喵")

    @state.handle()
    async def event_state(event:GroupMessageEvent, matcher: Matcher):
        gid = str(event.group_id)
        with open(address, "r", encoding="utf-8") as f:
            group_status = json.load(f)
        if gid not in group_status:
            await config_check()
        else:
            await matcher.finish(f"群{gid}的Event配置状态：\n" + "\n".join
            (
                [f"{path[func][0]}: {'开启' if group_status[gid][func] else '关闭'}" for func in
                path]
            )
        )

    async def init(g_temp):
        """
        初始化配置文件
        :return:
        """   
        # 如果数据文件路径不存在，则创建目录
        if not os.path.exists(config_path):  
            os.makedirs(config_path)  
        if os.path.exists(address):
            # 如果数据文件路径存在，尝试读取数据文件（config.json）
            with open(address, "r", encoding="utf-8") as f:
                g_temp.update(json.load(f))
        else:
            # 如果群数据文件不存在，则初始化g_temp为空字典，并写入对应的文件
            bot = nonebot.get_bot()
            group_list = await bot.get_group_list()
            #从group_list中遍历每个群组
            for group in group_list:
                # 为每个群组创建一个临时字典temp，用于存储群组的配置信息
                temp = {}
                for g_name in path:
                    # 将群组的每个配置项设置为默认值True
                    temp[g_name] = True
                    # 特殊情况下（g_name为'red_package'），将该配置项设为False
                    if g_name in ['red_package']:
                        temp[g_name] = False
                # 获取群组ID并转换为字符串类型
                gid = str(group["group_id"])
                # 将临时字典temp作为值，群组ID作为键，添加到g_temp字典中
                g_temp[gid] = temp
                # 将更新后的g_temp字典写入群组数据
                write_group_data(g_temp)

event = Event()