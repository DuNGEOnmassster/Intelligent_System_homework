from json import load
import os
from turtle import pd
import numpy as np
from itertools import combinations
from rules import init_rules, Point
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Animal identify system")

    parser.add_argument("-t","--test", default="./dataset/test.txt",
                        help="test data sentense for identification")
    parser.add_argument("--extend", default=False,
                        help="whether use extend rules or not, default False")
    parser.add_argument("--extend_rules", default="./dataset/extend_rules.txt",
                        help="input file to extend rules.")

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


def get_test_pattern(text, args):
    if args.extend:
        print("Use extend rules")
        rules_text,_ = load_file(args.extend_rules)
        datasets, emissions, targets = get_rule_pattern(rules_text)
    else:
        datasets, emissions, targets = init_rules()
    
    conditions = []
    init_split = text.split(sep="\n")
    for sentence in init_split:
        sen_list = sentence.split("：")
        # Capable to resist the distraction of useless message
        if len(sen_list) == 2: 
            condition = sen_list[1].split("某动物")[-1]
            # Avoid IndexError from fault condition
            if condition in datasets.values(): 
                rule = value2key(datasets, condition)
                # print(f"{rule}:{condition}")
                conditions.append(rule)

    return conditions


def get_rule_pattern(text):
    datasets, emissions, targets = init_rules()
    init_split = text.split(sep="\n")
    for sentence in init_split:
        sen_list = sentence.split(sep="：")
        # Capable to resist the distraction of useless message
        if len(sen_list) == 2: 
            result = sen_list[0].split(sep="）")[-1]
            condition_list = sen_list[1][:-1].split(sep="，")
            # print(f"{condition_list} result={result}")

            # Attend new conditions and results into datasets
            for item in condition_list:
                if item not in datasets.values():
                    # print(f"{item} not in datasets")
                    datasets[len(datasets)+1] = item
            if result not in datasets.values():
                # print(f"{result} not in datasets")
                datasets[len(datasets)+1] = result
                # Attend new result into targets
                targets.append(value2key(datasets, result))

            # Attend new emission into emissions
            condition_number = []
            for condition in condition_list:
                condition_number.append(value2key(datasets, condition))
            emissions.append(Point(set(condition_number),value2key(datasets, result)))

    return datasets, emissions, targets


def get_permutations(conditions):
    perm = []
    if len(conditions) == 1:
        return [conditions]
    for i in range(len(conditions)):
        s = conditions[:i] + conditions[i+1:]
        p = get_permutations(s)
        for x in p:
            perm.append(conditions[i:i+1]+x)

    return perm


def get_combinations(conditions):
    comb = []
    if len(conditions) == 1:
        return [conditions]
    for i in range(1,len(conditions)+1):
        for tuples in combinations((conditions), i):
            comb.append({c for c in tuples})

    return comb


def search(conditions, args):
    if args.extend:
        print("Search in extend rules")
        rules_text,_ = load_file(args.extend_rules)
        datasets, emissions, targets = get_rule_pattern(rules_text)
    else:
        datasets, emissions, targets = init_rules()
    print(f"conditions = {conditions}")
    # find the every condition combination to get results, put result as new condition
    comb = get_combinations(conditions)
    print(f"combinations = {comb}")

    visited = []
    cnt = 0
    while True:
        for item in emissions:
            # print(f"rules:{item.rules} ➡️ result:{item.result}")
            if item.rules in comb and item.rules not in visited:
                print(f"{item.rules} result = {item.result}")
                # if one result in target, return the target
                if item.result in targets:
                    print(f"Find Target: {datasets[item.result]}")
                    return item.result
                    
                # else regard result as another condition and restart
                else:
                    conditions.append(item.result)
                    visited.append(item.rules)
                    comb = get_combinations(conditions)
                    print(f"new conditions is {conditions}")
                    # import pdb; pdb.set_trace()
            else:
                cnt = cnt + 1
    

def find_rules():
    args = parse_args()
    text, is_file = load_file(args.test)
    print(f"It is {is_file} that this is a file")
    conditions = get_test_pattern(text, args)
    search(conditions, args)


if __name__ == "__main__":
    find_rules()