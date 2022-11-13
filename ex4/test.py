import torch
from matplotlib import pyplot as plt
from train import valid_loader, network, args
import torch.nn.functional as F

test_loader = valid_loader
device = torch.device("mps")
network = network.to(device)
model_path = args.model_save_path + 'model.pth'
model = torch.load(model_path)
# 测试是否参数都match以便模型正常执行识别任务
print(network.load_state_dict(model, strict=False))


network.eval()
test_loss = 0
correct = 0
examples = enumerate(test_loader)
batch_idx, (example_data, example_targets) = next(examples)
example_data, example_targets = example_data, example_targets.to(device)
with torch.no_grad():
    for data, target in test_loader:
        data, target = data.to(device), target.to(device)
        output = network(data)
        test_loss += F.nll_loss(output, target, size_average=False).item()
        pred = output.data.max(1, keepdim=True)[1]
        correct += pred.eq(target.data.view_as(pred)).sum()
test_loss /= len(test_loader.dataset)
print('\nTest set: Avgloss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
    test_loss, correct, len(test_loader.dataset),
    100. * correct / len(test_loader.dataset)))


fig = plt.figure()
for i in range(16):
    plt.subplot(4, 4, i + 1)
    plt.tight_layout()
    plt.imshow(example_data[i][0], cmap='gray', interpolation='none')
    plt.title("Prediction: {}".format(
        output.data.max(1, keepdim=True)[1][i].item()))
    plt.xticks([])
    plt.yticks([])
plt.show()
