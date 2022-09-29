import numpy as np
import os

def find_rules(txt_or_txt_file):
    if os.path.exists(txt_or_txt_file):
        file = open(txt_or_txt_file, 'r')
        readfile = file.read()
    else:
        readfile = txt_or_txt_file

    # spilt and find rules

    rule_list = []
    bigger_list = readfile.split("若某动物")
    for big_name in bigger_list:
        small_name = big_name.split("，则它")
        # print(small_name)
        flag = 0
        key = None
        value = None

        for rule in small_name:
            if flag == 2:
                value = rule[:-1]
                rule_list.append({key:value})
                flag = 0

            elif flag == 1:
                key = rule
                flag = flag + 1

            else:
                flag = flag + 1
    
    print(rule_list)



if __name__ == "__main__":
    data_process_list = []
    data_result_list = []
    list_data = []
    dict_input = {}

    txt = """
      （1）若某动物有奶，则它是哺乳动物。
      
      （2）若某动物有毛发，则它是哺乳动物。
      
      （3）若某动物有羽毛，则它是鸟。
      
      （4）若某动物会飞且生蛋，则它是鸟。
      
      （5）若某动物是哺乳动物且有爪且有犬齿且目盯前方，则它是食肉动物。
      
      （6）若某动物是哺乳动物且吃肉，则它是食肉动物。
      
      （7）若某动物是哺乳动物且有蹄，则它是有蹄动物。
      
      （8）若某动物是有蹄动物且反刍食物，则它是偶蹄动物。
      
      （9）若某动物是食肉动物且黄褐色且有黑色条纹，则它是老虎。
      
      （10）若某动物是食肉动物且黄褐色且有黑色斑点，则它是金钱豹。
      
      （11）若某动物是有蹄动物且长腿且长脖子且黄褐色且有暗斑点，则它是长颈鹿。
      
      （12）若某动物是有蹄动物且白色且有黑色条纹，则它是斑马。
      
      （13）若某动物是鸟且不会飞且长腿且长脖子且黑白色，则它是驼鸟。
      
      （14）若某动物是鸟且不会飞且会游泳且黑白色，则它是企鹅。
      
      （15）若某动物是鸟且善飞且不怕风浪，则它是海燕。
    """
    find_rules(txt)

