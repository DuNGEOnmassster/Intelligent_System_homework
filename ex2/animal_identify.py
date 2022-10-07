import os
import numpy as np
from rules import init_rules, Point
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Animal identify system")

    parser.add_argument("-d","--dataset", default="./dataset/test.txt",
                        help="input data file")
    parser.add_argument("--extend", default=False,
                        help="whether use extend rules or not, default False")
    parser.add_argument("-i","--input", default="是鸟且不会飞且会游泳且黑白色",
                        help="input test sentense for identification")

    return parser.parse_args()


def load_file(txt_or_txt_file):
    if os.path.exists(txt_or_txt_file):
        file = open(txt_or_txt_file, 'r')
        readfile = file.read()
        is_file = True
    else:
        readfile = txt_or_txt_file
        is_file = False
    
    return readfile, is_file


def get_pattern(text, args):
    datasets, emissions, targets = init_rules(args.extend)
    init_split = text.split(sep="\n")
    for sentence in init_split:
        sen_list = sentence.split("若某动物")
        if len(sen_list) == 2:
            item = sen_list[1].split(sep="，则它")
            key = item[0]
            value = item[1][:-1]
            print(f"{key}:{value}")
            


def find_rules():
    args = parse_args()
    text, is_file = load_file(args.dataset)
    print(f"It is {is_file} that this is a file")
    get_pattern(text, args)


if __name__ == "__main__":
    find_rules()