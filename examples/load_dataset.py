import os

import matplotlib.pyplot as plt
import numpy as np

from bbbc_datasets.utils.file_io import load_image
from bbbc_datasets.utils.general import filter_datasets
from tests import DATASETS  # Import shared dataset list


def list_available_datasets(filter_3d=None):
    """
    Lists all available BBBC datasets without downloading them.
    :param filter_3d: If True, lists only 3D datasets. If False, lists only 2D datasets. If None, lists all datasets.
    """
    print("📂 Available BBBC Datasets:")
    filtered_datasets = filter_datasets(DATASETS, filter_3d)
    for dataset_cls in filtered_datasets:
        print(
            f"- {dataset_cls.__name__}: {dataset_cls.__doc__.splitlines()[1].strip()}"
        )


def display_dataset_samples(filter_3d=None):
    """
    Loops through all datasets, loads the first image and label, and displays them.
    :param filter_3d: If True, displays only 3D datasets. If False, displays only 2D datasets. If None, displays all datasets.
    """
    filtered_datasets = filter_datasets(DATASETS, filter_3d)
    for dataset_cls in filtered_datasets:

        dataset = dataset_cls()

        image_paths = dataset.get_image_paths()

        print(
            f"Dataset: {dataset_cls.__name__} ({len(image_paths)} images, 3D={dataset.is_3d})"
        )

        if not image_paths:
            print(f"Skipping {dataset_cls.__name__} (No images found)")
            continue

        # Load the first image
        image_path = image_paths[0]
        image = load_image(image_path)

        # Load segmentation (if available)
        label = dataset.get_label(image_path)

        # Extract middle slice from 3D images
        if dataset.is_3d:
            mid_slice = image.shape[0] // 2  # Middle slice
            image = image[mid_slice]
            label = label[mid_slice]

        # Display images
        fig, axes = plt.subplots(1, 2 if label is not None else 1, figsize=(10, 5))
        axes = (
            [axes] if not isinstance(axes, np.ndarray) else axes
        )  # Handle single-axis case

        axes[0].imshow(image, cmap="gray")
        axes[0].set_title(f"{dataset_cls.__name__} - Image")
        axes[0].axis("off")

        if label is not None:
            axes[1].imshow(label, cmap="jet", alpha=0.5)
            axes[1].set_title(f"{dataset_cls.__name__} - Label")
            axes[1].axis("off")

        plt.show()


if __name__ == "__main__":
    list_available_datasets()
    display_dataset_samples()
