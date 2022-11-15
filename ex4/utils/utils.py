import torch
import torchvision
from torch.utils import data as Data

def init_dataloader(args):
    torch.manual_seed(args.random_seed)
    # get train loader and origin loader
    train_loader = torch.utils.data.DataLoader(
        torchvision.datasets.MNIST(args.dataset, train=True, download=True,
                                transform=torchvision.transforms.Compose([
                                    torchvision.transforms.ToTensor(),
                                    torchvision.transforms.Normalize(
                                        (0.1307,), (0.3081,))
                                ])),
        batch_size=args.batch_size_train, shuffle=True)
    origin_loader = torch.utils.data.DataLoader(
        torchvision.datasets.MNIST(args.dataset, train=False, download=True,
                                transform=torchvision.transforms.Compose([
                                    torchvision.transforms.ToTensor(),
                                    torchvision.transforms.Normalize(
                                        (0.1307,), (0.3081,))
                                ])),
        batch_size=args.batch_size_test, shuffle=True)

    # generate valid dataset and test dataset from origin dataset
    origin_dataset = origin_loader.dataset
    valid_split = args.valid_split
    valid_dataset,test_dataset = Data.random_split(origin_dataset,[int(len(origin_dataset)*valid_split), len(origin_dataset) - int(len(origin_dataset)*valid_split)])

    # get valid loader and test loader
    valid_loader = torch.utils.data.DataLoader(valid_dataset, batch_size = args.batch_size_test, shuffle = True, num_workers = 0)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size = args.batch_size_test, shuffle = True, num_workers = 0)

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
        valid_split = 0.5
            
    args = fake_args()
    train_loader,valid_loader,test_loader = init_dataloader(args)
    # for data, target in test_loader:
    #   print(data)
    #   print(target)
    #   print(type(test_loader))
    print(train_loader.dataset)
    print(valid_loader.dataset)
    print(test_loader.dataset)
    print(valid_loader.dataset[0][1])
    print(test_loader.dataset[0][1])
