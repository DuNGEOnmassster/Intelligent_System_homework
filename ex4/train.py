import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import argparse
import matplotlib.pyplot as plt
import torchvision
from torch.utils.data import DataLoader
from utils.utils import *


def parse_args():
    parser = argparse.ArgumentParser(description='MNIST in Pytorch')

    parser.add_argument('--batch_size_train', type=int, default=64,
                        help='declare batch size for training')
    parser.add_argument('--batch_size_test', type=int, default=1000,
                        help='declare batch size for testing')
    parser.add_argument('--epochs', type=int, default=10,
                        help='declare number of epochs to train')
    parser.add_argument('--lr', type=float, default=0.001,
                        help='declare learning rate')
    parser.add_argument('--gamma', type=float, default=0.7,
                        help='Learning rate step gamma')
    parser.add_argument("--momentum", type=float, default=0.5,
                        help="declare optim momentum")
    parser.add_argument('--use_mps', action='store_true', default=True,
                        help='use MacOS GPU for training')
    parser.add_argument('--ramdom_seed', type=int, default=1,
                        help='declare random seed')
    parser.add_argument('--log_interval', type=int, default=10,
                        help='how many batches to wait before logging training status')

    parser.add_argument("--dataset_path", type=str, default="./dataset/",
                        help="declare dataset path")
    parser.add_argument("--model_save_path", type=str, default="./model/",
                        help="declare model save path")
    parser.add_argument

    return parser.parse_args()

args = parse_args()


train_loader = DataLoader(
    torchvision.datasets.MNIST(args.dataset_path, train=True, download=True,
                               transform=torchvision.transforms.Compose([
                                   torchvision.transforms.ToTensor(),
                                   torchvision.transforms.Normalize(
                                       (0.1307,), (0.3081,))
                               ])),
    batch_size=args.batch_size_train, shuffle=True)
test_loader = DataLoader(
    torchvision.datasets.MNIST(args.dataset_path, train=False,
                               transform=torchvision.transforms.Compose([
                                   torchvision.transforms.ToTensor(),
                                   torchvision.transforms.Normalize(
                                       (0.1307,), (0.3081,))
                               ])),
    batch_size=args.batch_size_test, shuffle=True)
valid_loader = DataLoader(
    torchvision.datasets.MNIST(args.dataset_path, train=False,
                               transform=torchvision.transforms.Compose([
                                   torchvision.transforms.ToTensor(),
                                   torchvision.transforms.Normalize(
                                       (0.1307,), (0.3081,))
                               ])),
    batch_size=args.batch_size_test, shuffle=True)

device = torch.device("mps")
# 初始化网络和优化器
network = Net().to(device)
optimizer = optim.SGD(network.parameters(), lr=args.lr, momentum=args.momentum)
# 训练和测试分别使用两个list来存放数据
train_losses = []
train_counter = []
test_losses = []
test_counter = [i * len(train_loader.dataset) for i in range(args.epochs)]


def train(epoch, train_loader, device):
    network.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = network(data)
        loss = F.nll_loss(output, target, reduction='sum')
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
            torch.save(network.state_dict(), (args.model_save_path + 'model.pth'))
            torch.save(optimizer.state_dict(), (args.model_save_path + 'optimizer.pth'))


def test(test_loader, device):
    network.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = network(data)
            test_loss += F.nll_loss(output, target, size_average=False).item()
            pred = output.data.max(1, keepdim=True)[1]
            correct += pred.eq(target.data.view_as(pred)).sum()
    test_loss /= len(test_loader.dataset)
    test_losses.append(test_loss)
    print('\nTest set: Avgloss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))


if __name__ == '__main__':
    device = torch.device("mps")
    criterion = nn.CrossEntropyLoss()
    # 开始训练模型
    for epoch in range(1, args.epochs + 1):
        train(epoch, train_loader, device)
        test(test_loader, device)
        # test_model(test_loader,criterion,network)
    # 绘制loss曲线
    fig = plt.figure()
    plt.plot(train_counter, train_losses, color='blue')
    print(f"counter is {len(test_counter)}, losses is {len(test_losses)}")
    plt.scatter(test_counter, test_losses, color='red')
    plt.legend(['Train Loss', 'Test Loss'], loc='upper right')
    plt.xlabel('number of training examples seen')
    plt.ylabel('negative log likelihood loss')
    plt.show()


