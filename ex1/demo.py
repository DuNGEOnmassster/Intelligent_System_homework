def reversenum(node):
    """计算状态对应的逆序数,奇偶性一致则有解"""
    Sum = 0
    for i in range(1,9):
        num = 0
        for j in range(0,i):
          if node[j]>node[i] and node[i] != '0':
              num = num + 1
        Sum += num
    return Sum

def Hn(node):
    """h(n)函数，用于计算估价函数f(n)，这里的h(n)选择的是与目标状态相比错位的数目"""
    global goal
    hn = 0
    for i in range(0,9):
        if node[i] != goal[i]:
            hn += 1
    return hn
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
def expand_node(node):
    """拓展node状态对应的子结点"""
    # global expand
    tnode = []
    state = node.index("0")  # 返回"0"的位置
    elist = expand[state]  # 得知0可以移动的情况
    j = state
    for i in elist:
        j = state
        if i>j:
            i,j  =  j,i
        re =  node[:i] + node[j] + node[i+1:j] + node[i] + node[j+1:]  # 用切片拼出子节点
        tnode.append(re)
#     print(tnode)
    return tnode

def print_step(result):
    """将最后的结果按格式输出"""
    for i in range(len(result)):
            print("step--" + str(i+ 1))
            print(result[i][:3])
            print(result[i][3:6])
            print(result[i][6:])

def select_min(opened):
    """选择opened表中的最小的估价函数值对应的状态"""
    fn_dict = {}  # 字典
    for node in opened:
        fn = Fn[node]  
        fn_dict[node] = fn
    min_node = min(fn_dict, key = fn_dict.get) # 获得字典fn_dict中value的最小值所对应的键
    return min_node

def a_star(start, goal):
    if start == goal:
        print("初始状态和目标状态一致！")
        
    # 判断从初始状态是否可以达到目标状态
    if (reversenum(start)%2) != (reversenum(goal)%2):
        print("该目标状态不可达！")
        return None
        
    else:
        parent[start] = -1                # 初始结点的父结点存储为-1
        Gn[start] = 0                     # 初始结点的g(n)为0
        Fn[start] = Gn[start] + Hn(start)  # 计算初始结点的估价函数值 f(n)  =  g(n) + h(n)

        while opened:
            current = select_min(opened)  # 选择估价函数值最小的状态
            del Fn[current]              # 对代价清零
            opened.remove(current)       # 将要遍历的结点取出opened表

            if current == goal:
                break
                
            if current not in closed:
                closed.append(current)     # 存入closed表 
                Tnode = expand_node(current)    # 扩展子结点.用来遍历节点n所有的邻近节点
                print(f"Tnode =\n{Tnode}")
                for node in Tnode:
                    # 如果子结点在opened和closed表中都未出现，则存入opened表
                    # 并求出对应的估价函数值
                    if node not in opened and node not in closed:
                        Gn[node] = Gn[current]+1
                        Fn[node] = Gn[node]+Hn(node)
                        parent[node] = current
                        opened.append(node)
                    else:
                        # 若子结点已经在opened表中，则判断估价函数值更小的一个路径
                        # 同时改变parent字典和Fn字典中的值
                        if node in opened:
                            fn = Gn[current] + 1 + Hn(node)
                            if fn < Fn[node]:
                                Fn[node] = fn
                                parent[node] = current

        result = []  # 用来存放路径
        result.append(current)
        
        while parent[current] != -1:  # 根据parent字典中存储的父结点提取路径中的结点
            current  = parent[current]
            result.append(current)
        result.reverse()  # 逆序即为运行时的过程
        return result

if __name__ == "__main__":  
    # expand中存储的是九宫格中每个位置对应的可以移动的情况
    # 当定位了0的位置就可以得知可以移动的情况
    expand = {0:[1, 3],
              1:[0, 2, 4],
              2:[1, 5],
              3:[0,4,6], 
              4:[3,1,5,7], 
              5:[4,2,8],
              6:[3,7],  
              7:[6,4,8], 
              8:[7,5]}

    # start = input("请输入初始状态(从左至右，从上到下，如：153246708)：")
    # goal  = input("请输入目标状态(从左至右，从上到下，如：123456780)：")
    start = "153246708"
    goal = "123456780"
    
    # 初始化
    opened = [start]
    closed = []
    Fn = {}  # 状态对应的估价函数值 f(n)  =  g(n) + h(n)
    Gn = {}  # 初始结点到当前结点n的实际代价，即路径长度
    parent = {}  # 用来存储状态对应的父结点
    
    result = a_star(start, goal)
    if result != None:
        print_step(result)# 按格式输出结果


