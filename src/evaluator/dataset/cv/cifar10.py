import torch
from torchvision import datasets, transforms


def cifar10_data(datasave_path):
    """Load CIFAR-10 dataset and return data loaders for training and testing.

    Args:
        datasave_path (str): The directory where the CIFAR-10 dataset will be saved.

    Returns:
        tuple: A tuple containing the training data loader and the testing data loader.
    """    
    transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
    )

    trainset = datasets.CIFAR10(
        root=datasave_path, train=True, download=True, transform=transform
    )
    trainloader = torch.utils.data.DataLoader(
        trainset, batch_size=20, shuffle=True, num_workers=2
    )

    testset = datasets.CIFAR10(
        root=datasave_path, train=False, download=True, transform=transform
    )
    testloader = torch.utils.data.DataLoader(
        testset, batch_size=20, shuffle=False, num_workers=2
    )
    return trainloader, testloader
