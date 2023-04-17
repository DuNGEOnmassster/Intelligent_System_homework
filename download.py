import torch
from torchvision import datasets
from torchvision import transforms

train_transform = transforms.Compose([transforms.Resize((224, 224)),
                                        transforms.RandomHorizontalFlip(),
                                        transforms.ToTensor(),
                                        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

val_transform = transforms.Compose([transforms.Resize((224, 224)),
                                    transforms.ToTensor(),
                                    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

train_dataset = datasets.CIFAR100("./data", train=True, download=True, transform=train_transform)
val_dataset = datasets.CIFAR100("./data", train=False, download=True, transform=val_transform)