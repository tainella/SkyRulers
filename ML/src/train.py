import os
import pandas as pd

import torch
import torch.nn as nn

import torch.nn.functional as F
import torch.optim as optim

#custom modules
import preprocess
from EngineDataset import EngineDataset

def train_save(filename, model):
    df = pd.read_csv(filename)
    df = preprocess.preprocess_file(df, 0.95)
    
    training_set = EngineDataset(X_train, y_train)
    training_loader = torch.utils.data.DataLoader(training_set, batch_size = 32)
    
    model.train()
    

