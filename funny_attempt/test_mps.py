# M1 GPU test
import torch
x = torch.randn(10000, 1024, device="mps")
print(x)