#!/usr/bin/python3.7

import pickle
import pyperclip
import os
import sys
from pyvirtualdisplay import Display
from selenium import webdriver


def load_solves():
    with open("solves.pkl", "wb") as f:
        pickle.dump([],f)


    with open("solves.pkl", "rb") as f:
        data = pickle.load(f)
    print(data)
def parse_to_algs_time(stats, exe_moves):

    mistake_sec = -1
    stats[0]["time"] = 0.0
    for i in range (1,len(stats)):
        stats[i]["time"] = exe_moves[stats[i]["count"] - 1][1]
        if "diff_moves" in stats[i]:
            current = stats[i]["time"]
            first = stats[i - stats[i]["diff_moves"]]["time"]
            time_exe = round(current - stats[1 + i - stats[i]["diff_moves"]]["time"], 2)
            time_alg = round(current - first ,2)
            time_pause = round(time_alg - time_exe, 2)
            alg_str = []
            for j in range(stats[i - stats[i]["diff_moves"]]["count"] + 1, i + 1):
                # print(stats[j]["move"])
                alg_str.append(stats[j]["move"])
            alg_str = " ".join(alg_str)
            stats[i]["alg_stats"] = {"time_alg" : time_alg, "exe" : time_exe, "pause" :  time_pause, "alg_str" :  alg_str}
            stats[i]["alg_stats"]["comment"]  = stats[i]["comment"]
            stats[i]["alg_stats"]["piece"] = stats[i]["piece"]
        if "mistake" in stats[i]["comment"]:
            mistake_sec = exe_moves[stats[i]["count"]][1]
    algs = []
    for move in stats:
        if "diff_moves" in move:
            if "mistake" not in move["comment"]:
                algs.append([move["alg_stats"]])

    return (algs, mistake_sec)


def main():
    with open("solves.pkl", "rb") as f:
        data = pickle.load(f)
        print(*data[-1]["algs_time"], sep="\n")

    pyperclip.copy(sys.argv[1])

    # stats = data[0]
        # exe_moves = data[1]

        # print(*exe_moves, sep="\n")
    # algs, mistake_sec = parse_to_algs_time(stats, exe_moves)
    # print(*algs, sep="\n")
    # for alg in algs:
    #     print(alg)
    # print(mistake_sec)


if __name__ == '__main__':
  main()