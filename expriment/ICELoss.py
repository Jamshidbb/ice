from torch import Tensor
import torch.distributions as dist
import torch
from torch.nn.modules.module import Module
from torch.serialization import load


class ICELoss(Module):
    def __init__(self, max_bins, mu = 0, sigma = 1, device='cpu') -> None:
        super(ICELoss, self).__init__()
        self.quantiles = dist.Normal(mu, sigma).icdf(torch.arange(1, max_bins + 1)/(max_bins + 1)).to(device=device)
        self.epsilon =  1E-45

    def forward(self, input: Tensor, target: Tensor) -> Tensor:
        error = input.view(-1) - target.view(-1)
        effect = (error[:, None] - self.quantiles[None, :].to(error.device))/4
        distro = torch.exp(-0.5 * effect.pow(2)).sum(0)
        loss = -torch.log(distro).sum()
        return loss
