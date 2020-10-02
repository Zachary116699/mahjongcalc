# -*- coding: utf-8 -*-
from shanten import Shanten
from tiles import Tile
import time


if __name__ == '__main__':
    print("Enter '!end' to end this program")
    print("Made by Zachary")
    print("1-9m：万子，1-9p：饼/筒, 1-9s：索/条，1-7z：东南西北白发中")
    print("鸣牌用空格隔开，暗杠用五个来表示，例：123m456s22z 11111z 234m")
    print("------" * 6)
    while True:
        tile_str = input("Input your tiles:\n")
        if tile_str == "!end":
            break
        start = time.time()
        your_tile = Tile(tile_str)
        if your_tile.error_state:
            print("[Error]:Please input right tiles.")
        else:
            hand_tiles = your_tile.hand_tiles
            rest_tiles = your_tile.rest_card
            shanten_data = Shanten.get_shanten_data(hand_tiles)
            Shanten.print_shanten_message(shanten_data, rest_tiles)
        print("[time_use:]", round(time.time() - start, 3), "s")
        print("------" * 6)
