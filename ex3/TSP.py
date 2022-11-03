import random
import argparse
import numpy as np
import math

def parse_args():
    parser = argparse.ArgumentParser(description="Solving TSP with Genetic Algorithms")
    
    parser.add_argument("--citys", type=int, default=10,
                        help="total num of citys")
    parser.add_argument("--target",type=float, default=166.541336,
                        help="The minimum answer referenced from report")
    parser.add_argument("--num", type=int, default=4,
                        help="population size")
    parser.add_argument("--binary_encode", type=bool, default=False,
                        help="whether use binary encode, TSP default with False")

    parser.add_argument("--max_generation", type=int, default=500,
                        help="declare the maximum of generation")
    parser.add_argument("--encode_bits", type=int, default=4,
                        help="declare the length of encode bits")
    parser.add_argument("--max_cross_bits", type=int, default=3,
                        help="declare the maximum of changing bits in a crossing epoch")
    parser.add_argument("--single_mutation_bits", type=int, default=1,
                        help="declare the maximum of mutation bits in a single gene")
    parser.add_argument("--max_mutation_bits", type=int, default=3,
                        help="declare the maximum of total mutation bits in a mutation epoch")

    return parser.parse_args()


def get_city_map():
    map_dict = {0: (87, 7),
                1: (91, 38),
                2: (83, 46),
                3: (71, 44),
                4: (64, 60),
                5: (68, 58),
                6: (83, 69),
                7: (87, 76),
                8: (74, 78),
                9: (71, 71)}
    return map_dict

def get_target(args):
    return args.target


def shuffle_set(a):
    p = np.random.permutation(len(a))
    return a[p]


def get_row_number(args):
    row_number = {}
    for i in range(args.num):
        key = "s" + str(i+1)
        row_number[key] = shuffle_set(np.array([i for i in range(args.citys)]))
    return row_number


def get_encode(row_number: dict, args):
    gene = row_number.copy()
    for item in gene.keys():
        if args.binary_encode:  # use binary encode for other problem
            gene[item] = bin(gene[item])   
            if len(gene[item]) < args.encode_bits + 2:
                zero_filling = "0" * (args.encode_bits + 2 - len(gene[item]))  
                gene[item] = "0b"+zero_filling+gene[item][2:] 
                print(f"warning! new is {gene[item]}")   
        else:  # binary encode is useless in TSP
            break
    return gene


def get_decode(gene: dict, args):
    row_number = gene.copy()
    for item in row_number.keys():
        if args.binary_encode:  # use binary decode for other problem
            row_number[item] = int(gene[item], 2)
        else:  # binary decode is useless in TSP
            break
    return row_number


def get_distance(c1, c2):
    l1 = c1[1]-c2[1]
    l2 = c1[0]-c2[0]
    distance = math.sqrt(l1**2 + l2**2)
    return distance


def get_fitness(gene: dict, args):
    fitness = gene.copy()
    print(f"fitness is {fitness}")
    # for item in fitness.keys():
    #     if args.binary_encode:
    #         fitness[item] = pow(int(fitness[item], 2), 2)
    #     else:
    #         fitness[item] = pow(fitness[item],2)
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


def get_select(gene: dict, args):
    fitness = get_fitness(gene, args)
    print(f"fitness is {fitness}")
    pxi, cumulative_pxi = get_pxi(fitness, args)
    print(f"pxi = {pxi}\ncumulative pxi = {cumulative_pxi}")
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
    gm = gc.copy()
    gc_keys = [i for i in gc.keys()]
    gc_mutation_count = {i:0 for i in gc_keys}
    for mutation in range(args.max_mutation_bits):
        lucky_number = random.randint(0, args.num-1)
        lucky_bit = random.randint(1, args.encode_bits)
        while 1:
            if gc_mutation_count[gc_keys[lucky_number]] < args.single_mutation_bits:
                gene_temp = gm[gc_keys[lucky_number]]
                print(f"lucky number = {lucky_number}, lucky gene = {gene_temp}, lucky bit = {lucky_bit} \
                    {gm[gc_keys[lucky_number]][-lucky_bit]}, {int(gm[gc_keys[lucky_number]][-lucky_bit])^1}")
                gm[gc_keys[lucky_number]] = gene_temp[:(7-lucky_bit)] + str(int(gm[gc_keys[lucky_number]][-lucky_bit])^1) + gene_temp[(7-lucky_bit+1):]
                gc_mutation_count[gc_keys[lucky_number]] += 1
                break
            else:
                lucky_number = (lucky_number + 1) % args.num
    print(f"gm = {gm}")
    # return new gene: dict
    return gm


def get_init(args, is_init=True, row_number=None):
    if is_init:
        row_number = get_row_number(args)
    print(f"row number is {row_number}")
    gene = get_encode(row_number, args)
    print(f"gene is {gene}")

    return gene


def check_target(gene: dict, args, cnt):
    gene_number = [i for i in get_decode(gene, args).values()]
    print(f"gene_number is {gene_number}")
    gene_fitness = get_fitness(gene_number, args)
    print(f"gene_fitness is {gene_fitness}")
    # target = get_target(args)
    # if cnt > args.max_generation:
    #     print(f"Reach maximum generation")
    #     return True
    # if target in gene_number:
    #     print(f"Find target :{target} in generation {cnt}")
    #     return True
    # else:
    #     return False


# def SGA(C, E, P0, M, end):
def SGA():
    args = parse_args()
    gene = get_init(args)
    cnt = 1
    check_target(gene, args, cnt)
    # while not check_target(gene, args, cnt):
    #     print(f"Generation {cnt}")
    #     gs = get_select(gene, args)
    #     gc = get_cross(gs, args)
    #     gene = get_mutation(gc, args)
    #     cnt += 1
    # a = np.array([i for i in range(1,6)])
    # b = np.array([i for i in range(2,7)])
    # print(f"a = {a}, b = {b}")
    # a = shuffle_set(a)
    # print(f"a = {a}, b = {b}")
    # return cnt


if __name__ == "__main__":
    SGA()