import torch
from torchvision import datasets, transforms

def cifar100_data(datasave_path):
    """
    Load and return the CIFAR-100 dataset.

    Args:
        datasave_path (str): The directory where the dataset will be saved.

    Returns:
        tuple: A tuple containing the trainloader and testloader for the CIFAR-100 dataset.
    """    
    transform = transforms.Compose(
        [transforms.ToTensor(),
         transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    trainset = datasets.CIFAR100(
        root=datasave_path, train=True,
        download=True, transform=transform)
    trainloader = torch.utils.data.DataLoader(
        trainset, batch_size=20, shuffle=True, num_workers=2)

    testset = datasets.CIFAR100(
        root=datasave_path, train=False,
        download=True, transform=transform)
    testloader = torch.utils.data.DataLoader(
        testset, batch_size=20, shuffle=False, num_workers=2)

    return trainloader, testloader