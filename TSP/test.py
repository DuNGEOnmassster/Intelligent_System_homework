# 开发时间 2022/10/25 11:44
import numpy as np
import pandas as pd
import random
"""df = pd.DataFrame({"name": ["A001", "A002", "B001", "A001_K", "C002", "B001_K", "B001"],
                    "protein": [25, 28, 45, 22, 60, 40, 27],
                    "Qty": [85, 90, 75, 80, 30, 50, 30],
                    "rank": ["1st", "1st", "1st", "2nd", "1st", "1st", "2nd"]})

# 1 简单的条件筛选：单一条件筛选
data = df[df["name"] == "A001"]
data = data.loc[0, "name"]
print(data)

print([1,2]+[3,5])
roulette = pd.DataFrame({
            "gene": [],
            "start": [],
            "end": [],
        })
# print(roulette)
gene = [0,2,3]
start = 2.3
chosen_rate = 3.2
roulette.loc[len(roulette.index)] = [gene, start, start+chosen_rate]
print(roulette)"""

l1 = [2,4,3,1,5]
for i in range(5):
    if l1[i] == 2:
        l1[i] = 0
print(l1)

print(random.random())

chromosome = [str(x) for x in range(1, 10+1)]
print(chromosome)
for i in range(3):
    gene = random.sample(chromosome, 10)
    print(gene)
