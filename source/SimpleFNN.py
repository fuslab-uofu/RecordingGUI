from torch import nn
import torch

class Identity(nn.Module):
    def __init(self):
        super.__init__()

    def forward(self, x):

        return x


class FNN(nn.Module):
    def __init__(self, n_inputs, n_outputs, n_layers, n_npl):
        super().__init__()

        self.layers = nn.ModuleList()
        self.activations = nn.ModuleList()

        # First Layer
        self.n_inps = n_inputs
        self.layers.append(nn.Linear(n_inputs, n_npl))
        # self.activations.append(nn.ReLU())
        self.activations.append(nn.Tanh())
        # self.activations.append(Identity())

        if n_layers > 2:
            for x in range(n_layers-2):
                self.layers.append(nn.Linear(n_npl, n_npl))
                self.activations.append(nn.Tanh())
                # self.activations.append(nn.ReLU())
                # self.activations.append(Identity())

        self.layers.append(nn.Linear(n_npl , n_outputs))
        # self.activations.append(nn.Sigmoid())
        self.activations.append(nn.Softmax())
        # self.activations.append(Identity())

    '''
    Forward pass - Simple fully connected network with given activations
    '''
    def forward(self, x):
        out = x
        for i in range(len(self.layers)):
            out = self.layers[i](out)
            out = self.activations[i](out)

        return out



    '''
    Saves the model in the specified path and name with .pth extension
    '''
    def save(self, path):
        torch.save(self.state_dict(), path)

    '''
    Loads the model given its path.
    Different Architecture or activation function (with parameters) in the saved model will throw an error
    '''
    def load(self, path):
        self.load_state_dict(torch.load(path))


