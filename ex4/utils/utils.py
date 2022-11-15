import torch
import torchvision
import sys
from torch.utils import data as Data
import numpy as np
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.dropout = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.dropout(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x)


# 定义模型结构
class CNN(nn.Module):

    def __init__(self):
        super(CNN,self).__init__()
        self.conv1 = nn.Conv1d(in_channels = 1,out_channels = 16,kernel_size = 3,stride = 1,padding = 1)
        self.conv2 = nn.Conv1d(16,32,3,1,1)
        self.conv3 = nn.Conv1d(32,64,3,1,1)
        self.conv4 = nn.Conv1d(64,64,5,1,2)
        self.conv5 = nn.Conv1d(64,128,5,1,2)
        self.conv6 = nn.Conv1d(128,128,5,1,2)
        self.maxpool = nn.MaxPool1d(3,stride=2)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
        self.softmax = nn.Softmax(dim=1)
        self.dropout = nn.Dropout(0.5)
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(40832,256)
        self.fc21 = nn.Linear(40832,16)
        self.fc22 = nn.Linear(16,256)
        self.fc3 = nn.Linear(256,3)

    def forward(self,x):
        x = x.view(x.size(0),1,x.size(1))
        x = self.conv1(x)   #nn.Conv1d(in_channels = 1,out_channels = 32,kernel_size = 11,stride = 1,padding = 5)
        x = self.relu(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = self.conv3(x)
        x = self.relu(x)
        x = self.conv4(x)
        x = self.relu(x)
        x = self.maxpool(x)
        x = self.conv5(x)
        x = self.relu(x)
        x = self.conv6(x)
        x = self.relu(x)        
        x = self.maxpool(x)
        x = self.dropout(x)
        x = self.flatten(x)
        x1 = self.fc1(x)
        x1 = self.relu(x1)
        x21 = self.fc21(x)
        x22 = self.relu(x21)
        x22 = self.fc22(x22)
        x2 = self.relu(x22)
        x = self.fc3(x1+x2)
        return x


# 定义数据适配器，用于加载数据至pytorch框架
class DataAdapter(Data.Dataset):

    def __init__(self,X,Y):
        super(DataAdapter,self).__init__()
        self.X = torch.FloatTensor(X)
        self.Y = torch.LongTensor(Y)

    def __getitem__(self,index):
        return self.X[index,:],self.Y[index]

    def __len__(self):
        return len(self.X)


# 定义该函数用于重新打乱训练集和验证集
def shuffle_data(train_loader,valid_loader,valid_split,batch_size):
    train_dataset = train_loader.dataset.dataset # 获取训练集的数据集
    valid_dataset = valid_loader.dataset.dataset
    X = torch.cat((train_dataset.X,valid_dataset.X),0) # 拼接数据集
    Y = torch.cat((train_dataset.Y,valid_dataset.Y),0)
    dataset = DataAdapter(X,Y) # 重新生成数据集
    train_dataset,valid_dataset = Data.random_split(dataset,[len(dataset) - int(len(dataset)*valid_split),int(len(dataset)*valid_split)]) # 重新划分训练集和验证集
    train_loader = Data.DataLoader(train_dataset,batch_size = batch_size,shuffle = True,num_workers = 0)
    valid_loader = Data.DataLoader(valid_dataset,batch_size = batch_size,shuffle = True,num_workers = 0)
    return train_loader,valid_loader


# 定义训练函数
def train_model(train_loader, model, criterion, optimizer, device):
    model.train()
    train_loss = []
    train_acc = []

    for i, data in enumerate(train_loader, 0):
        # inputs,labels = data[0].cuda(),data[1].cuda()
#         inputs, labels = data[0].cuda(), data[1].cuda()  # 获取数据
        inputs, labels = data[0], data[1]  # 获取数据

        outputs = model(inputs)  # 预测结果

        _, pred = outputs.max(1)  # 求概率最大值对应的标签

        num_correct = (pred == labels).sum().item()
        acc = num_correct / len(labels)  # 计算准确率

        loss = criterion(outputs, labels)  # 计算loss
        optimizer.zero_grad()  # 梯度清0
        loss.backward()  # 反向传播
        optimizer.step()  # 更新系数

        train_loss.append(loss.item())
        train_acc.append(acc)

    return np.mean(train_loss), np.mean(train_acc)


# 定义测试函数，具体结构与训练函数相似
def test_model(test_loader, criterion, model):
    model.eval()
    test_loss = []
    test_acc = []

    for i, data in enumerate(test_loader, 0):
        # inputs,labels = data[0].cuda(),data[1].cuda()
#         inputs, labels = data[0].cuda(), data[1].cuda()
        inputs, labels = data[0], data[1]

        outputs = model(inputs)
        loss = criterion(outputs, labels)

        _, pred = outputs.max(1)
        num_correct = (pred == labels).sum().item()
        acc = num_correct / len(labels)

        test_loss.append(loss.item())
        test_acc.append(acc)

    return np.mean(test_loss), np.mean(test_acc)