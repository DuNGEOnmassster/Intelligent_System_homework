import math
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
from common import GetData,ResultShow,draw

def calFitness(line,dis_matrix):
    dis_sum = 0
    dis = 0
    for i in range(len(line)):
        if i<len(line)-1:
            dis = dis_matrix.loc[line[i],line[i+1]]
            dis_sum = dis_sum+dis
        else:
            dis = dis_matrix.loc[line[i],line[0]]
            dis_sum = dis_sum+dis
    return round(dis_sum,1)


def tournament_select(pops,popsize,fits,tournament_size):
    new_pops,new_fits = [],[]
    while len(new_pops)<len(pops):
        tournament_list = random.sample(range(0,popsize),tournament_size)
        tournament_fit = [fits[i] for i in tournament_list]
        #转化为df方便索引
        tournament_df = pd.DataFrame([tournament_list,tournament_fit]).transpose().sort_values(by=1).reset_index(drop=True)
        #选出获胜者
        fit = tournament_df.iloc[0,1]
        pop = pops[int(tournament_df.iloc[0,0])]
        new_pops.append(pop)
        new_fits.append(fit)
    return new_pops,new_fits


def crossover(popsize,parent1_pops,parent2_pops,pc):
    child_pops = []
    for i in range(popsize):
        #初始化
        child = [None]*len(parent1_pops[i])
        parent1 = parent1_pops[i]
        parent2 = parent2_pops[i]
        if random.random() >= pc:
            child = parent1.copy()#随机生成一个（或者随机保留父代中的一个）
            random.shuffle(child)
        else:
            #parent1
            start_pos = random.randint(0,len(parent1)-1)
            end_pos = random.randint(0,len(parent1)-1)
            if start_pos>end_pos:
                tem_pop = start_pos
                start_pos = end_pos
                end_pos = tem_pop
            child[start_pos:end_pos+1] = parent1[start_pos:end_pos+1].copy()
            # parent2 -> child
            list1 = list(range(end_pos+1,len(parent2)))
            list2 = list(range(0,start_pos))
            list_index = list1+list2
            j = -1
            for i in list_index:
                for j in range(j+1,len(parent2)):
                    if parent2[j] not in child:
                        child[i] = parent2[j]
                        break
        child_pops.append(child)
    return child_pops


def mutate(pops,pm):
    pops_mutate = []
    for i in range(len(pops)):
        pop = pops[i].copy()
        #随机多次成对变异
        t = random.randint(1,5)
        count = 0
        while count < t:
            if random.random() < pm: 
                    mut_pos1 = random.randint(0,len(pop)-1)  
                    mut_pos2 = random.randint(0,len(pop)-1)
                    if mut_pos1 != mut_pos2:
                        tem = pop[mut_pos1]
                        pop[mut_pos1] = pop[mut_pos2]
                        pop[mut_pos2] = tem
            pops_mutate.append(pop)
            count +=1
    return pops_mutate


def draw_path(line,CityCoordinates):
    x,y= [],[]
    for i in line:
        Coordinate = CityCoordinates[i]
        x.append(Coordinate[0])
        y.append(Coordinate[1])
    x.append(x[0])
    y.append(y[0])
    plt.title("Genetic Algorithm TSP")
    plt.plot(x, y,'r-', color='#4169E1', alpha=0.8, linewidth=0.8)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()


def get_city(path):
    CityCoordinates = []
    with open(path, "r") as file:
        all_line = file.readlines()
        for line in all_line:
            point = line.split("\n")[0].split(" ")[-2:]
            CityCoordinates.append((int(point[0]), int(point[1])))
    return CityCoordinates


if __name__ == '__main__':
    #参数
    CityNum = 20#城市数量
    MinCoordinate = 0#二维坐标最小值
    MaxCoordinate = 101#二维坐标最大值
    #GA参数
    generation = 10000  #迭代次数
    popsize = 100   #种群大小
    tournament_size = 5 #锦标赛小组大小
    pc = 0.95   #交叉概率
    pm = 0.1    #变异概率

    CityCoordinates = get_city("./data/TSP100cities.tsp")
    #计算城市之间的距离
    dis_matrix = pd.DataFrame(data=None,columns=range(len(CityCoordinates)),index=range(len(CityCoordinates)))
    for i in range(len(CityCoordinates)):
        xi,yi = CityCoordinates[i][0],CityCoordinates[i][1]
        for j in range(len(CityCoordinates)):
            xj,yj = CityCoordinates[j][0],CityCoordinates[j][1]
            dis_matrix.iloc[i,j] = round(math.sqrt((xi-xj)**2+(yi-yj)**2),2)

    iteration = 0
    #初始化,随机构造
    pops = [random.sample([i for i in list(range(len(CityCoordinates)))],len(CityCoordinates)) for j in range(popsize)]
    
    #计算适应度
    fits = [None]*popsize
    for i in range(popsize):
        fits[i] = calFitness(pops[i],dis_matrix)
    #保留当前最优
    best_fit = min(fits)
    best_pop = pops[fits.index(best_fit)]
    print('初代最优值 %.1f' % (best_fit))
    best_fit_list = []
    best_fit_list.append(best_fit)
    
    pre_fit = best_fit
    repeat = 0
    early_stop = False
    start = time.time()				#程序计时开始
    while iteration <= generation:
        #锦标赛赛选择
        pop1,fits1 = tournament_select(pops,popsize,fits,tournament_size)
        pop2,fits2 = tournament_select(pops,popsize,fits,tournament_size)
        #交叉
        child_pops = crossover(popsize,pop1,pop2,pc)
        #变异
        child_pops = mutate(child_pops,pm)
        #计算子代适应度
        child_fits = [None]*popsize
        for i in range(popsize):
            child_fits[i] = calFitness(child_pops[i],dis_matrix) 
        #一对一生存者竞争
        for i in range(popsize):
            if fits[i] > child_fits[i]:
                fits[i] = child_fits[i]
                pops[i] = child_pops[i]
        
        if best_fit>min(fits):
            best_fit = min(fits)
            best_pop = pops[fits.index(best_fit)]
        
        best_fit_list.append(best_fit)
        
        print('第%d代最优值 %.1f' % (iteration, best_fit))
        iteration += 1

        # if repeat >= 10:
        #     early_stop = True
        #     end = time.time()
        #     break

        if best_fit == pre_fit:
            repeat += 1
        else:
            repeat = 0
            pre_fit = best_fit
        
    if early_stop:
        print("程序的运行时间是：%s"%(end-start))
    else:
        end = time.time()
        print("程序的运行时间是：%s"%(end-start))

    #路径顺序
    print(best_pop)
    #路径图
    draw_path(best_pop,CityCoordinates)
