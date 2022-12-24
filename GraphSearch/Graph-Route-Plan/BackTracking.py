# -*- coding: utf-8 -*-
"""
	基于回溯法的旅行商问题解法Python源码

	Author:	Greatpan
	Date:	2018.10.10
"""

import numpy as np
import time


# -*- coding: utf-8 -*-
"""
	基于贪心算法的旅行商问题解法Python源码
	
	Author:	Greatpan
	Date:	2018.9.30
"""

import math 
import time

def GreedyMethond(CityNum,Dist):
	"""
	函数名：GreedyMethond(CityNum,Dist)
	函数功能：	贪心策略算法核心
		输入	1 	CityNum：城市数量
			2	Dist：城市间距离矩阵
		输出	1 Cumulative_Path：最优路径长
			2 Already_Visited_City：最优路径
	其他说明：无
	"""
	Already_Visited_City=[]					#Already_Visited_City:已经遍历过的城市
	Cumulative_Path=0						#Cumulative_Path:目前所走城市的累积路径长
	Already_Visited_City.append(0)			#从城市0出发						

	for i in range(1,CityNum):  
		Cur_Min_Dist=math.inf				#Cur_Min_Dist：当前最小距离
		for j in range(1,CityNum):			#寻找下一个距离最短的城市
			if j not in Already_Visited_City and (Dist[Already_Visited_City[i-1]][j] < Cur_Min_Dist):
				Cur_Min_City = j;			#Cur_Min_City:代表离当前城市距离最小的未经历的城市
				Cur_Min_Dist=Dist[Already_Visited_City[i - 1]][j];

		Already_Visited_City.append(Cur_Min_City)
		Cumulative_Path+=Cur_Min_Dist
	Cumulative_Path+=Dist[0][Cur_Min_City]	#将从最后一个城市回到出发城市的距离
	Already_Visited_City.append(0)
	return Cumulative_Path,Already_Visited_City

##############################程序入口#########################################
if __name__ == "__main__":
	Position,CityNum,Dist = GetData("./data/TSP25cities.tsp")

	start = time.clock()				#程序计时开始
	Min_Path,BestPath=GreedyMethond(CityNum,Dist)	#调用贪心算法
	end = time.clock()					#程序计时结束

	print()
	ResultShow(Min_Path,BestPath,CityNum,"贪心算法")
	print("程序的运行时间是：%s"%(end-start))
	draw(BestPath,Position,"Greedy Methond")
"""
结果：
贪心法求得最短旅行商经过所有城市回到原城市的最短路径为：
0->9->8->5->3->2->1->7->4->6->0
总路径长为：10464.1834865

程序的运行时间是：0.000508957
"""

# -*- coding: utf-8 -*-
"""
	基于贪心算法的旅行商问题解法Python源码
	
	Author:	Greatpan
	Date:	2018.9.30
"""
import pandas
import numpy as np
import math
import matplotlib.pyplot as plt 

class Node:
	"""
	类名：Node
	函数功能：	从外界读取城市数据并处理
		输入	无
		输出	1 Position：各个城市的位置矩阵
			2 CityNum：城市数量
			3 Dist：城市间距离矩阵
	其他说明：无
	"""
	def __init__(self,CityNum):
		"""
		函数名：GetData()
		函数功能：	从外界读取城市数据并处理
			输入	无
			输出	1 Position：各个城市的位置矩阵
				2 CityNum：城市数量
				3 Dist：城市间距离矩阵
		其他说明：无
		"""
		self.visited=[False]*CityNum    #记录城市是否走过
		self.start=0                    #起点城市
		self.end=0                      #目标城市
		self.current=0                  #当前所处城市
		self.num=0                      #走过的城市数量
		self.pathsum=0                  #走过的总路程
		self.lb=0                       #当前结点的下界
		self.listc=[]                   #记录依次走过的城市

def GetData(datapath):
	"""
	函数名：GetData()
	函数功能：	从外界读取城市数据并处理
		输入	无
		输出	1 Position：各个城市的位置矩阵
			2 CityNum：城市数量
			3 Dist：城市间距离矩阵
	其他说明：无
	"""
	dataframe = pandas.read_csv(datapath,sep=" ",header=None)
	Cities = dataframe.iloc[:,1:3]
	Position= np.array(Cities)				#从城市A到B的距离矩阵
	CityNum=Position.shape[0]				#CityNum:代表城市数量
	Dist = np.zeros((CityNum,CityNum))		#Dist(i,j)：城市i与城市j间的距离

	#计算距离矩阵
	for i in range(CityNum):
		for j in range(CityNum):
			if i==j:
				Dist[i,j] = math.inf
			else:
				Dist[i,j] = math.sqrt(np.sum((Position[i,:]-Position[j,:])**2))
	return Position,CityNum,Dist

