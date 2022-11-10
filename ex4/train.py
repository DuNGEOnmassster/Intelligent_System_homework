import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import argparse
import matplotlib.pyplot as plt
import torchvision
from torch.utils.data import DataLoader
from utils.utils import Net, train_loader, log_interval, test_loader


def parse_args():
    parser = argparse.ArgumentParser(description='MNIST in Pytorch')

    parser.add_argument('--batch_size_train', type=int, default=64,
                        help='declare batch size for training')
    parser.add_argument('--batch_size_test', type=int, default=1000,
                        help='declare batch size for testing')
    parser.add_argument('--epochs', type=int, default=20,
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

    args = parser.parse_args()

