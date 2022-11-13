# 开发时间 2022/10/25 11:18
import numpy as np
import random
import math
import pandas as pd

map_dict = {
    '1': (87, 7),
    '2': (91, 38),
    '3': (83, 46),
    '4': (71, 44),
    '5': (64, 60),
    '6': (68, 58),
    '7': (83, 69),
    '8': (87, 76),
    '9': (74, 78),
    '10': (71, 71)
}


def get_distance(c1, c2):
    l1 = c1[1]-c2[1]
    l2 = c1[0]-c2[0]
    distance = math.sqrt(l1**2 + l2**2)
    return distance


def cross_two_gene(g1, g2, gene_len):
    seed = np.random.randint(0, gene_len, 2)
    seed.sort()
    start_seed = seed[0]
    end_seed = seed[1]

    new_g1 = g1[start_seed:end_seed]
    ooc1 = set(new_g1)
    for i in range(gene_len):
        if g2[i] not in ooc1:
            new_g1.append(g2[i])
    new_g2 = g2[start_seed:end_seed]
    ooc2 = set(new_g2)
    for i in range(gene_len):
        if g1[i] not in ooc2:
            new_g2.append(g1[i])
    return Gene(new_g1), Gene(new_g2)


class Gene:
    def __init__(self, gene_list):
        self.gene = gene_list
        self.gene_len = len(gene_list)
        self.adapt = 0
        self.cal_adapt()

    def cal_adapt(self):
        ada_sum = 0
        for i in range(self.gene_len):
            c1 = map_dict[self.gene[i]]
            c2 = map_dict[self.gene[i+1]] if i+1 < self.gene_len else map_dict[self.gene[0]]
            distance = get_distance(c1, c2)
            ada_sum += distance
        self.adapt = 1/ada_sum


class QuestionSpace:
    def __init__(self, pc, pm, genes):
        self.genes = genes
        self.genes_num = len(genes)
        self.p_cross = pc
        self.p_mutation = pm
        self.local_best_gene: Gene = None
        self.get_local_best_gene()

    def get_local_best_gene(self):
        local_best_ada = 0
        local_best_gene = None
        for gene in self.genes:
            if gene.adapt > local_best_ada:
                local_best_gene = gene
        self.local_best_gene = local_best_gene

    def select(self):
        ada_sum = 0 # 总适应度
        for gene in self.genes:
            ada_sum += gene.adapt
        # 设置轮盘
        roulette = pd.DataFrame(
            columns=["gene", "start", "end"]
        )
        start = 0
        for gene in self.genes:
            chosen_rate = gene.adapt / ada_sum
            roulette.loc[len(roulette.index)] = [gene, start, start+chosen_rate]
            start += chosen_rate

        # 开始选择
        new_gene_list = []
        for i in range(self.genes_num):
            randseed = random.random()
            new_gene = roulette[(roulette["start"] <= randseed) & (roulette["end"] >= randseed)]
            new_gene = new_gene.values.tolist()
            new_gene_list.append(new_gene[0][0])
        self.genes = new_gene_list
        # print("[INFO]-------->Selected genes:", )

    def cross(self):
        pair_num = int((self.genes_num*self.p_cross)//2)
        for i in range(pair_num):
            g1 = self.genes[i*2]
            g2 = self.genes[i*2+1]
            self.genes[i*2], self.genes[i*2+1] = cross_two_gene(g1.gene, g2.gene, g1.gene_len)

    def mutation(self):
        num_of_mut = math.floor(self.p_mutation * self.genes[0].gene_len * self.genes_num)
        for i in range(num_of_mut):
            gene = self.genes[random.randint(0, self.genes_num)]
            for index in range(gene.gene_len-1):
                seed = random.random()
                if seed < self.p_mutation:
                    t = gene[index]
                    gene[index] = gene[index+1]
                    gene[index+1] = t
                    break
        # 更新所有基因的适应度
        for gene in self.genes:
            gene.cal_adapt()
        # 获得当前最优解
        self.get_local_best_gene()
