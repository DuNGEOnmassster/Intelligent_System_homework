from utils.rules import init_rules
import os

def check_origin_rules():
    datasets, emissions, targets = init_rules()

    # Check the legitimacy of targets
    for target in targets:
        if datasets[target] == None:
            return False

    # Check the legitimacy of emissions
    for emission in emissions:
        if datasets[emission.result] == None:
            return False
    
    return True


def check_extend_rules(txt_or_txt_file):
    # Check the legitimacy of file rules
    if os.path.exists(txt_or_txt_file):
        file = open(txt_or_txt_file, 'r')
        readfile = file.read()
        for rule in readfile.split(sep="\n"):
            if "：" in rule:
                rule_segment = rule.split(sep="：")
                if len(rule_segment) == 2:
                    if rule_segment[0].split(sep="）")[1] == None or rule_segment[1] == None:
                        return False
                else:
                    return False
            else:
                return False
        print("Legal extend file rules")
        return True
    # Check the legitimacy of text rules
    else:
        if "：" in txt_or_txt_file:
            rule_segment = txt_or_txt_file.split(sep="：")
            if len(rule_segment) == 2:
                if rule_segment[0].split(sep="）")[1] == None or rule_segment[1] == None:
                    return False
            else:
                return False
            print("Legal extend text rules")
            return True
        else:
            return False


if __name__ == "__main__":
    check_origin_rules()
    extend_path = "./dataset/extend_rules.txt"
    extend_text = "（3）犀牛：有毛发，有奶，鼻子上有角，褐色，皮糙肉后，皮糙肉厚，有蹄；"
    check_extend_rules(extend_path)
    check_extend_rules(extend_text)