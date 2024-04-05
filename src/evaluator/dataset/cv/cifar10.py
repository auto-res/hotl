import torch
from torchvision import datasets, transforms


def cifar10_data(datasave_path):
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
