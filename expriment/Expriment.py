import torch
from datetime import datetime
from torch.utils.data.dataloader import DataLoader
from expriment.ICELoss import ICELoss
from expriment.LineDataset import LineDataset
from .mlp import Net
from tqdm import tqdm

class Expriment:
    def __init__(self, logger, sigma = 3, total = 30000, max_bins = 200, sampels = 200, loss = "ICE", device='cpu') -> None:
        self.sigma = sigma
        self.total = total
        self.loss = loss
        self.loss_functions = {
            "MSE": torch.nn.MSELoss(),
            "ICE": ICELoss(max_bins, 0, self.sigma, device)
        }
        self.net = Net(n_feature=1, n_hidden=50, n_output=1).to(device=device)
        self.optimizer = torch.optim.Adam(self.net.parameters(), lr=1E-4)
        self.ds = LineDataset(sampels, 2).to(device=device)
        self.logger = logger
        logger.run_name = f'expriment_{loss}_sigma_{str(sigma).replace(".", "_")}_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        # self.sampler = SlidingBatchSampler(SequentialSampler(self.ds), batch_size=20, drop_last=True)

    def fit(self):
        self.logger.log("points", self.toxy(self.ds[:-1][0].cpu().data.numpy(), self.ds[:-1][1].cpu().data.numpy()))
        self.logger.log("total", self.total)

        for t in tqdm(range(self.total)):
            for x, y in DataLoader(self.ds, batch_size=50, shuffle=True):
                prediction = self.net(x) 
                loss = self.loss_functions[self.loss](self.net(x), y)

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

            if t == 0 or t % 100 == 99:
                self.net.train(False)
                self.logger.log("netloss", float(loss.cpu().data.numpy()), t)
                loss = self.loss_functions["MSE"](prediction, y) 
                prediction = self.net(self.ds[:-1][0])
                self.logger.log("loss", float(loss.cpu().data.numpy()), t)
                self.logger.log("pred", self.toxy(self.ds[:-1][0].cpu().data.numpy(), prediction.cpu().data.numpy()), t)
                self.net.train()

    def save(self):
        self.logger.save()

    def toxy(self, xs, ys):
        return [{"x" : float(x[0]), "y" : float(y[0])} for x, y in zip(xs, ys)]