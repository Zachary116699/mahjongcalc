# -*- coding: utf-8 -*-
from shanten import Shanten
import utils
import random
import time


def get_14_tiles():
    random_index = []
    while len(random_index) < 14:
        index = random.randint(0, 135)
        if index not in random_index:
            random_index.append(index)
    tiles = []
    deck = utils.get_all_136_tiles()
    for index in random_index:
        tiles.append(deck[index])
    tiles.sort()
    return tiles


def speed_test(test_num):
    test_list = []
    for i in range(0, test_num):
        hand_tiles = get_14_tiles()
        test_list.append(hand_tiles)
    time_list = []
    shanten_list = []
    print('------test start------')
    count = 1
    for hand_tiles in test_list:
        print(count)
        count += 1
        start = time.time()
        print("input:", utils.codes_to_str(hand_tiles))
        hand_shanten_data = Shanten.get_shanten_data(hand_tiles)
        shanten_list.append(hand_shanten_data["all_shanten"])
        rest_tiles = Shanten.remove_item(hand_tiles, utils.get_all_136_tiles())
        Shanten.print_shanten_message(hand_shanten_data, rest_tiles)
        time_use = time.time() - start
        time_list.append(time_use)
        print("time:", time_use)
        print('------')
    print('---test end---')
    all_time = 0
    for time_use in time_list:
        all_time += time_use
    time_average = all_time / len(time_list)
    shanten_sum = 0
    for shanten in shanten_list:
        shanten_sum += shanten
    shanten_average = shanten_sum / len(shanten_list)
    shanten_dir = {}
    shanten_set = list(set(shanten_list))
    shanten_set.sort()
    for k in shanten_set:
        shanten_dir[k] = shanten_list.count(k)
    print("test num:", test_num)
    print("use time:", all_time, "s")
    print("average time:", time_average, "s")
    print("average shanten:", shanten_average)
    for k in shanten_dir:
        print("shanten %d: %d times" % (k, shanten_dir[k]))


if __name__ == '__main__':
    test_times = int(input("Input the test num: "))
    speed_test(test_times)
    state = True
    while state:
        a = input("Enter end to end:")
        if a == "end":
            state = False
