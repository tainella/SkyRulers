import torch
import torch.nn as nn

class NN(nn.Module):
    def __init__(self):
        super(NN,self).__init__()
        self.layer1=nn.Linear(X_train.shape[1], X_train.shape[1] * 3)
        self.layer2=nn.Linear(X_train.shape[1] * 3, X_train.shape[1] * 2)
        self.layer3=nn.Linear(X_train.shape[1] * 2, X_train.shape[1] // 2)
        self.layer4=nn.Linear(X_train.shape[1] // 2, y_train.shape[1])
        
    def forward(self,x):
        x=F.relu(self.layer1(x))
        x=F.relu(self.layer2(x))
        x=F.relu(self.layer3(x))
        x=self.layer4(x)
        return x

def train(training_loader):
    epochs=30
    for i in range(epochs):
        for x_batch, y_batch in training_loader:
            #initialize the model parameter
            optimizer.zero_grad(set_to_none = True)
            #calculate the loss
            output = model.forward(x_batch)
    #         print('output.shape', output.shape)
    #         print('y_batch', y_batch.shape)
            loss = loss_fn(output, y_batch)
            #backpropagation
            loss.backward()
            #update the parameters
            optimizer.step()
        if(i % 5 == 0):
            print(f"epochs: {i}......loss:{loss}")