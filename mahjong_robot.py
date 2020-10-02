# -*- coding: utf-8 -*-
from tiles import Tile
from shanten import Shanten
import utils


hand_str = input("input your hand tiles: ")
your_tile = Tile(hand_str)
your_shanten = 8
error_state = your_tile.error_state
rest_tiles = your_tile.rest_card
if error_state:
    print("please input right 14 tiles")
hand_tiles = your_tile.hand_tiles
discard_list = []
while not error_state:
    shanten_data = Shanten.get_shanten_data(hand_tiles)
    your_shanten = shanten_data["all_shanten"]
    if your_shanten == -1:
        print("win")
        break
    print("hand_str:", utils.codes_to_str(hand_tiles))
    Shanten.print_shanten_message(shanten_data, rest_tiles)
    print("------")
    discard = input("to discard: ")
    discard_code = utils.str_to_code(discard)
    hand_tiles.remove(discard_code)
    discard_list.append(discard_code)
    remove_tiles = input("to remove form deck: ")
    remove_card = Tile(remove_tiles).hand_tiles
    rest_tiles = Shanten.remove_item(remove_card, rest_tiles)
    in_tile = input("in: ")
    in_tile = utils.str_to_code(in_tile)
    hand_tiles.append(in_tile)
    hand_tiles.sort()
    print('------')


