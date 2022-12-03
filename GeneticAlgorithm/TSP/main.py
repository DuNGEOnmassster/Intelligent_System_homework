# 开发时间 2022/10/25 11:18
import random

from utils import *

input_dict = {
    "基因长度": 10,
    "进化基因数": 20,
    "交叉率": 0.6,
    "变异率": 0.002,
    "最优解": ["1", "4", "6", "5", "10", "9", "8", "7", "3", "2"],
    "进化次数": 500
}


def start_evolution(gene_len, gene_num, pc, pm, best_gene, evolve_epoch):
    genes = []
    chromosome = [str(x) for x in range(1, gene_len+1)] # 染色体库
    best_gene = Gene(best_gene)
    print("Theoretical best gene's distance:", 1/best_gene.adapt)
    # 随机创建基因
    for i in range(gene_num):
        gene = random.sample(chromosome, gene_len)
        gene = Gene(gene)
        genes.append(gene)
    q_space = QuestionSpace(pc, pm, genes)
    q_space.get_local_best_gene()
    found_best_gene = q_space.local_best_gene
    if q_space.local_best_gene.adapt >= best_gene.adapt:
        print("[INFO]-------->Best gene is sampled!")
        print("Best gene:", q_space.local_best_gene.gene, 1/q_space.local_best_gene.adapt)
    else:
        for i in range(evolve_epoch):
            q_space.select()
            q_space.cross()
            q_space.mutation()
            if q_space.local_best_gene.adapt >= best_gene.adapt:
                print(f"[INFO]-------->Find best gene {q_space.local_best_gene.gene}, distance:{1/q_space.local_best_gene.adapt} in epoch{i}")
                return
            else:
                if q_space.local_best_gene.adapt >= found_best_gene.adapt:
                    found_best_gene = q_space.local_best_gene
                print(f"[INFO]-------->Epoch{i}:local_best gene:{q_space.local_best_gene.gene},distance:{1/q_space.local_best_gene.adapt}")
        print(f"[INFO]-------->Evolution stops")
        print("找到的最优解：", found_best_gene.gene, 1/found_best_gene.adapt)


if __name__ == "__main__":
    start_evolution(input_dict["基因长度"], input_dict["进化基因数"], input_dict["交叉率"], input_dict["变异率"], input_dict["最优解"], input_dict["进化次数"])
