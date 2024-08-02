class Pipes:
    LAST_COMMAND = 0.0

    @staticmethod
    def cooldown(main, message):
        if message.user not in main.options.get('global.bypass_cooldown', []):
            now_time = time.time()
            if now_time > Pipes.LAST_COMMAND + main.options.get('global.cooldown_time'):
                Pipes.LAST_COMMAND = now_time
            else:
                raise BotException('使用指令过快!')

    @staticmethod
    def _api(name, requester, response_processor, *args):
        def _(main, message):
            api_url = message.get(f'apiset.{name}', '')
            url_args = tuple([message.get(arg, '') for arg in args])
            if len(url_args) == 0:
                url = api_url
            elif len(url_args) == 1:
                url = api_url % url_args[0]
            else:
                url = api_url % url_args
            response = requester(url, headers={'User-Agent': message.get('user_agent', '')})
            data = response_processor(response)
            message.data['api_%s' % name] = data

        return _

    @staticmethod
    def _api_status(name, response, code=200):
        if response.status_code != code:
            raise BotException('API %s 查询失败! (HTTP %d)' % (name, response.status_code))

    @staticmethod
    def api(name, success_flag=None, test_key=None, *args):
        def _(response):
            Pipes._api_status(name, response, 200)
            data = json.loads(response.content.decode('utf-8'))
            if success_flag is not None:
                if not Utils.get(data, success_flag, False):
                    raise BotException('API %s 查询失败! (Failed)' % name)
            if test_key is not None:
                if Utils.get(data, test_key) is None:
                    raise BotException('API %s 查询失败! (None)' % name)
            return data

        return Pipes._api(name, requests.get, _, *args)

    @staticmethod
    def api_binary(name, *args):
        def _(response):
            Pipes._api_status(name, response, 200)
            return response.content

        return Pipes._api(name, requests.get, _, *args)

    @staticmethod
    def api_optifine_format():
        def _requester(url, headers):
            url, name = url.split('&&')
            return requests.post(url, data=f'username={name}',
                                 headers={**headers, 'Content-Type': 'application/x-www-form-urlencoded'},
                                 allow_redirects=False)

        def _processer(response):
            if response.status_code != 302:
                return None
            location = response.headers.get('Location', '')
            index_equal = location.find('=')
            index_and = location.find('&')
            if not location or index_equal == -1 or index_and == -1 or index_equal >= index_and:
                return None
            return location[index_equal + 1:index_and]

        return Pipes._api('optifine_format', _requester, _processer, 'api_mojang_profile.name')

    @staticmethod
    def re_expression(exp, arg, error_msg):
        def _(main, message):
            value = message.get(arg)
            if not isinstance(value, str) or not exp.fullmatch(value):
                raise BotException(error_msg)

        return _

    @staticmethod
    def replace(mapping):
        def _(main, message):
            message.placeholders.update(mapping)

        return _

    @staticmethod
    def plus(value_a, value_b, result):
        def _(main, message):
            message.set(result, message.get(value_a, 0) + message.get(value_b, 0))

        return _

    @staticmethod
    def game_mode(mode_map, mode_arg, arg='args.2', placeholder='!', placeholder_bridge='`'):
        def _(main, message):
            mode_name = message.get(arg, None)
            if mode_name in mode_map:
                mode = mode_map[mode_name]
                message.placeholders[placeholder] = mode[0]
                message.placeholders[placeholder_bridge] = mode[1]
                message.set(mode_arg, mode[2])
            else:
                raise BotException('未知的模式!')

        return _

    @staticmethod
    def session(main, message):
        uuid = message.get('api_mojang_session.id', '?' * 32)
        properties = message.get('api_mojang_session.properties', [])
        message.set('session.id_dashed', f'{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}')
        for property in properties:
            if property.get('name', '') == 'textures':
                value = json.loads(base64.b64decode(property.get('value', '')).decode())
                message.set('session.skin', Utils.get(value, 'textures.SKIN.url', '默认'))
                if Utils.get(value, 'textures.SKIN.metadata.model') == 'slim':
                    message.set('session.model', '纤细 (Alex)')
                else:
                    message.set('session.model', '默认 (Steve)')
                cape = Utils.get(value, 'textures.CAPE.url')
                if cape is None:
                    message.set('session.cape', '无')
                else:
                    cape = Maps.CAPE.get(cape, cape)
                    message.set('session.cape', cape)
                break

    @staticmethod
    def hypixel(main, message):
        uuid = message.get('api_mojang_profile.id')
        username = message.get('api_hypixel_player.player.displayname', '无')
        username_mojang = message.get('api_mojang_profile.name')
        custom_rank = main.options.get(f'options.hypixel.ranks.{uuid}')
        rank = ''
        rank_raw = 'NONE'
        rank_prefix = message.get('api_hypixel_player.player.prefix')
        rank_rank = message.get('api_hypixel_player.player.rank')
        rank_monthly = message.get('api_hypixel_player.player.monthlyPackageRank')
        rank_new = message.get('api_hypixel_player.player.newPackageRank')
        rank_package = message.get('api_hypixel_player.player.packageRank')
        if rank_prefix is not None:
            rank, rank_raw = Utils.reset_style(rank_prefix) + ' ', 'CUSTOM'
        elif rank_rank in Maps.RANK:
            rank, rank_raw = Maps.RANK[rank_rank], rank_rank
        elif rank_monthly in Maps.RANK:
            rank, rank_raw = Maps.RANK[rank_monthly], rank_monthly
        elif rank_new in Maps.RANK:
            rank, rank_raw = Maps.RANK[rank_new], rank_new
        elif rank_package in Maps.RANK:
            rank, rank_raw = Maps.RANK[rank_package], rank_package
        if custom_rank is not None:
            rank = custom_rank.replace('{rank}', rank)
        message.set('hypixel.name', rank + username_mojang)
        message.set('hypixel.rank_raw', rank_raw)
        if username != username_mojang:
            message.set('hypixel.name_change', f'\n此玩家已改名! ({username} -> {username_mojang})')
        else:
            message.set('hypixel.name_change', '')

    @staticmethod
    def command_hypixel(main, message):
        rank_raw = message.get('hypixel.rank_raw', 'NONE')
        hypixel_exp = message.get('api_hypixel_player.player.networkExp', 0.0)
        hypixel_level = (0.0008 * hypixel_exp + 12.25) ** 0.5 - 2.5
        rank_prefix_color = message.get('api_hypixel_player.player.monthlyRankColor', 'GOLD')
        rank_plus_color = message.get('api_hypixel_player.player.rankPlusColor', 'RED')
        rank_color_line = ''
        if rank_raw == 'MVP_PLUS':
            rank_color_line = f'\nMVP+ 颜色: {Maps.PLUS_COLOR.get(rank_plus_color, rank_plus_color)}'
        elif rank_raw == 'SUPERSTAR':
            rank_color_line = f'\nMVP 颜色: {Maps.PREFIX_COLOR.get(rank_prefix_color, rank_prefix_color)} | ++ 颜色: {Maps.PLUS_COLOR.get(rank_plus_color, rank_plus_color)}'
        message.set('hypixel.level', hypixel_level)
        message.set('hypixel.rank_color', rank_color_line)

    @staticmethod
    def command_bedwars(main, message):
        bedwars_total_exp = message.get('api_hypixel_player.player.stats.Bedwars.Experience', 0)
        bedwars_level = 100 * (bedwars_total_exp // 487000)
        bedwars_exp = 0
        bedwars_full_exp = '0'
        bedwars_total_exp %= 487000
        if bedwars_total_exp < 500:
            bedwars_level, bedwars_exp, bedwars_full_exp = bedwars_level, bedwars_total_exp, '500'
        elif bedwars_total_exp < 1500:
            bedwars_level, bedwars_exp, bedwars_full_exp = bedwars_level + 1, bedwars_total_exp - 500, '1k'
        elif bedwars_total_exp < 3500:
            bedwars_level, bedwars_exp, bedwars_full_exp = bedwars_level + 2, bedwars_total_exp - 1500, '2k'
        elif bedwars_total_exp < 7000:
            bedwars_level, bedwars_exp, bedwars_full_exp = bedwars_level + 3, bedwars_total_exp - 3500, '3.5k'
        else:
            bedwars_level, bedwars_exp, bedwars_full_exp = bedwars_level + 4 + (bedwars_total_exp - 7000) // 5000, (
                        bedwars_total_exp - 7000) % 5000, '5k'
        bedwars_level = int(bedwars_level)
        bedwars_exp = int(bedwars_exp)
        bedwars_shop = message.get('api_hypixel_player.player.stats.Bedwars.favourites_2', Consts.DEFAULT_SHOP).split(
            ',')
        bedwars_slots = message.get('api_hypixel_player.player.stats.Bedwars.favorite_slots',
                                    Consts.DEFAULT_SLOTS).split(',')
        message.set('bedwars.shop',
                    Utils.format_shop(Maps.FAVORITE, bedwars_shop[:7]) +
                    Utils.format_shop(Maps.FAVORITE, bedwars_shop[7:14]) +
                    Utils.format_shop(Maps.FAVORITE, bedwars_shop[14:]))
        message.set('bedwars.slots', Utils.format_shop(Maps.FAVORITE, bedwars_slots))
        message.set('bedwars.level', str(bedwars_level))
        message.set('bedwars.level_int', bedwars_level)
        message.set('bedwars.star',
                    '\u272b' if bedwars_level < 1100 else '\u272a' if bedwars_level < 2100 else '\u269d')
        message.set('bedwars.exp', bedwars_exp)
        message.set('bedwars.full_exp', bedwars_full_exp)

    @staticmethod
    def command_skywars(main, message):
        skywars_total_exp = int(message.get('api_hypixel_player.player.stats.SkyWars.skywars_experience', 0))
        skywars_level = 0
        skywars_exp = skywars_total_exp
        skywars_full_exp = '0'
        skywars_icon = message.get('api_hypixel_player.player.stats.SkyWars.selected_prestige_icon', 'default')
        skywars_corrupt = message.get('api_hypixel_player.player.stats.SkyWars.angel_of_death_level', 0)
        skywars_angels_offering = message.get('api_hypixel_player.player.stats.SkyWars.angels_offering', 0) > 0
        skywars_favor_of_the_angel = 'favor_of_the_angel' in message.get(
            'api_hypixel_player.player.stats.SkyWars.packages', [])
        skywars_corrupt_suffix = ''
        if skywars_angels_offering:
            if skywars_favor_of_the_angel:
                skywars_corrupt_suffix = ' (天使之祭&天使眷顾)'
            else:
                skywars_corrupt_suffix = ' (天使之祭)'
        elif skywars_favor_of_the_angel:
            skywars_corrupt_suffix = ' (天使眷顾)'
        if skywars_angels_offering:
            skywars_corrupt += 1
        if skywars_favor_of_the_angel:
            skywars_corrupt += 1
        skywars_level, skywars_exp, skywars_full_exp = Utils.get_level(skywars_total_exp, Maps.SKYWARS_LEVELS)
        message.set('skywars.level', skywars_level)
        message.set('skywars.exp', skywars_exp)
        message.set('skywars.full_exp', skywars_full_exp)
        message.set('skywars.star', Maps.SKYWARS_STAR.get(skywars_icon, '?'))
        message.set('skywars.corrupt', '%d%%%s' % (skywars_corrupt, skywars_corrupt_suffix))

    @staticmethod
    def command_guild(api):
        def _(main, message):
            members = message.get(f'api_hypixel_guild_{api}.guild.members', [])
            exp = message.get(f'api_hypixel_guild_{api}.guild.exp', 0)
            tag_color = message.get(f'api_hypixel_guild_{api}.guild.tagColor')
            preferred_games = message.get(f'api_hypixel_guild_{api}.guild.preferredGames', [])
            level, guild_exp, full_exp = Utils.get_level(exp, Maps.GUILD_LEVELS)
            level -= 1
            message.set('guild.member_count', len(members))
            message.set('guild.level', level)
            message.set('guild.exp', guild_exp)
            message.set('guild.full_exp', full_exp)
            message.set('guild.double_exp', min(100, level // 3 * 2 + level % 3))
            message.set('guild.double_coins', min(100, level // 3))
            message.set('guild.tag_color', Maps.GUILD_TAG_COLOR.get(tag_color, tag_color))
            message.set('guild.preferred_games', ', '.join(
                [Utils.string_to_camel(game) for game in preferred_games]) if preferred_games else '无')

        return _

    @staticmethod
    def command_guild_player(api):
        def _(main, message):
            members = message.get(f'api_hypixel_guild_{api}.guild.members', [])
            groups = message.get(f'api_hypixel_guild_{api}.guild.ranks', [])
            group_map = {x.get('name', '?').lower(): x.get('tag') for x in groups}
            uuid = message.get('api_mojang_profile.id', 'Love')
            for member in members:
                rank = member.get('rank', '###CUTE###').lower()
                if member.get('uuid', 'Q_TT') == uuid or (rank not in group_map and uuid == 'Love'):
                    tag = group_map.get(rank, '[]ILoveQ_TTForever')
                    if tag == '[]ILoveQ_TTForever': tag = 'GM'
                    message.set('guild.player', member)
                    message.set('guild.player.tag', f' [{tag}]' if tag else '')
                    message.set('guild.player.exp', dict(zip(map(str, range(7)), map(lambda x: x[1], sorted(
                        member.get('expHistory', {}).items(), key=lambda x: x[0])))))
                    break

        return _

    @staticmethod
    def _check_valign(main, message, valign, binary):
        message.set('ofcape.valign', valign)
        APIs.OPTIFINE_BANNER(main, message)
        image_match = Utils.get_image(message.get('api_optifine_banner'), (2, 2, 22, 34))
        return image_match.tobytes() == binary

    @staticmethod
    def command_optifine_cape(main, message):
        name = message.get('api_mojang_profile.name', '')
        image = Utils.get_image(message.get('api_optifine_cape'))
        image_banner = image.crop((2, 2, 22, 34)).tobytes()
        color_top = ''.join(map('%02X'.__mod__, image.getpixel((22, 2))))
        color_bottom = ''.join(map('%02X'.__mod__, image.getpixel((22, 33))))
        of_format = message.get('api_optifine_format')
        if of_format is None:
            color_text = ''.join(map('%02X'.__mod__, image.getpixel((6, 10))))
            color_shadow = ''.join(map('%02X'.__mod__, image.getpixel((6, 12))))
            colors = color_top + color_bottom + color_text + color_shadow
            message.set('ofcape.design', Maps.OFCAPE_DESIGN.get(colors, 'Custom...'))
            message.set('ofcape.custom', f'\nText: {color_text}\nShadow: {color_shadow}')
            message.set('ofcape.banner', '')
        else:
            valign = 'b'
            message.set('ofcape.url', of_format)
            for va in 'stm':
                if Pipes._check_valign(main, message, va, image_banner):
                    valign = va
                    break
            if not Pipes._check_valign(main, message, valign, image_banner):
                raise BotException('OptiFine 披风查询失败!')
            align = Maps.OFCAPE_ALIGN.get(valign, 'Unknown')
            message.set('ofcape.design', 'Banner...')
            message.set('ofcape.banner', f'\nURL: {of_format}\nAlign: {align}')
            message.set('ofcape.custom', '')
        message.set('ofcape.top', color_top)
        message.set('ofcape.bottom', color_bottom)