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
    parser.add_argument("--max_cross_citys", type=int, default=3,
                        help="declare the maximum of changing citys in each crossing group")
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
    fitness_name = [i for i in fitness.keys()]
    gene_number = [i for i in get_decode(gene, args).values()]
    city_map = get_city_map()
    cnt = 0
    for item in gene_number:
        ada_sum = 0
        for i in range(len(item)):
            c1 = city_map[item[i]]
            c2 = city_map[item[i+1]] if i+1 < len(item) else city_map[item[0]]
            distance = get_distance(c1, c2)
            ada_sum += distance
        fitness[fitness_name[cnt]] = ada_sum
        cnt += 1
    return fitness


def get_pxi(fitness: dict, args):
    cnt = 0
    fitness_name = [i for i in fitness.keys()]
    for item in fitness.values():
        fitness[fitness_name[cnt]] = 1/item
        cnt += 1
    sum_fitness = sum(fitness.values())
    # print(f"new fitness is {fitness}\nsum fitness is {sum_fitness}")
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
    print(f"gs = {gs}")
    # return new gene: dict
    return gs


def get_cross(gs: dict, args):
    gc = gs.copy()
    gs_keys = [i for i in gs.keys()]
    cross_group = [[gs[gs_keys[2*i]], gs[gs_keys[2*i+1]]] for i in range(len(gs)//2)]
    new_number = get_decode(gs, args)
    print(f"new_number = {new_number}")
    print(f"cross_group = {cross_group}")
    seed = np.random.randint(0, args.citys, 2)
    seed.sort()
    start_seed = seed[0]
    end_seed = seed[1]
    print(f"start seed is {start_seed}, end seed is {end_seed}")
    # for group in cross_group:
    #     cross_citys = random.randint(1, args.max_cross_citys)
    #     cross_site = random.randint(0,args.citys-cross_citys-1)
    #     city_set = [i for i in group[0][cross_site:cross_site+cross_citys]]
    #     print(f"In group0:{group[0]}, cross num is {cross_citys}, cross site is {cross_site}, city set is {city_set}")
    #     crossed_sites = []
    #     for i in city_set:
    #         crossed_sites.append(group[1].tolist().index(i))
    #     print(f"In group1:{group[1]}, crossed site is {sorted(crossed_sites)}")
    #     cnt = 0
    #     for i in sorted(crossed_sites):
    #         group[0][cross_site+cnt] = group[1][i]
    #     cnt = 0
    #     for i in sorted(crossed_sites):
    #         group[1][i] = city_set[cnt]
    #         cnt += 1
        
    #     gc[gs_keys[cnt*2]] = group[0][:len(group[0])-cross_bits] + group[1][-cross_bits:]
    #     gc[gs_keys[cnt*2 + 1]] = group[1][:len(group[1])-cross_bits] + group[0][-cross_bits:]
    #     cnt += 1
    # print(f"gc = {gc}")
    # print(f"new number after crossing: {get_decode(gc, args)}")
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
    gene_fitness = get_fitness(gene, args)
    # print(f"gene_fitness is {gene_fitness}")
    target = get_target(args)
    if cnt > args.max_generation:
        print(f"Reach maximum generation")
        return True
    for fit in gene_fitness.values():     
        if target >= float(fit):
            print(f"Find target :{fit} in generation {cnt}")
            return True
    else:
        return False


# def SGA(C, E, P0, M, end):
def SGA():
    args = parse_args()
    gene = get_init(args)
    cnt = 1
    # check_target(gene, args, cnt)
    while not check_target(gene, args, cnt):
        print(f"Generation {cnt}")
        gs = get_select(gene, args)
        print(f"gs = {gs}")
        gc = get_cross(gs, args)
        # gene = get_mutation(gc, args)
        cnt += 1
        gene = gc
    # a = np.array([i for i in range(1,6)])
    # b = np.array([i for i in range(2,7)])
    # print(f"a = {a}, b = {b}")
    # a = shuffle_set(a)
    # print(f"a = {a}, b = {b}")
    # return cnt


if __name__ == "__main__":
    SGA()