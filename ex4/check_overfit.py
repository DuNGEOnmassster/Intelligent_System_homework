import torch
import torch.nn.functional as F
from matplotlib import pyplot as plt
from train import Net, args, test_loader

def show_examples(output, example_data):
    fig = plt.figure()
    for i in range(16):
        plt.subplot(4, 4, i + 1)
        plt.tight_layout()
        # 设置字体为楷体
        plt.rcParams['font.sans-serif'] = ['KaiTi']
        plt.imshow(example_data[i][0], cmap='gray', interpolation='none')
        plt.title("Prediction: {}".format(
            output.data.max(1, keepdim=True)[1][i].item()))
        plt.xticks([])
        plt.yticks([])
    plt.show()


def draw_loss(test_counter, test_losses):
    # draw loss curve
    fig = plt.figure()
    plt.plot(test_counter, test_losses, color='red')
    plt.legend(['Valid Loss'], loc='upper right')
    plt.xlabel('number of training examples seen')
    plt.ylabel('negative log likelihood loss')
    plt.show()


def test(model, test_loader, device, test_losses, test_acc, test_counter):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, size_average=False).item()
            pred = output.data.max(1, keepdim=True)[1]
            correct += pred.eq(target.data.view_as(pred)).sum()
    test_loss /= len(test_loader.dataset)
    test_losses.append(test_loss)
    test_counter = [i for i in range(1, len(test_loader.dataset)+1)]
    print('\nTest set: Avg. loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))
    correct = int(correct)/len(test_loader.dataset)
    test_acc.append(correct)


def process():
    test_losses = []
    test_acc = []
    test_counter = []

    device = torch.device("mps") if args.use_mps else torch.device("cpu")
    model = Net().to(device)
    network_state_dict = torch.load('./model/model.pth')
    model.load_state_dict(network_state_dict)
    test(model, test_loader, device, test_losses, test_acc, test_counter)


if __name__ == "__main__":
    process()