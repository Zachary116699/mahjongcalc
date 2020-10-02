# -*- coding: utf-8 -*-
import utils
import time


class Tile(object):

    def __init__(self, tiles):
        self.tiles_str = tiles
        self.tiles_code = self._to_coding()
        self.mp_state = self._is_mp()
        self.tiles_code = self._trans_a_g()
        self.error_state = self._check_error()
        self.hand_tiles = self.tiles_code[0]
        self.tiles_sorted_str = self._to_str()
        self.rest_card = self._get_rest_card()

    def _is_mp(self):
        if len(self.tiles_code) >= 2:
            for i in range(1, len(self.tiles_code)):
                item = self.tiles_code[i]
                if not utils.is_a_kan(item):
                    return True
        return False

    def _split_tile_str(self):
        sp_list = self.tiles_str.split(" ")
        return sp_list

    @staticmethod
    def cut_tiles_str(tile_str):
        cut_list = []
        start = 0
        for i in range(0, len(tile_str)):
            if utils.is_digit(tile_str[i]):
                pass
            else:
                cut = tile_str[start:i + 1]
                cut_list.append(cut)
                start = i + 1
        return cut_list

    @staticmethod
    def to_coding(tiles_str_list):
        recoding_tiles = []
        for tiles_str in tiles_str_list:
            if tiles_str.endswith("m"):
                for i in range(0, len(tiles_str) - 1):
                    recoding_tiles.append(int(tiles_str[i]))
            if tiles_str.endswith("p"):
                for i in range(0, len(tiles_str) - 1):
                    recoding_tiles.append(int(tiles_str[i]) + 10)
            if tiles_str.endswith("s"):
                for i in range(0, len(tiles_str) - 1):
                    recoding_tiles.append(int(tiles_str[i]) + 20)
            if tiles_str.endswith("z"):
                for i in range(0, len(tiles_str) - 1):
                    recoding_tiles.append(int(tiles_str[i]) * 2 + 30)
        recoding_tiles.sort()
        return recoding_tiles

    def _to_coding(self):
        cut_list = self._split_tile_str()
        tiles_code = []
        for cut in cut_list:
            tiles_str_list = Tile.cut_tiles_str(cut)
            tile_code = Tile.to_coding(tiles_str_list)
            tiles_code.append(tile_code)
        return tiles_code

    def _check_mp(self):
        if len(self.tiles_code) >= 2:
            check_state = True
            for i in range(1, len(self.tiles_code)):
                item = self.tiles_code[i]
                if not (utils.is_chi(item) | utils.is_pon(item) | utils.is_m_kan(item) | utils.is_a_kan(item)):
                    check_state = False
            return check_state
        else:
            return True

    def _trans_a_g(self):
        code_list = self.tiles_code.copy()
        if len(code_list) >= 2:
            for i in range(1, len(code_list)):
                item = code_list[i]
                if utils.is_a_kan(item):
                    code_list[i].remove(item[0])
        return code_list

    def _check_tiles_nums(self):
        count_dir = {}
        all_code = []
        tiles_code = self.tiles_code
        for cut in tiles_code:
            for i in cut:
                all_code.append(i)
        keys = list(set(all_code))
        for k in keys:
            count_dir[k] = all_code.count(k)
        nums_list = list(count_dir.values())
        for num in nums_list:
            if num > 4:
                return False
        return True

    def _check_all_nums(self):
        tiles_len = len(self.tiles_code[0]) + 3 * (len(self.tiles_code) - 1)
        if tiles_len != 14:
            return False
        return True

    def _check_error(self):
        if self._check_tiles_nums() and self._check_all_nums() and self._check_mp():
            return False
        return True

    def _to_str(self):
        sort_str = ''
        for tiles in self.tiles_code:
            sort_str += utils.codes_to_str(tiles)
            sort_str += " "
        return sort_str

    def print_all_values(self):
        print("self.tiles_str =", self.tiles_str)
        print("self.tiles_sorted_str =", self.tiles_sorted_str)
        print("self.tiles_code =", self.tiles_code)
        print("self.hand_tiles =", self.hand_tiles)
        print("self.mp_state =", self.mp_state)
        print("self.error_state =", self.error_state)

    def _get_all_tiles(self):
        tiles_code = self.tiles_code
        all_tiles = []
        for item in tiles_code:
            for tile in item:
                all_tiles.append(tile)
        return all_tiles

    def _get_rest_card(self):
        all_tiles = self._get_all_tiles()
        tiles_deck = utils.get_all_136_tiles()
        if self.error_state:
            return None
        else:
            rest_card = Tile.remove_item(all_tiles, tiles_deck)
            return rest_card

    @staticmethod
    def remove_item(item, hand_tiles):
        copy_hand = hand_tiles.copy()
        for i in item:
            copy_hand.remove(i)
        return copy_hand


if __name__ == '__main__':
    start_time = time.time()
    a = Tile("1586411s4z 999m 7777s")
    a.print_all_values()
    print("time:", time.time() - start_time)
