from dataclasses import dataclass

@dataclass
class Point:
    rules: set
    result: int


def init_rules():
    datasets = { 1:"有奶", 2:"有毛发", 3:"有羽毛", 4:"会飞", 5:"会生蛋",
                6:"是哺乳动物", 7:"是鸟", 8:"有爪", 9:"有犬齿", 10:"目盯前方",
                11:"是食肉动物", 12:"有蹄", 13:"是有蹄动物", 14:"会反刍食物",
                15:"是偶蹄动物", 16:"黄褐色", 17:"有黑色条纹", 18:"是老虎",
                19:"有黑色斑点", 20:"是金钱豹", 21:"长腿", 22:"长脖子",
                23:"是长颈鹿", 24:"是白色", 25:"是斑马", 26:"不会飞", 27:"黑白色",
                28:"是鸵鸟", 29:"会游泳", 30:"是企鹅", 31:"善飞", 32:"不怕风浪",
                33:"是海燕", 34:"吃肉", 35:"有暗斑点",
                }
        
    emissions = [   Point(set([1]),6), Point(set([2]),6), Point(set([3]),7), Point(set([4, 5]),7), 
                    Point(set([6, 8, 9, 10]),11), Point(set([6, 34]),11), 
                    Point(set([6, 12]),13), Point(set([13, 14]),15), Point(set([11, 16, 17, 34]),18),
                    Point(set([11, 16, 19]),20), Point(set([13, 16, 21, 22, 35]),23), 
                    Point(set([13, 17, 24]),25), Point(set([7, 21, 22, 26, 27]),28),
                    Point(set([7, 26, 27, 29]),30), Point(set([7, 31, 32]),33),
                ]

    targets = [18, 20, 23, 25, 28, 30, 33]

    return datasets, emissions, targets

if __name__ == "__main__":
    pass
    
