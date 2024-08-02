class Maps:
    def _mode(mode_map, prefix, mode_prefix, bridge_prefix, description, *aliases):
        mode_prefix = prefix + mode_prefix
        bridge_prefix = prefix + bridge_prefix
        for alias in aliases:
            mode_map[alias] = (mode_prefix, bridge_prefix, description)

    _BW = 'api_hypixel_player.player.stats.Bedwars.'
    MODE_BEDWARS = {None: (_BW, '', '')}

    def _dream(mode_func, mode_map, prefix, name, description, short):
        mode_func(mode_map, prefix, f'eight_two_{name}_', '', f'双人{description}模式', f'eight_two_{name}',
                  f'8_2_{name}', f'{short}2', f'{name}2')
        mode_func(mode_map, prefix, f'four_four_{name}_', '', f' 4v4v4v4 {description}模式', f'four_four_{name}',
                  f'4_4_{name}', f'{short}4', f'{name}4', f'{name}')

    _mode(MODE_BEDWARS, _BW, '', '', '', '', 'a', 'all', 'overall')
    _mode(MODE_BEDWARS, _BW, 'eight_one_', '', '单人模式', 'eight_one', 'solo', 'solos', '1', '1s', '81', '1v1', '8_1')
    _mode(MODE_BEDWARS, _BW, 'eight_two_', '', '双人模式', 'eight_two', 'double', 'doubles', '2', '2s', '82', '2v2',
          '8_2')
    _mode(MODE_BEDWARS, _BW, 'four_three_', '', ' 3v3v3v3 ', 'four_three', 'three', 'threes', '3', '3s', '43', '3v3',
          '3v3v3v3', '3333', '4_3')
    _mode(MODE_BEDWARS, _BW, 'four_four_', '', ' 4v4v4v4 ', 'four_four', 'four', 'fours', '4', '4s', '44', '4v4v4v4',
          '4444', '4_4')
    _mode(MODE_BEDWARS, _BW, 'two_four_', '', ' 4v4 ', 'two_four', '4v4', '24', '2_4')
    _mode(MODE_BEDWARS, _BW, 'castle_', '', ' 40v40 城池攻防战模式', 'castle', 'two_forty', '40', '240', '40v40')
    _dream(_mode, MODE_BEDWARS, _BW, 'voidless', '无虚空', 'v')
    _dream(_mode, MODE_BEDWARS, _BW, 'armed', '枪战', 'a')
    _dream(_mode, MODE_BEDWARS, _BW, 'swap', '交换', 's')
    _dream(_mode, MODE_BEDWARS, _BW, 'rush', '疾速', 'r')
    _dream(_mode, MODE_BEDWARS, _BW, 'ultimate', '超能力', 'u')
    _dream(_mode, MODE_BEDWARS, _BW, 'lucky', '幸运方块', 'l')
    _dream(_mode, MODE_BEDWARS, _BW, 'underworld', 'Underworld', 'uw')
    _DUELS = 'api_hypixel_player.player.stats.Duels.'
    MODE_DUELS = {None: (_DUELS, _DUELS, '')}
    _mode(MODE_DUELS, _DUELS, '', '', '', '', 'a', 'all', 'overall')
    _mode(MODE_DUELS, _DUELS, 'bow_duel_', 'bow_duel_', '弓箭决斗', 'bow_duel', 'bow')
    _mode(MODE_DUELS, _DUELS, 'classic_duel_', 'classic_duel_', '经典决斗', 'classic_duel', 'classic')
    _mode(MODE_DUELS, _DUELS, 'op_duel_', 'op_duel_', '高手决斗', 'op_duel', 'op')
    _mode(MODE_DUELS, _DUELS, 'uhc_duel_', 'uhc_duel_', '极限生存决斗', 'uhc_duel', 'uhc', 'buhc')
    _mode(MODE_DUELS, _DUELS, 'potion_duel_', 'potion_duel_', '药水决斗', 'potion_duel', 'potion', 'nodebuff', 'pot')
    _mode(MODE_DUELS, _DUELS, 'mw_duel_', 'mw_duel_', '超级战墙决斗', 'mw_duel', 'mw', 'megawall', 'megawalls')
    _mode(MODE_DUELS, _DUELS, 'blitz_duel_', 'blitz_duel_', '闪电饥饿游戏决斗', 'blitz_duel', 'blitz', 'bsg')
    _mode(MODE_DUELS, _DUELS, 'sw_duel_', 'sw_duel_', '空岛战争决斗', 'sw_duel', 'sw', 'skywar', 'skywars')
    _mode(MODE_DUELS, _DUELS, 'combo_duel_', 'combo_duel_', '连击决斗', 'combo_duel', 'combo')
    _mode(MODE_DUELS, _DUELS, 'bowspleef_duel_', 'bowspleef_duel_', '掘一死箭决斗', 'bowspleef_duel', 'bowspleef')
    _mode(MODE_DUELS, _DUELS, 'sumo_duel_', 'sumo_duel_', '相扑决斗', 'sumo_duel', 'sumo')
    _mode(MODE_DUELS, _DUELS, 'boxing_duel_', 'boxing_duel_', ' Boxing 决斗', 'boxing_duel', 'boxing')
    _mode(MODE_DUELS, _DUELS, 'bridge_duel_', 'bridge_duel_bridge_', '战桥决斗', 'bridge_duel', 'bridge')
    _mode(MODE_DUELS, _DUELS, 'uhc_doubles_', 'uhc_doubles_', '极限生存双人模式', 'uhc_doubles', 'uhc2')
    _mode(MODE_DUELS, _DUELS, 'uhc_four_', 'uhc_four_', '极限生存四人模式', 'uhc_four', 'uhc4')
    _mode(MODE_DUELS, _DUELS, 'sw_doubles_', 'sw_doubles_', '空岛战争双人模式', 'sw_doubles', 'sw2', 'skywar2',
          'skywars2')
    _mode(MODE_DUELS, _DUELS, 'mw_doubles_', 'mw_doubles_', '超级战墙双人模式', 'mw_doubles', 'mw2', 'megawall2',
          'megawalls2')
    _mode(MODE_DUELS, _DUELS, 'op_doubles_', 'op_doubles_', '高手双人模式', 'op_doubles', 'op2')
    _mode(MODE_DUELS, _DUELS, 'bridge_doubles_', 'bridge_doubles_bridge_', '战桥双人模式', 'bridge_doubles', 'bridge2')
    _mode(MODE_DUELS, _DUELS, 'bridge_threes_', 'bridge_threes_bridge_', '战桥三人模式', 'bridge_threes', 'bridge3')
    _mode(MODE_DUELS, _DUELS, 'bridge_four_', 'bridge_four_bridge_', '战桥四人模式', 'bridge_four', 'bridge4')
    _mode(MODE_DUELS, _DUELS, 'bridge_2v2v2v2_', 'bridge_2v2v2v2_bridge_', '战桥 2v2v2v2 模式', 'bridge_2v2v2v2',
          'bridge42')
    _mode(MODE_DUELS, _DUELS, 'bridge_3v3v3v3_', 'bridge_3v3v3v3_bridge_', '战桥 3v3v3v3 模式', 'bridge_3v3v3v3',
          'bridge43')
    _mode(MODE_DUELS, _DUELS, 'capture_threes_', 'capture_threes_bridge_', '战桥 CTF 三人模式', 'capture_threes',
          'capture', 'ctf')
    _mode(MODE_DUELS, _DUELS, 'uhc_meetup_', 'uhc_meetup_', '极限生存死亡竞赛', 'uhc_meetup', 'uhc_meetup',
          'uhc_deathmatch')
    _mode(MODE_DUELS, _DUELS, 'parkour_eight_', 'parkour_eight_', '跑酷决斗', 'parkour_eight', 'parkour')
    _mode(MODE_DUELS, _DUELS, 'duel_arena_', 'duel_arena_', '竞技场模式', 'duel_arena', 'arena')
    FAVORITE = {
        'null': '空',
        'wool': '羊毛',
        'hardened_clay': '粘土',
        'blast-proof_glass': '玻璃',
        'end_stone': '末地石',
        'ladder': '梯子',
        'oak_wood_planks': '木板',
        'obsidian': '黑曜石',
        'stone_sword': '石剑',
        'iron_sword': '铁剑',
        'diamond_sword': '钻石剑',
        'stick_(knockback_i)': '击退棒',
        'chainmail_boots': '锁链套',
        'iron_boots': '铁套',
        'diamond_boots': '钻石套',
        'shears': '剪刀',
        'wooden_pickaxe': '镐',
        'wooden_axe': '斧',
        'arrow': '箭',
        'bow': '弓',
        'bow_(power_i)': '力量弓',
        'bow_(power_i__punch_i)': '冲击弓',
        'speed_ii_potion_(45_seconds)': '速度',
        'jump_v_potion_(45_seconds)': '跳跃',
        'invisibility_potion_(30_seconds)': '隐身',
        'golden_apple': '金苹果',
        'bedbug': '床虱',
        'dream_defender': '铁傀儡',
        'fireball': '火球',
        'tnt': 'TNT',
        'ender_pearl': '珍珠',
        'water_bucket': '水桶',
        'bridge_egg': '搭桥蛋',
        'magic_milk': '牛奶',
        'sponge': '海绵',
        'compact_pop-up_tower': '速建塔',
        'magnum': '马格南手枪',
        'rifle': '步枪',
        'smg': 'SMG',
        'not-a-flamethrower': '不是喷火器',
        'shotgun': '霰弹枪',
        'Melee': '剑',
        'Tools': '工具',
        'Ranged': '弓',
        'Utility': '道具',
        'Blocks': '方块',
        'Potions': '药水',
        'Compass': '指南针'
    }
    SKYWARS_LEVELS = (
        (20, '20'),
        (50, '50'),
        (80, '80'),
        (100, '100'),
        (250, '250'),
        (500, '500'),
        (1000, '1k'),
        (1500, '1.5k'),
        (2500, '2.5k'),
        (4000, '4k'),
        (5000, '5k'),
        (10000, '10k')
    )
    SKYWARS_STAR = {
        'default': '\u22c6',
        'angel_1': '\u2605',
        'angel_2': '\u2606',
        'angel_3': '\u263c',
        'angel_4': '\u2736',
        'angel_5': '\u2733',
        'angel_6': '\u2734',
        'angel_7': '\u2737',
        'angel_8': '\u274b',
        'angel_9': '\u273c',
        'angel_10': '\u2742',
        'angel_11': '\u2741',
        'angel_12': '\u262c',
        'iron_prestige': '\u2719',
        'gold_prestige': '\u2764',
        'diamond_prestige': '\u2620',
        'emerald_prestige': '\u2726',
        'sapphire_prestige': '\u270c',
        'ruby_prestige': '\u2766',
        'crystal_prestige': '\u2735',
        'opal_prestige': '\u2763',
        'amethyst_prestige': '\u262f',
        'rainbow_prestige': '\u273a',
        'mythic_prestige': '\u0ca0_\u0ca0',
        'favor_icon': '\u2694',
        'omega_icon': '\u03a9'
    }
    RANK = {
        'ADMIN': '[ADMIN] ',
        'GAME_MASTER': '[GM] ',
        'YOUTUBER': '[YOUTUBE] ',
        'SUPERSTAR': '[MVP++] ',
        'VIP': '[VIP] ',
        'VIP_PLUS': '[VIP+] ',
        'MVP': '[MVP] ',
        'MVP_PLUS': '[MVP+] '
    }
    CAPE = {
        'http://textures.minecraft.net/texture/2340c0e03dd24a11b15a8b33c2a7e9e32abb2051b2481d0ba7defd635ca7a933': 'Migrator 迁移披风 (http://textures.minecraft.net/texture/2340c0e03dd24a11b15a8b33c2a7e9e32abb2051b2481d0ba7defd635ca7a933)',
        'http://textures.minecraft.net/texture/f9a76537647989f9a0b6d001e320dac591c359e9e61a31f4ce11c88f207f0ad4': 'Vanilla 双版本披风 (http://textures.minecraft.net/texture/f9a76537647989f9a0b6d001e320dac591c359e9e61a31f4ce11c88f207f0ad4)',
        'http://textures.minecraft.net/texture/e7dfea16dc83c97df01a12fabbd1216359c0cd0ea42f9999b6e97c584963e980': 'Minecon 2016 末影人披风 (http://textures.minecraft.net/texture/e7dfea16dc83c97df01a12fabbd1216359c0cd0ea42f9999b6e97c584963e980)',
        'http://textures.minecraft.net/texture/b0cc08840700447322d953a02b965f1d65a13a603bf64b17c803c21446fe1635': 'Minecon 2015 铁傀儡披风 (http://textures.minecraft.net/texture/b0cc08840700447322d953a02b965f1d65a13a603bf64b17c803c21446fe1635)',
        'http://textures.minecraft.net/texture/153b1a0dfcbae953cdeb6f2c2bf6bf79943239b1372780da44bcbb29273131da': 'Minecon 2013 活塞披风 (http://textures.minecraft.net/texture/153b1a0dfcbae953cdeb6f2c2bf6bf79943239b1372780da44bcbb29273131da)',
        'http://textures.minecraft.net/texture/a2e8d97ec79100e90a75d369d1b3ba81273c4f82bc1b737e934eed4a854be1b6': 'Minecon 2012 金镐披风 (http://textures.minecraft.net/texture/a2e8d97ec79100e90a75d369d1b3ba81273c4f82bc1b737e934eed4a854be1b6)',
        'http://textures.minecraft.net/texture/953cac8b779fe41383e675ee2b86071a71658f2180f56fbce8aa315ea70e2ed6': 'Minecon 2011 苦力怕披风 (http://textures.minecraft.net/texture/953cac8b779fe41383e675ee2b86071a71658f2180f56fbce8aa315ea70e2ed6)',
        'http://textures.minecraft.net/texture/9e507afc56359978a3eb3e32367042b853cddd0995d17d0da995662913fb00f7': 'Mojang Studios 披风 (http://textures.minecraft.net/texture/9e507afc56359978a3eb3e32367042b853cddd0995d17d0da995662913fb00f7)',
        'http://textures.minecraft.net/texture/5786fe99be377dfb6858859f926c4dbc995751e91cee373468c5fbf4865e7151': 'Mojang 披风 (http://textures.minecraft.net/texture/5786fe99be377dfb6858859f926c4dbc995751e91cee373468c5fbf4865e7151)'
    }
    PREFIX_COLOR = {
        'GOLD': '金色',
        'AQUA': '青色'
    }
    PLUS_COLOR = {
        'RED': '浅红色 (默认)',
        'GOLD': '金色 (35 级)',
        'GREEN': '浅绿色 (45 级)',
        'YELLOW': '黄色 (55 级)',
        'LIGHT_PURPLE': '粉色 (65 级)',
        'WHITE': '白色 (75 级)',
        'BLUE': '浅蓝色 (85 级)',
        'DARK_GREEN': '深绿色 (95 级)',
        'DARK_RED': '深红色 (150 级)',
        'DARK_AQUA': '青色 (150 级)',
        'DARK_PURPLE': '紫色 (200 级)',
        'DARK_GRAY': '灰色 (200 级)',
        'BLACK': '黑色 (250 级)',
        'DARK_BLUE': '深蓝色 (100 Rank)'
    }
    GUILD_TAG_COLOR = {
        None: '无标签',
        'GRAY': '灰色 (默认)',
        'GOLD': '金色 (MVP++)',
        'DARK_AQUA': '青色 (15 级)',
        'DARK_GREEN': '绿色 (25 级)',
        'YELLOW': '黄色 (45 级)'
    }
    GUILD_LEVELS = (
        (100000, '100k'),
        (150000, '150k'),
        (250000, '250k'),
        (500000, '500k'),
        (750000, '750k'),
        (1000000, '1m'),
        (1250000, '1.25m'),
        (1500000, '1.5m'),
        (2000000, '2m'),
        (2500000, '2.5m'),
        (2500000, '2.5m'),
        (2500000, '2.5m'),
        (2500000, '2.5m'),
        (2500000, '2.5m'),
        (3000000, '3m')
    )
    OFCAPE_DESIGN = {
        '852C2C5E1C1CE29F00441616': 'Standard',
        'F8F8F8DDDDDDFFFFFFC8C8C8': 'White',
        '8585855E5E5ECECECE444444': 'Gray',
        '1E1E1E010101404040202020': 'Black',
        '8500005E0000E20000440000': 'Red',
        '008500005E0000E200004400': 'Green',
        '00008500005E4040FF000044': 'Blue',
        'F2F200CACA00FFFF00BEBE00': 'Yellow',
        '8500855E005EE200E2440044': 'Purple',
        '008585005E5E00E2E2004444': 'Cyan'
    }
    OFCAPE_ALIGN = {
        's': 'Scale',
        't': 'Top',
        'm': 'Middle',
        'b': 'Bottom'
    }