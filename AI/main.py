import torch, pdb
from torch.utils.data import DataLoader
from torch import nn
from torchvision import transforms
from torchvision.datasets import MNIST
from torchvision.utils import make_grid
from tqdm.auto import tqdm
import matplotlib.pyplot as plt


# viz function
def show(tensor, ch=1, size=(28, 28), num=16):
    data = tensor.detach().cpu().view(-1, ch, *size)
    grid = make_grid(data[:num], nrow=4).permute(1, 2, 0)
    plt.imshow(grid)
    plt.show()


# setup of main parameters and hyperparameters
epochs = 500
cur_step = 0
info_step = 300
mean_gen_loss = 0
mean_disc_loss = 0

z_dim = 64
lr = 0.00001  # learn rate
loss_func = nn.BCEWithLogitsLoss()

bs = 128  # batch size
device = 'cuda'

dataloader = DataLoader(MNIST('.', download=True, transform=transforms.ToTensor()), shuffle=True, batch_size=bs)


# number of steps = 60000 / 128 = 468.75

# declare models


# Generator
def genBlock(inp, out):
    return nn.Sequential(
        nn.Linear(inp, out),
        nn.BatchNorm1d(out),
        nn.ReLU(inplace=True)
    )


class Generator(nn.Module):
    def __init__(self, z_dim=64, i_dim=784, h_dim=128):
        super().__init__()
        self.gen = nn.Sequential(
            genBlock(z_dim, h_dim),  # enter 64 exit 128
            genBlock(h_dim, h_dim * 2),  # from 128 to 256
            genBlock(h_dim * 2, h_dim * 4),  # from 256 to 512
            genBlock(h_dim * 4, h_dim * 8),  # from 512 to 1024
            nn.Linear(h_dim * 8, i_dim * 8),  # from 1024 to 784 (28x28)
            nn.Sigmoid()
        )

    def foward(self, noise):
        return self.gen(noise)

    def gen_noise(number, z_dim):
        return torch.randn(number, z_dim).to(device)


# Discriminator
def discBlock(inp, out):
    return nn.Sequential(
        nn.Linear(inp, out),
        nn.LeakyReLU(0.2)
    )

class Discriminator(nn.Module):
    def __init__(self,i_dim=784, h_dim=256):
        super().__init__()
        self.disc=nn.Sequential(
            discBlock(i_dim, h_dim*4),  # 784 to 1024
            discBlock(h_dim*4, h_dim*2),  # 1024 to 512
            discBlock(h_dim*2, h_dim),  # 512 to 256
            nn.Linear(h_dim, 1)  # 256 to 1
        )

        def forward(self, image):
            return self.disc(image)


gen = Generator(z_dim).to(device)
gen_opt = torch.optim.Adam(gen.parameters(), lr=lr)
disc = Discriminator().to(device)
disc_opt = torch.optim.Adam(disc.parameters(), lr=lr)


