import torch
from matplotlib import pyplot as plt
from utils.utils import init_dataloader
from train import Net, args


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


def process():
    _,_,test_loader = init_dataloader(args)
    model = Net()
    network_state_dict = torch.load('./model/model.pth')
    model.load_state_dict(network_state_dict)

    examples = enumerate(test_loader, start=100)
    batch_idx, (example_data, example_targets) = next(examples)
    with torch.no_grad():
        output = model(example_data)
    show_examples(output, example_data)

if __name__ == "__main__":
    process()