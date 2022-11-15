import torch
import torchvision


def init_dataloader(args):
    torch.manual_seed(args.random_seed)
    train_loader = torch.utils.data.DataLoader(
        torchvision.datasets.MNIST(args.dataset, train=True, download=True,
                                transform=torchvision.transforms.Compose([
                                    torchvision.transforms.ToTensor(),
                                    torchvision.transforms.Normalize(
                                        (0.1307,), (0.3081,))
                                ])),
        batch_size=args.batch_size_train, shuffle=True)
    valid_loader = torch.utils.data.DataLoader(
        torchvision.datasets.MNIST(args.dataset, train=False, download=True,
                                transform=torchvision.transforms.Compose([
                                    torchvision.transforms.ToTensor(),
                                    torchvision.transforms.Normalize(
                                        (0.1307,), (0.3081,))
                                ])),
        batch_size=args.batch_size_valid, shuffle=True)

    test_loader = torch.utils.data.DataLoader(
        torchvision.datasets.MNIST(args.dataset, train=False, download=True,
                                transform=torchvision.transforms.Compose([
                                    torchvision.transforms.ToTensor(),
                                    torchvision.transforms.Normalize(
                                        (0.1307,), (0.3081,))
                                ])),
        batch_size=args.batch_size_test, shuffle=True)
    
    return train_loader, valid_loader, test_loader


if __name__ == "__main__":
    class fake_args():
        def __init__(self):
            pass

        dataset = "./dataset/"
        random_seed = 3407
        batch_size_train = 64
        batch_size_valid = 1000
        batch_size_test = 16
            
    args = fake_args()
    _,_,test_loader = init_dataloader(args)
    for data, target in test_loader:
      print(data)
      print(target)
      print(type(test_loader))
