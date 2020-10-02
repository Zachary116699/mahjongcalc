# -*- coding: utf-8 -*-
import utils
from tiles import Tile


class Shanten(object):

    @staticmethod
    def remove_item(item, hand_tiles):
        """
        :param item: item to remove form hand_tiles
        :param hand_tiles: hand_tiles
        :return:
        """
        copy_hand = hand_tiles.copy()
        for i in item:
            copy_hand.remove(i)
        return copy_hand

    @staticmethod
    def get_meld(hand_tiles):
        """从手牌中抓面子"""
        meld_list = []
        hand_tiles_set = set(hand_tiles)
        for tile in hand_tiles_set:
            if utils.check_left_shun(tile, hand_tiles):
                meld_list.append([tile, tile + 1, tile + 2])
            if utils.check_ke(tile, hand_tiles):
                meld_list.append([tile, tile, tile])
        meld_list.sort()
        return meld_list

    @staticmethod
    def check_meld_joint(meld_list, item, hand_tiles):
        """判断item面子的独立性"""
        copy_hand = hand_tiles.copy()
        for meld in meld_list:
            copy_hand = Shanten.remove_item(meld, copy_hand)
        if utils.check_left_shun(item[0], copy_hand) and utils.is_chi(item):
            return True
        if utils.check_ke(item[0], copy_hand) and utils.is_pon(item):
            return True
        return False

    @staticmethod
    def divide_meld(hand_tiles):
        """从手牌中获得不同面子的分法,返回分法"""
        meld_list = Shanten.get_meld(hand_tiles)
        joint_meld_list = []
        for meld in meld_list:
            melds_list = [[meld]]
            done = True
            while done:
                a_list = []
                for item in meld_list:
                    for melds in melds_list:
                        copy_melds = melds.copy()
                        if Shanten.check_meld_joint(melds, item, hand_tiles):
                            copy_melds.append(item)
                            a_list.append(copy_melds)
                if len(a_list) == 0:
                    done = False
                else:
                    melds_list = a_list
            for melds in melds_list:
                melds.sort()
                joint_meld_list.append(melds)
        a_dir = {}
        for meld_divide in joint_meld_list:
            a_dir[str(meld_divide)] = meld_divide
        joint_meld_list = list(a_dir.values())
        joint_meld_list.sort()
        return joint_meld_list

    @staticmethod
    def first_divide(hand_tiles):
        """第一次分解手牌，获得包含面子的分法，返回分法列表"""
        joint_meld = Shanten.divide_meld(hand_tiles)
        if len(joint_meld) != 0:
            for joint_list in joint_meld:
                copy_hand = hand_tiles.copy()
                for meld in joint_list:
                    copy_hand = Shanten.remove_item(meld, copy_hand)
                joint_list.insert(0, copy_hand)
            list_len = []
            for joint in joint_meld:
                list_len.append(len(joint))
            max_len = max(list_len)
            copy_joint = joint_meld.copy()
            for joint in joint_meld:
                if len(joint) < max_len:
                    copy_joint.remove(joint)
            copy_joint.sort()
            return copy_joint
        else:
            return [[hand_tiles]]

    @staticmethod
    def get_pmeld(tiles_code):
        """获取剩余牌中的pmeld列表"""
        pmeld_list = []
        tiles = set(tiles_code)
        for tile in tiles:
            if utils.check_pmeld_1(tile, tiles_code):
                pmeld_list.append([tile, tile + 1])
            if utils.check_pmeld_2(tile, tiles_code):
                pmeld_list.append([tile, tile + 2])
            if utils.check_pair(tile, tiles_code):
                pmeld_list.append([tile, tile])
        pmeld_list.sort()
        return pmeld_list

    @staticmethod
    def check_pmeld_joint(pmeld_list, pmeld, tiles_code):
        """判断pmeld之间的独立性"""
        copy_code = tiles_code.copy()
        for a_pmeld in pmeld_list:
            copy_code = Shanten.remove_item(a_pmeld, copy_code)
        if utils.is_pair(pmeld):
            if utils.check_pair(pmeld[0], copy_code):
                return True
            return False
        if pmeld[0] in copy_code and pmeld[1] in copy_code:
            return True
        return False

    @staticmethod
    def divide_pmeld(divide_tiles):
        """获取包含pmeld和面子的长度为5的分法"""
        tiles_code = divide_tiles[0]
        len_limit = 5 - len(divide_tiles)
        pmeld_list = Shanten.get_pmeld(tiles_code)
        joint_pmeld_list = []
        for pmeld in pmeld_list:
            pmelds_list = [[pmeld]]
            done = True
            while done:
                a_list = []
                for item in pmeld_list:
                    for pmelds in pmelds_list:
                        copy_pmelds = pmelds.copy()
                        if Shanten.check_pmeld_joint(pmelds, item, tiles_code):
                            copy_pmelds.append(item)
                            if len(copy_pmelds) > len_limit:
                                break
                            else:
                                a_list.append(copy_pmelds)
                if len(a_list) == 0:
                    done = False
                else:
                    pmelds_list = a_list
            for pmelds in pmelds_list:
                pmelds.sort()
                joint_pmeld_list.append(pmelds)

        a_dir = {}
        for pmeld_divide in joint_pmeld_list:
            pmeld_divide.sort()
            a_dir[str(pmeld_divide)] = pmeld_divide
        joint_pmeld_list = list(a_dir.values())
        return joint_pmeld_list

    @staticmethod
    def second_divide(hand_tiles):
        """第二次分解手牌,返回分法列表"""
        divide_tiles_list = Shanten.first_divide(hand_tiles)
        divide_method = []
        for divide_tiles in divide_tiles_list:
            joint_pmelds_list = Shanten.divide_pmeld(divide_tiles)
            for joint_pmelds in joint_pmelds_list:
                copy_divide = divide_tiles.copy()
                for pmeld in joint_pmelds:
                    copy_divide[0] = Shanten.remove_item(pmeld, copy_divide[0])
                    copy_divide.append(pmeld)
                    if len(copy_divide) == (len(hand_tiles) - 2) / 3 + 1:
                        break
                divide_method.append(copy_divide)
        if len(divide_method) == 0:
            for divide_tiles in divide_tiles_list:
                divide_method.append(divide_tiles)
        return divide_method

    @staticmethod
    def shanten_calc(divide_method):
        """计算分法的向听数，返回向听数"""
        pmeld_num = 0
        pair_exist = False
        pmeld_exist_in_rest = False
        tiles_len = 0
        for item in divide_method:
            tiles_len += len(item)
        meld_num = int((14 - tiles_len) / 3)
        for i in range(1, len(divide_method)):
            item = divide_method[i]
            if utils.is_chi(item) or utils.is_pon(item):
                meld_num += 1
            elif utils.is_pair(item):
                pmeld_num += 1
                pair_exist = True
            else:
                pmeld_num += 1
        for tile in divide_method[0]:
            if utils.check_pair(tile, divide_method[0]):
                pair_exist = True
                pmeld_exist_in_rest = True
            if utils.check_pmeld_1(tile, divide_method[0]) or utils.check_pmeld_2(tile, divide_method[0]):
                pmeld_exist_in_rest = True
        shanten = 8 - 2 * meld_num - pmeld_num
        if pair_exist and pmeld_exist_in_rest:
            shanten -= 1
        return shanten

    @staticmethod
    def get_shanten(divide_method_list):
        """获取牌面的向听数"""
        shanten_list = []
        for divide_method in divide_method_list:
            shanten = Shanten.shanten_calc(divide_method)
            shanten_list.append(shanten)
        shanten_min = min(shanten_list)
        return shanten_min

    @staticmethod
    def get_wait_list(to_discard_list, hand_tiles, hand_shanten):
        """获取出牌推荐列表数据"""
        test_tiles = utils.get_near_card(hand_tiles)
        to_wait_list = []
        for discard in to_discard_list:
            copy_hand = hand_tiles.copy()
            copy_hand.remove(discard)
            for tile in test_tiles:
                copy_hand_1 = copy_hand.copy()
                copy_hand_1.append(tile)
                copy_hand_1.sort()
                copy_divide_method = Shanten.second_divide(copy_hand_1)
                copy_shanten = Shanten.get_shanten(copy_divide_method)
                if hand_shanten > copy_shanten:
                    to_wait_list.append([discard, tile])
        return to_wait_list

    @staticmethod
    def get_wait_dir(to_wait_list):
        """处理出牌推荐列表数据，返回出牌推荐的字典"""
        to_wait_dir = {}
        for item in to_wait_list:
            tile_str = utils.code_to_str(item[0])
            to_wait_dir[tile_str] = []
        for item in to_wait_list:
            tile_str = utils.code_to_str(item[0])
            to_wait_dir[tile_str].append(item[1])
        return to_wait_dir

    @staticmethod
    def scan_normal_situation(hand_tiles):
        """获取正常胡法的向听数和出牌推荐，返回字典"""
        divide_method_list = Shanten.second_divide(hand_tiles)
        hand_shanten = Shanten.get_shanten(divide_method_list)
        to_discard_list = list(set(hand_tiles))
        to_discard_list.sort()
        to_wait_list = Shanten.get_wait_list(to_discard_list, hand_tiles, hand_shanten)
        to_wait_dir = Shanten.get_wait_dir(to_wait_list)
        return {"shanten": hand_shanten, "discard": to_wait_dir}

    @staticmethod
    def get_shanten_of_kokushi(hand_tiles):
        """计算牌面距离国士无双的向听数"""
        hand_tiles_set = set(hand_tiles)
        kokushi_tiles = [1, 9, 11, 19, 21, 29, 32, 34, 36, 38, 40, 42, 44]
        kokushi_tiles_in_hand = []
        for tile in hand_tiles_set:
            if tile in kokushi_tiles:
                kokushi_tiles_in_hand.append(tile)
        kokushi_shanten = 13 - len(kokushi_tiles_in_hand)
        other_tiles = Shanten.remove_item(kokushi_tiles_in_hand, hand_tiles)
        for tile in other_tiles:
            if tile in kokushi_tiles:
                kokushi_shanten -= 1
                break
        return kokushi_shanten

    @staticmethod
    def scan_kokushi(hand_tiles):
        """获取国士无双的向听数和出牌推荐，返回字典"""
        kokushi_shanten = Shanten.get_shanten_of_kokushi(hand_tiles)
        kokushi_tiles = [1, 9, 11, 19, 21, 29, 32, 34, 36, 38, 40, 42, 44]
        to_discard_list = list(set(hand_tiles))
        to_discard_list.sort()

        to_wait_list = []
        for discard in to_discard_list:
            copy_hand = hand_tiles.copy()
            copy_hand.remove(discard)
            for tile in kokushi_tiles:
                copy_hand_1 = copy_hand.copy()
                copy_hand_1.append(tile)
                copy_hand_1.sort()
                if Shanten.get_shanten_of_kokushi(copy_hand_1) < kokushi_shanten:
                    to_wait_list.append([discard, tile])
        to_wait_dir = Shanten.get_wait_dir(to_wait_list)
        return {"shanten": kokushi_shanten, "discard": to_wait_dir}

    @staticmethod
    def get_shanten_of_chiitoitsu(hand_tiles):
        """计算牌面距离七对子的向听数"""
        hand_tiles_set = set(hand_tiles)
        pair_count = 0
        for tile in hand_tiles_set:
            if utils.check_pair(tile, hand_tiles):
                pair_count += 1
        if pair_count == 7:
            chiitoitsu_shanten = -1
        else:
            chiitoitsu_shanten = 6 - pair_count
        return chiitoitsu_shanten

    @staticmethod
    def scan_chiitoitsu(hand_tiles):
        """获取七对子的向听数和出牌推荐，返回字典"""
        hand_shanten = Shanten.get_shanten_of_chiitoitsu(hand_tiles)
        hand_tiles_set = set(hand_tiles)
        to_discard_list = list(set(hand_tiles))
        to_discard_list.sort()

        to_wait_list = []
        for discard in to_discard_list:
            copy_hand = hand_tiles.copy()
            copy_hand.remove(discard)
            for tile in hand_tiles_set:
                copy_hand_1 = copy_hand.copy()
                copy_hand_1.append(tile)
                copy_hand_1.sort()
                if Shanten.get_shanten_of_chiitoitsu(copy_hand_1) < hand_shanten:
                    to_wait_list.append([discard, tile])

        to_wait_dir = Shanten.get_wait_dir(to_wait_list)
        return {"shanten": hand_shanten, "discard": to_wait_dir}

    @staticmethod
    def get_shanten_data(hand_tiles):
        """获取包含国士和七对子的向听数和出牌推荐，返回对应字典"""
        normal_data = Shanten.scan_normal_situation(hand_tiles)
        discard_dir = normal_data["discard"].copy()
        shanten_list = [normal_data["shanten"]]
        if len(hand_tiles) == 14:
            kokushi_data = Shanten.scan_kokushi(hand_tiles)
            chiitoitsu_data = Shanten.scan_chiitoitsu(hand_tiles)
            shanten_list.append(kokushi_data["shanten"])
            shanten_list.append(chiitoitsu_data["shanten"])
            if kokushi_data["shanten"] < chiitoitsu_data["shanten"]:
                discard_dir_1 = kokushi_data["discard"]
                min_shanten = kokushi_data["shanten"]
            elif kokushi_data["shanten"] > chiitoitsu_data["shanten"]:
                discard_dir_1 = chiitoitsu_data["discard"]
                min_shanten = chiitoitsu_data["shanten"]
            else:
                discard_dir_1 = Shanten.combine(kokushi_data["discard"], chiitoitsu_data["discard"])
                min_shanten = kokushi_data["shanten"]
            if min_shanten == normal_data["shanten"]:
                discard_dir = Shanten.combine(discard_dir_1, discard_dir)
            if min_shanten < normal_data["shanten"]:
                discard_dir = discard_dir_1
        shanten_data = {
            "all_shanten": min(shanten_list),
            "normal_shanten": normal_data["shanten"],
            "discard": discard_dir
        }
        return shanten_data

    @staticmethod
    def combine(dir_1, dir_2):
        """用于合并出牌推荐的字典，返回合并后的字典"""
        new_dir = {}
        for key in dir_1:
            new_dir[key] = []
        for key in dir_2:
            new_dir[key] = []
        for key in dir_1:
            for ele in dir_1[key]:
                new_dir[key].append(ele)
        for key in dir_2:
            for ele in dir_2[key]:
                new_dir[key].append(ele)
        for key in new_dir:
            new_dir[key] = list(set(new_dir[key]))
            new_dir[key].sort()
        return new_dir

    @staticmethod
    def count_tiles(shanten_data, rest_of_136_tiles):
        """计算出牌的待牌数量并排序"""
        discard_dir = shanten_data["discard"]
        keys = list(discard_dir.keys())
        count_keys = []
        for k in keys:
            count = 0
            for tile in discard_dir[k]:
                count += rest_of_136_tiles.count(tile)
            count_keys.append([count, k])
        count_keys.sort()
        count_keys.reverse()
        return count_keys

    @staticmethod
    def print_shanten_message(shanten_data, rest_of_136_tiles):
        """
        输出向听字典中的信息
        :param shanten_data: 计算得到的向听字典
        :param rest_of_136_tiles: 去除手牌后剩下的牌
        :return:None
        """
        if shanten_data["all_shanten"] == -1:
            print("You win.")
        else:
            if shanten_data["all_shanten"] == 0:
                print("Tenpai.")
            else:
                print("shanten include kokushi and chiitoitsu:", shanten_data["all_shanten"])
                print("shanten without kokushi and chiitoitsu:", shanten_data["normal_shanten"])
            keys = Shanten.count_tiles(shanten_data, rest_of_136_tiles)
            print("[How to discard]:")
            for key_count in keys:
                k = key_count[1]
                a = "discard: %s, to wait:[" % (k,)
                a += utils.codes_to_str(shanten_data["discard"][k])
                a += '] ' + str(key_count[0]) + ' tiles'
                print(a)


if __name__ == '__main__':
    import time
    start = time.time()
    strdata = '234m68m13579p1s 789s'
    print("input:", strdata)
    tile_1 = Tile(strdata)
    hand_tiles_1 = tile_1.hand_tiles
    print("sorted:", tile_1.tiles_sorted_str)
    print("hand_tiles:", hand_tiles_1)
    print("------")
    shanten_data_1 = Shanten.get_shanten_data(hand_tiles_1)
    rest_of_136_tiles_1 = tile_1.rest_card
    Shanten.print_shanten_message(shanten_data_1, rest_of_136_tiles_1)
    print("------")
    print('time:', time.time() - start)
