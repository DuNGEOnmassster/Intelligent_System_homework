# 开发时间 2022/9/21 11:31
import numpy as np
import common

map = np.array([[2, 3, 8], [0, 1, 4], [7, 6, 5]])
dict = {
    "a":[[2,4],[1,5]],
    "b":1
}
dict["c"] = 2
dict["a"].insert(2,5)
print(dict["a"])