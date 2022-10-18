import random


def check_fitness(fitness: dict):
    return sum(fitness.values()) == 1.0


def get_fitness():
    fitness = {'s1':0.11, 's2':0.15, 's3':0.29, 's4':0.45, 's5':0.23}
    return fitness


def get_pxi(fitness: dict):
    sum_fitness = sum(fitness.values())
    num_pheno = len(fitness)
    pxi = {}
    for i in fitness.keys():
        print(i)
        pxi[i] = float(str(fitness[i]/sum_fitness))
    print(f"{num_pheno} phenos in total with sum Pxi probability as {sum(pxi.values())}")
    return num_pheno, pxi


def get_select():
    pass


def get_cross():
    pass


def get_mutation():
    pass


def get_init():
    pheno_type = {'s1', 's2', 's3', 's4'}
    fitness = get_fitness()
    N, pxi = get_pxi(fitness)


def SGA(C, E, P0, M, end):
    gs = get_select()
    gc = get_cross()
    gm = get_mutation()
    if end:
        return None


if __name__ == "__main__":
    get_init()