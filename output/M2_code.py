
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

def gradient_descent_with_adam_and_weight_decay(objective, params, lr, beta1, beta2, m, v, weight_decay, epsilon):
    # Compute gradient with optional weight decay
    gradient = np.gradient(objective(params), params)
    if weight_decay != 0:
        gradient += weight_decay * params

    # Update parameters using Adam
    m = beta1 * m + (1 - beta1) * gradient  # Update first moment estimate
    v = beta2 * v + (1 - beta2) * (gradient**2)  # Update second moment estimate
    m_hat = m / (1 - beta1)  # Bias correction for first moment
    v_hat = v / (1 - beta2)  # Bias correction for second moment
    params -= lr * m_hat / (np.sqrt(v_hat) + epsilon)  # Update parameters

    return params, m, v

def train(trainloader, params, device):
    net = Net()
    net.to(device)  # Move the model to the specified device

    criterion = nn.CrossEntropyLoss()
    # Replace Adam optimizer with custom gradient descent with Adam and optional weight decay
    # optimizer = optim.Adam(net.parameters(), lr=params['lr'])
    m, v = 0, 0  # Initialize first and second moment vectors
    beta1, beta2 = 0.9, 0.999  # Hyperparameters for Adam
    epsilon = 1e-8  # Small number to prevent division by zero
    weight_decay = params.get('weight_decay', 0)  # Optional weight decay

    for epoch in range(1):  # loop over the dataset multiple times
        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            inputs, labels = data[0].to(device), data[1].to(device)  # Move inputs and labels to the specified device

            # optimizer.zero_grad()  # zero the parameter gradients
            # Custom gradient descent with Adam and optional weight decay does not use optimizer.zero_grad()

            outputs = net(inputs)  # forward + backward + optimize
            loss = criterion(outputs, labels)
            loss.backward()
            # optimizer.step()
            # Custom update step using gradient descent with Adam and optional weight decay
            for param in net.parameters():
                if param.grad is not None:
                    grad = param.grad.data.cpu().numpy()
                    updated_param, m, v = gradient_descent_with_adam_and_weight_decay(
                        lambda p: loss.item(), param.data.cpu().numpy(), params['lr'], beta1, beta2, m, v, weight_decay, epsilon
                    )
                    param.data = torch.from_numpy(updated_param).to(device)

            running_loss += loss.item()
            if i % 2000 == 1999:  # print every 2000 mini-batches
                running_loss = 0.0

    return net

def test(net, testloader, device):
    all_outputs = []

    with torch.no_grad():
        for data in testloader:
            images, labels = data[0].to(device), data[1].to(device)  # Move images to the specified device
            outputs = net(images)
            probabilities = F.softmax(outputs, dim=1)
            probabilities_np = probabilities.cpu().numpy().tolist()  # Move the probabilities back to CPU for numpy conversion
            all_outputs.extend(probabilities_np)

    all_outputs_np = np.array(all_outputs)
    return all_outputs_np

def model(trainloader, testloader, params):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net = train(trainloader, params, device)
    y_pred = test(net, testloader, device)
    return y_pred
