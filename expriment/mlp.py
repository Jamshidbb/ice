import torch
import torch.nn.functional as F


class Net(torch.nn.Module):
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net, self).__init__()
        self.hidden0 = torch.nn.Linear(n_feature, n_hidden)
        self.hidden1 = torch.nn.Linear(n_hidden, n_hidden)
        self.hidden2 = torch.nn.Linear(n_hidden, n_hidden)
        self.hidden3 = torch.nn.Linear(n_hidden, n_hidden)
        self.hidden4 = torch.nn.Linear(n_hidden, n_hidden)
        self.hidden5 = torch.nn.Linear(n_hidden, n_hidden)
        self.hidden6 = torch.nn.Linear(n_hidden, n_hidden)
        self.hidden7 = torch.nn.Linear(n_hidden, n_hidden)
        self.hidden8 = torch.nn.Linear(n_hidden, n_hidden)
        self.hidden9 = torch.nn.Linear(n_hidden, n_hidden)
        self.hidden10 = torch.nn.Linear(n_hidden, n_hidden)
        self.hidden11 = torch.nn.Linear(n_hidden, n_hidden)
        self.hidden12 = torch.nn.Linear(n_hidden, n_hidden)
        self.predict = torch.nn.Linear(n_hidden, n_output)

    def forward(self, x):
        x = F.relu(self.hidden0(x))
        x = F.relu(self.hidden1(x))
        x = F.relu(self.hidden2(x))
        x = F.relu(self.hidden3(x))
        x = F.relu(self.hidden4(x))
        x = F.relu(self.hidden5(x))
        x = F.relu(self.hidden6(x))
        x = F.relu(self.hidden7(x))
        x = F.relu(self.hidden8(x))
        x = F.relu(self.hidden9(x))
        x = F.relu(self.hidden10(x))
        x = F.relu(self.hidden11(x))
        x = F.relu(self.hidden12(x))
        x = self.predict(x)
        return x