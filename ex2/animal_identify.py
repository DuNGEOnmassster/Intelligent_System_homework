import os
import numpy as np
from rules import init_rules, Point
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Animal identify system")

    parser.add_argument("--extend", default=False,
                        help="whether use extend rules or not, default False")
    parser.add_argument("-i","--input", default="./dataset/test.txt",
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


def value2key(dict, value):
    return [k for k, v in dict.items() if v == value][0]


def get_pattern(text, args):
    datasets, emissions, targets = init_rules(args.extend)
    conditions = []
    init_split = text.split(sep="\n")
    for sentence in init_split:
        sen_list = sentence.split("：")
        if len(sen_list) == 2: # Capable to resist the distraction of useless message
            condition = sen_list[1].split("某动物")[-1]
            if condition in datasets.values(): # Avoid IndexError from fault condition
                rule = value2key(datasets, condition)
                # print(f"{rule}:{condition}")
                conditions.append(rule)

    return conditions


def search(conditions, args):
    datasets, emissions, targets = init_rules(args.extend)
    print(conditions)
    for item in emissions:
        print(f"rules:{item.rules} ➡️ result:{item.result}")
        # find the every combination to get results
        ...
        # if one result in target, return the target
        ...



def find_rules():
    args = parse_args()
    text, is_file = load_file(args.input)
    print(f"It is {is_file} that this is a file")
    conditions = get_pattern(text, args)
    search(conditions, args)



if __name__ == "__main__":
    find_rules()