import torch
import random
from matplotlib import pyplot as plt
from utils.utils import init_dataloader
from train import Net, args

_,_,test_loader = init_dataloader(args)
network = Net()
network_state_dict = torch.load('./model/model.pth')
network.load_state_dict(network_state_dict)
model = torch.load('./model/model.pth')
# 测试是否参数都match以便模型正常执行识别任务
print(network.load_state_dict(model, strict=False))

# model.load_state_dict(torch.load(model_path))

examples = enumerate(test_loader, start=100)
batch_idx, (example_data, example_targets) = next(examples)
with torch.no_grad():
    output = network(example_data)
print(type(output))
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
