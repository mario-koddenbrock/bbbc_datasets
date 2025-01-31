import os

import matplotlib.pyplot as plt
import numpy as np

from bbbc_datasets.utils.file_io import load_image
from tests import DATASETS  # Import shared dataset list


def display_dataset_samples():
    """
    Loops through all datasets, loads the first image and label, and displays them.
    """
    for dataset_cls in DATASETS:
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
    display_dataset_samples()
