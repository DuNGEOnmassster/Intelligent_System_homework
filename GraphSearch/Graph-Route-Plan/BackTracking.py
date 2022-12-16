City_Graph = [[0, 0, 0, 0, 0],
              [0,-1, 30, 6, 4],
              [0,30, -1, 5, 10],
              [0,6, 5, -1, 20],
              [0,4, 10, 20, -1]]
path_num = len(City_Graph) 
isin = [0]*(path_num) #用来检测该节点是否已经添加到路径中
path = [0]*(path_num) #用于储存路径
best_path = [0]*(path_num) #用于储存最优路径
best_length = 100000 #初始化最优路径的路程总和

