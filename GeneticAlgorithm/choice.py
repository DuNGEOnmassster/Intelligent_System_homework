import random
import argparse
import math


def parse_args():
    parser = argparse.ArgumentParser(description="Solving Equations with Genetic Algorithms")
    
    parser.add_argument("--func", type=str ,default='pow(x,2)',
                        help="eqution to be solved")
    parser.add_argument("--num", type=int, default=4,
                        help="population size")
    parser.add_argument("--binary_encode", type=bool, default=True,
                        help="whether use binary encode, default with True")

    return parser.parse_args()


def check_fitness(fitness: dict):
    return sum(fitness.values()) == 1.0


def get_row_number(n: int):
    row_number = {}
    for i in range(n):
        key = "s" + str(i+1)
        row_number[key] = random.randint(1,31)
    return row_number


def get_encode(row_number: dict, args):
    gene = row_number.copy()
    for item in gene.keys():
        if args.binary_encode:
            gene[item] = bin(gene[item])
        else:
            break
    return gene


def get_fitness(gene: dict, args):
    fitness = gene.copy()
    for item in fitness.keys():
        if args.binary_encode:
            fitness[item] = pow(int(fitness[item], 2), 2)
        else:
            fitness[item] = pow(fitness[item],2)
    return fitness


def get_pxi(fitness: dict):
    sum_fitness = sum(fitness.values())
    num_pheno = len(fitness)
    pxi = {}
    for i in fitness.keys():
        # print(i)
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
    args = parse_args()
    row_number = get_row_number(args.num)
    print(row_number)
    gene = get_encode(row_number, args)
    print(gene)
    fitness = get_fitness(gene, args)
    print(fitness)
    N, pxi = get_pxi(fitness)
    

def SGA(C, E, P0, M, end):
    gs = get_select()
    gc = get_cross()
    gm = get_mutation()
    if end:
        return None


if __name__ == "__main__":
    get_init()