import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt

from utils.utils import learning_rate, momentum, n_epochs, train_loader, log_interval, test_loader, valid_loader


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # 卷积层
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        # 全连接层
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        # 激活层
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x)


# 初始化网络和优化器
network = Net()
optimizer = optim.SGD(network.parameters(), lr=learning_rate, momentum=momentum)
# 训练和测试分别使用两个list来存放数据
train_losses = []
train_counter = []
test_losses = []
test_acc = []
test_counter = [i * len(train_loader.dataset) for i in range(n_epochs + 1)]


def train(epoch):
    network.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        optimizer.zero_grad()
        output = network(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                       100. * batch_idx / len(train_loader), loss.item()))
            train_losses.append(loss.item())
            train_counter.append(
                (batch_idx * 64) + ((epoch - 1) * len(train_loader.dataset)))
            # 保存每次训练后的参数
            torch.save(network.state_dict(), './model/model.pth')
            torch.save(optimizer.state_dict(), './model/optimizer.pth')


def test():
    network.eval()
    valid_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in valid_loader:
            output = network(data)
            valid_loss += F.nll_loss(output, target, size_average=False).item()
            pred = output.data.max(1, keepdim=True)[1]
            correct += pred.eq(target.data.view_as(pred)).sum()
    valid_loss /= len(valid_loader.dataset)
    test_losses.append(valid_loss)
    print('\nTest set: Avg. loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        valid_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))
    correct = int(correct)/len(valid_loader.dataset)
    test_acc.append(correct)


if __name__ == '__main__':
    # 开始训练模型
    test()
    for epoch in range(1, n_epochs + 1):
        train(epoch)
        test()
    # 绘制loss曲线
    fig = plt.figure()
    plt.plot(train_counter, train_losses, color='blue')
    plt.scatter(test_counter, test_losses, color='red')
    plt.legend(['Train Loss', 'Test Loss'], loc='upper right')
    plt.xlabel('number of training examples seen')
    plt.ylabel('negative log likelihood loss')
    plt.show()
    # 训练优化模型
    continued_network = Net()
    continued_optimizer = optim.SGD(network.parameters(), lr=learning_rate,
                                    momentum=momentum)
    # 直接调用已保存的参数进一步训练
    network_state_dict = torch.load('./model/model.pth')
    continued_network.load_state_dict(network_state_dict)
    optimizer_state_dict = torch.load('./model/optimizer.pth')
    continued_optimizer.load_state_dict(optimizer_state_dict)
    # 继承前三次训练结果 并从第四次开始防止覆盖已有loss曲线
    for i in range(4, 9):
        test_counter.append(i * len(train_loader.dataset))
        train(i)
        test()
    # 绘制loss曲线
    fig1 = plt.figure()
    plt.plot(train_counter, train_losses, color='blue')
    plt.scatter(test_counter, test_losses, color='red')
    plt.legend(['Train Loss', 'Valid Loss'], loc='upper right')
    plt.xlabel('number of training examples seen')
    plt.ylabel('negative log likelihood loss')
    plt.show()
    # 绘制acc曲线
    fig2 = plt.figure()
    plt.scatter(test_counter, test_acc, color='green')
    plt.legend(['Valid Acc'], loc='upper right')
    plt.xlabel('number of training examples seen')
    plt.ylabel('negative log likelihood acc')
    plt.show()
