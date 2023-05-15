import torch

class EngineDataset:
    def __init__(self, features, targets):
        self.features = features
        self.labels = targets

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        feat_ = torch.tensor(self.features[idx], dtype=torch.float)
        label_ = torch.tensor(self.labels[idx], dtype=torch.float)
        return feat_, label_