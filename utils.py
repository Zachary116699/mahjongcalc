# -*- coding: utf-8 -*-


def is_digit(str_1):
    """检测字符是否为数字"""
    try:
        float(str_1)
        return True
    except ValueError:
        return False


def is_chi(item):
    """检测item是否吃或顺"""
    if len(item) != 3:
        return False
    return item[0] + 2 == item[1] + 1 == item[2]


def is_pon(item):
    """检测item是否碰或刻"""
    if len(item) != 3:
        return False
    return item[0] == item[1] == item[2]


def is_m_kan(item):
    """检测item是否明杠"""
    if len(item) != 4:
        return False
    return item[0] == item[1] == item[2] == item[3]


def is_pair(item):
    """检测item是否雀头"""
    if len(item) != 2:
        return False
    return item[0] == item[1]


def is_a_kan(item):
    """检测item是否暗杠"""
    if len(item) != 5:
        return False
    return item[0] == item[1] == item[2] == item[3] == item[4]


def check_left_shun(tile, tiles_list):
    """检测tile是否和hand_tiles的牌形成左顺"""
    if (tile in tiles_list) and (tile + 1 in tiles_list) and (tile + 2 in tiles_list):
        return True
    return False


def check_ke(tile, tiles_list):
    """检测tile是否和tiles_list的牌形成刻子"""
    if tiles_list.count(tile) >= 3:
        return True
    return False


def check_pair(tile, tiles_list):
    """检测tile是否和tiles_list的牌形成对子"""
    if tiles_list.count(tile) >= 2:
        return True
    return False


def check_pmeld_1(tile, tiles_list):
    """检测tiles_list中是否形成tile在左侧的直接相连的pmeld"""
    if (tile in tiles_list) and (tile + 1 in tiles_list):
        return True
    return False


def check_pmeld_2(tile, tiles_list):
    """检测tiles_list中是否形成tile在左侧的直接相连的pmeld"""
    if tile in [9, 19, 32, 34, 36, 38, 40, 42, 44]:
        return False
    elif (tile in tiles_list) and (tile + 2 in tiles_list):
        return True
    else:
        return False


def get_pairs(hand_tiles):
    """抓雀头形成列表"""
    pair_tile = []
    for tile in hand_tiles:
        if check_pair(tile, hand_tiles):
            pair_tile.append(tile)
    pair_tile = list(set(pair_tile))
    pair_tile.sort()
    return pair_tile


def get_near_card(hand_tiles):
    """得到邻牌列表"""
    lin_tiles = []
    for tile in hand_tiles:
        if tile in [32, 34, 36, 38, 40, 42, 44]:
            lin_tiles.append(tile)
        elif tile in [1, 11, 21]:
            lin_tiles.append(tile)
            lin_tiles.append(tile + 1)
            lin_tiles.append(tile + 2)
        elif tile in [9, 19, 29]:
            lin_tiles.append(tile)
            lin_tiles.append(tile - 1)
            lin_tiles.append(tile - 2)
        elif tile in [8, 18, 28]:
            lin_tiles.append(tile + 1)
            lin_tiles.append(tile)
            lin_tiles.append(tile - 1)
            lin_tiles.append(tile - 2)
        elif tile in [2, 12, 22]:
            lin_tiles.append(tile - 1)
            lin_tiles.append(tile)
            lin_tiles.append(tile + 1)
            lin_tiles.append(tile + 2)
        else:
            lin_tiles.append(tile)
            lin_tiles.append(tile - 1)
            lin_tiles.append(tile + 1)
            lin_tiles.append(tile - 2)
            lin_tiles.append(tile + 2)
    lin_tiles = list(set(lin_tiles))
    lin_tiles.sort()
    return lin_tiles


def get_tiles_deck():
    """所有牌表的编码"""
    deck = [32, 34, 36, 38, 40, 42, 44]
    for i in range(1, 30):
        deck.append(i)
    deck.remove(10)
    deck.remove(20)
    deck.sort()
    return deck


def get_all_136_tiles():
    """获取136张牌的列表"""
    deck = get_tiles_deck()
    all_136_tiles = []
    for tile in deck:
        all_136_tiles.append(tile)
        all_136_tiles.append(tile)
        all_136_tiles.append(tile)
        all_136_tiles.append(tile)
    return all_136_tiles


def code_to_str(code):
    """编码转化成牌"""
    if 1 <= code <= 9:
        return str(code) + 'm'
    if 11 <= code <= 19:
        return str(code - 10) + 'p'
    if 21 <= code <= 29:
        return str(code - 20) + 's'
    if code >= 31:
        return str(int((code - 30) / 2)) + 'z'


def codes_to_str(tiles_list):
    """将牌列表转化为牌字符"""
    man = []
    pin = []
    sou = []
    zi = []
    for tile in tiles_list:
        if 1 <= tile <= 9:
            man.append(tile)
        if 11 <= tile <= 19:
            pin.append(tile - 10)
        if 21 <= tile <= 29:
            sou.append(tile - 20)
        if tile >= 31:
            zi.append(int((tile - 30) / 2))
    tiles_str = ''
    if len(man) != 0:
        for code in man:
            tiles_str += str(code)
        tiles_str += 'm'
    if len(pin) != 0:
        for code in pin:
            tiles_str += str(code)
        tiles_str += 'p'
    if len(sou) != 0:
        for code in sou:
            tiles_str += str(code)
        tiles_str += 's'
    if len(zi) != 0:
        for code in zi:
            tiles_str += str(code)
        tiles_str += 'z'
    return tiles_str


def str_to_code(a_str):
    code = 0
    if a_str.endswith('m'):
        code = int(a_str[0])
    if a_str.endswith('p'):
        code = int(a_str[0]) + 10
    if a_str.endswith('s'):
        code = int(a_str[0]) + 20
    if a_str.endswith('z'):
        code = int(a_str[0]) * 2 + 30
    return code
