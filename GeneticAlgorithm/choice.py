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

    parser.add_argument("--encode_bits", type=int, default=5,
                        help="declear the length of encode bits")
    parser.add_argument("--max_cross_bits", type=int, default=3,
                        help="declear the maximum of changing bits in a crossing epoch")
    parser.add_argument("--single_mutation_bits", type=int, default=1,
                        help="declear the maximum of mutation bits in a single gene")
    parser.add_argument("--max_mutation_bits", type=int, default=3,
                        help="declear the maximum of total mutation bits in a mutation epoch")

    return parser.parse_args()


def check_fitness(fitness: dict):
    return sum(fitness.values()) == 1.0


def get_row_number(args):
    row_number = {}
    for i in range(args.num):
        key = "s" + str(i+1)
        row_number[key] = random.randint(1, pow(2, args.encode_bits)-1)
    return row_number


def get_encode(row_number: dict, args):
    gene = row_number.copy()
    for item in gene.keys():
        if args.binary_encode:
            gene[item] = bin(gene[item])   
            if len(gene[item]) < args.encode_bits + 2:
                zero_filling = "0" * (args.encode_bits + 2 - len(gene[item]))  
                gene[item] = "0b"+zero_filling+gene[item][2:] 
                print(f"warning! new is {gene[item]}")   
        else:
            break
    return gene


def get_decode(gene: dict, args):
    row_number = gene.copy()
    for item in row_number.keys():
        if args.binary_encode:
            row_number[item] = int(gene[item], 2)
        else:
            break
    return row_number


def get_fitness(gene: dict, args):
    fitness = gene.copy()
    for item in fitness.keys():
        if args.binary_encode:
            fitness[item] = pow(int(fitness[item], 2), 2)
        else:
            fitness[item] = pow(fitness[item],2)
    return fitness


def get_pxi(fitness: dict, args):
    sum_fitness = sum(fitness.values())
    pxi = {}
    cumulative_pxi = {}
    cnt = 0
    for i in fitness.keys():
        pxi[i] = float(str(fitness[i]/sum_fitness))
        cumulative_pxi[i] = pxi[i] + cnt
        cnt = cnt + pxi[i]
    print(f"{args.num} phenos in total with sum Pxi probability as {sum(pxi.values())}")
    return pxi, cumulative_pxi


def get_select(gene: dict, cumulative_pxi: dict):
    gs = cumulative_pxi.copy()
    cumu_name = [i for i in cumulative_pxi.keys()]
    cumu_list = [i for i in cumulative_pxi.values()]
    for item in gs.keys():
        rid = random.uniform(0,1)
        cupxi = 0
        while rid > cumu_list[cupxi]:
            cupxi += 1
        gs[item] = gene[cumu_name[cupxi]]
    # return new gene: dict
    return gs


def get_cross(gs: dict, args):
    gc = gs.copy()
    gs_keys = [i for i in gs.keys()]
    cnt = 0
    cross_group = [[gs[gs_keys[2*i]], gs[gs_keys[2*i+1]]] for i in range(len(gs)//2)]
    new_number = get_decode(gs, args)
    print(f"gs = {gs}")
    print(f"new_number = {new_number}")
    print(f"cross_group = {cross_group}")
    for group in cross_group:
        cross_bits = random.randint(1, args.max_cross_bits)
        # print(f"cross bits = {cross_bits}, cross step = {group[0][-cross_bits:]}, row step = {group[0][len(group[0])-cross_bits:]}")
        gc[gs_keys[cnt*2]] = group[0][:len(group[0])-cross_bits] + group[1][-cross_bits:]
        gc[gs_keys[cnt*2 + 1]] = group[1][:len(group[1])-cross_bits] + group[0][-cross_bits:]
        cnt += 1
    print(f"gc = {gc}")
    print(f"new number after crossing: {get_decode(gc, args)}")
    # return new gene: dict
    return gc


def get_mutation(gc: dict, args):

    # return new gene: dict


def get_init(is_init=True, row_number=None):
    args = parse_args()
    if is_init:
        row_number = get_row_number(args)
    print(f"row number is {row_number}")
    gene = get_encode(row_number, args)
    print(f"gene is {gene}")
    fitness = get_fitness(gene, args)
    print(f"fitness is {fitness}")
    pxi, cumulative_pxi = get_pxi(fitness, args)
    print(f"pxi = {pxi}\ncumulative pxi = {cumulative_pxi}")
    return gene, cumulative_pxi, args


# def SGA(C, E, P0, M, end):
def SGA():
    gene, cumulative_pxi, args = get_init()
    gs = get_select(gene, cumulative_pxi)
    gc = get_cross(gs, args)
    gm = get_mutation()


if __name__ == "__main__":
    SGA()