def ResultShow(Min_Path,BestPath,CityNum,string):
	"""
	函数名：GetData()
	函数功能：	从外界读取城市数据并处理
		输入	无
		输出	1 Position：各个城市的位置矩阵
			2 CityNum：城市数量
			3 Dist：城市间距离矩阵
	其他说明：无
	"""
	print("基于"+string+"求得的旅行商最短路径为：")
	for m in range(CityNum):
		print(str(BestPath[m])+"—>",end="")
	print(BestPath[CityNum])
	print("总路径长为："+str(Min_Path))
	print()

def draw(BestPath,Position,title):
	"""
	函数名：draw(BestPath,Position,title)
	函数功能：	通过最优路径将旅行商依次经过的城市在图表上绘制出来
		输入	1 	BestPath：最优路径
			2	Position：各个城市的位置矩阵
			3	title:图表的标题
		输出	无
	其他说明：无
	"""
	plt.title(title) 
	plt.plot(Position[:,0],Position[:,1],'bo')
	for i,city in enumerate(Position): 
		plt.text(city[0], city[1], str(i)) 
	plt.plot(Position[BestPath, 0], Position[BestPath, 1], color='red') 
	plt.show()

def CalcPath_sum(layer,i):
	"""
		函数名：CalcPath_sum(layer,i)
		函数功能：计算从初始城市到第layer层再到接下来的第i个城市所经历的总距离
			输入	1: layer 回溯所处的层数，也即所遍历的城市数
				2: i 当前层数下接下来要访问的子节点，即要访问的下一个城市
			输出	1: Path_sum 求的的是当前递归所处的层数的累积路径值+到下一个节点的距离
		其他说明：无
	"""
	#计算从初始城市到第layer层
	Path_sum = sum([Dist[city1][city2] for city1,city2 in zip(Curpath[:layer], Curpath[1:layer+1])])

	#计算从初始城市到第layer层再到接下来的第i个城市所经历的总距离
	Path_sum += Dist[Curpath[i-1]][i]

	return Path_sum


def IsPrun(layer,i):
	"""
	函数名：IsPrun(layer,i)
	函数功能：判断是否符合剪枝条件，符合则返回True,不符合则返回False
		输入	1: layer 回溯所处的层数，也即所遍历的城市数
			2: i 当前层数下接下来要访问的子节点，即要访问的下一个城市
		输出	1: 是——返回True，否——返回False
	其他说明：Path_sum 求的的是当前递归所处的层数的累积路径值+到下一个节点的距离
	"""
	Path_sum=CalcPath_sum(layer,i)

	# Path_sum值大于当前所求得的最小距离时则进行剪枝(True),否则不减枝(False)
	if Path_sum >= Cur_Min_Path:
		return True
	else:
		return False


def BackTrackingMethod(Dist,CityNum,layer):
	"""
	函数名：BackTrackingMethod(Dist,CityNum,layer)
	函数功能： 动态规划算法的程序入口
		输入	1 CityNum：城市数量
			2 Dist：城市间距离矩阵
            3 layer:旅行商所处层数，也即遍历的城市数
		输出	：无
	其他说明：无
	"""
	global Path_sum,Cur_Min_Path,Min_Path,BestPath
	if(layer==CityNum):
		Path_sum=CalcPath_sum(layer,0)
		if(Path_sum<=Cur_Min_Path):
			Cur_Min_Path=Path_sum
			Min_Path=Cur_Min_Path
			BestPath=Curpath.tolist()
			BestPath.append(0)
	else:
		for i in range(layer,CityNum):
			#判断是否符合剪枝条件，不符合则继续执行
			if IsPrun(layer,i):
				continue
			else:
				Curpath[i],Curpath[layer] = Curpath[layer],Curpath[i]  # 路径交换一下
				BackTrackingMethod(Dist, CityNum, layer+1)
				Curpath[i],Curpath[layer] = Curpath[layer],Curpath[i]  # 路径交换回来

##############################程序入口#########################################
if __name__ == "__main__":
	Position,CityNum,Dist = GetData("./data/TSP10cities.tsp")
	Curpath = np.arange(CityNum)
	Min_Path=0
	BestPath=[]
	Cur_Min_Path = Greedy.GreedyMethond(CityNum,Dist)[0]

	start = time.clock()				#程序计时开始
	BackTrackingMethod(Dist,CityNum,1)	#调用回溯法
	end = time.clock()					#程序计时结束

	print()
	ResultShow(Min_Path,BestPath,CityNum,"回溯法")
	print("程序的运行时间是：%s"%(end-start))
	draw(BestPath,Position,"BackTracking Method")

"""
结果：
回溯法求得最短旅行商经过所有城市回到原城市的最短路径为：
0->4->6->7->1->3->2->5->8->9->0
总路径长为：10127.552143541276

程序的运行时间是：0.245802962
"""