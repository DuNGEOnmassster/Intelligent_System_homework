# from torchsummary import summary
from utils.utils import Net


if __name__ == "__main__":
    model = Net()
    # summary(model, input_size=(10, 1, 5, 5), batch_size=1, device="cpu")
    print(model)
