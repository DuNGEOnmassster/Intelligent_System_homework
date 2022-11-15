import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt
import argparse
from utils.utils import init_dataloader


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


def parse_args():
    parser = argparse.ArgumentParser(description="MNIST implementation in pytorch")

    parser.add_argument("--n_epochs", type=int, default=8,
                        help="declare total number of trainning epochs")
    parser.add_argument("--dataset", default='./dataset/',
                        help="declare dataset path")
    parser.add_argument("--model_path", default="./model/model.pth",
                        help="declare model save&load path")
    parser.add_argument("--optimizer_path", default="./model/optimizer.pth",
                        help="declare optimizer save&load path")

    parser.add_argument("--batch_size_train", type=int, default=64,
                        help="declare batch size of train_loader")
    parser.add_argument("--batch_size_valid", type=int, default=1000,
                        help="declare batch size of valid_loader")
    parser.add_argument("--batch_size_test", type=int, default=16,
                        help="declare batch size of test_loader")
    parser.add_argument("--random_seed", type=int, default=3407,
                        help="use this magical random seed 3407")
    parser.add_argument("--lr", type=float, default=0.01,
                        help="declare learning rate")
    parser.add_argument("--weight_decay", type=float, default=1e-6,
                        help="declare weight decay used in Adam")
    parser.add_argument("--momentum", type=float, default=0.5,
                        help="declare momentum used in SGD")
    parser.add_argument("--log_interval", type=int, default=10,
                        help="declare log interval for loss printing")

    parser.add_argument("--use_SGD", type=bool, default=False,
                        help="declare whether to use SGD as optimizer")
    parser.add_argument("--use_Adam", type=bool, default=True,
                        help="declare whether to use Adam as optimizer")
    parser.add_argument("--use_mps", type=bool, default=True,
                        help="declare whether to use mps, default with True")

    return parser.parse_args()


def process():
    device = torch.device("mps") if args.use_mps else torch.device("cpu")
args = parse_args()
train_loader, valid_loader, test_loader = init_dataloader(args)
torch.manual_seed(args.random_seed)
# 初始化网络和优化器
model = Net()
if args.use_Adam:
    optimizer = optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
elif args.use_SGD:
    optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum)
else:
    # default with lr 0.0001 SGD
    optimizer = optim.SGD(model.parameters(), lr=0.0001)
# 训练和测试分别使用两个list来存放数据
train_losses = []
train_counter = []
test_losses = []
test_acc = []
test_counter = [i * len(train_loader.dataset) for i in range(args.n_epochs + 1)]


def train(epoch):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % args.log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                       100. * batch_idx / len(train_loader), loss.item()))
            train_losses.append(loss.item())
            train_counter.append(
                (batch_idx * 64) + ((epoch - 1) * len(train_loader.dataset)))
            # 保存每次训练后的参数
            torch.save(model.state_dict(), './model/model.pth')
            torch.save(optimizer.state_dict(), './model/optimizer.pth')


def test():
    model.eval()
    valid_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in valid_loader:
            output = model(data)
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


def draw_loss(train_counter, train_losses, test_counter, test_losses):
    # 绘制loss曲线
    fig = plt.figure()
    plt.plot(train_counter, train_losses, color='blue')
    plt.scatter(test_counter, test_losses, color='red')
    plt.legend(['Train Loss', 'Valid Loss'], loc='upper right')
    plt.xlabel('number of training examples seen')
    plt.ylabel('negative log likelihood loss')
    plt.show()


def draw_acc(total_epochs, test_acc):
    # 绘制acc曲线
    fig = plt.figure()
    plt.plot(total_epochs, test_acc, color='green')
    plt.legend(['Valid Acc'], loc='upper right')
    plt.xlabel('number of training examples seen')
    plt.ylabel('negative log likelihood acc')
    plt.show()

if __name__ == '__main__':
    # 开始训练模型
    total_epochs = [0]
    test()
    for epoch in range(1, args.n_epochs + 1):
        train(epoch)
        total_epochs.append(epoch)
        test()
    draw_loss(train_counter, train_losses, test_counter, test_losses)
    draw_acc(total_epochs, test_acc)
