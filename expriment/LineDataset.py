from typing import List
import torch
from torch.utils.data import Dataset
from torch.utils.data.sampler import Sampler

class LineDataset(Dataset):
    def __init__(self, length, slope, bias = 0, noise = 3, predictable = True):
        super().__init__()
        if predictable:
            torch.manual_seed(1)
        self.length = length
        self.x = torch.unsqueeze(torch.linspace(-1, 1, self.length + 1), dim=1).float()
        self.y = slope * self.x + bias + noise * torch.rand(self.x.size()).float()

    def cuda(self):
        self.x = self.x.cuda()
        self.y = self.y.cuda()
        return self

    def to(self, device):
        self.x = self.x.to(device=device)
        self.y = self.y.to(device=device)
        return self

    def __len__(self):
        return self.length

    def __getitem__(self, index):
        return self.x[index], self.y[index]
