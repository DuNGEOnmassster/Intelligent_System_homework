import random


def check_fitness(fitness: dict):
    return sum(fitness.values()) == 1.0


def get_pxi(fitness: dict):
    sum_fitness = sum(fitness.values())
    pxi = {}
    for i in fitness.keys():
        print(i)
        pxi[i] = float(str(fitness[i]/sum_fitness))
    print(sum(pxi.values()))


def get_init():
    pheno_type = {'s1', 's2', 's3', 's4'}
    fitness = {'s1':0.11, 's2':0.15, 's3':0.29, 's4':0.45, 's5':0.23}
    get_pxi(fitness)



if __name__ == "__main__":
    get_init()