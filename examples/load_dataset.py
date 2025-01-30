import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
import tifffile as tiff

from tests import DATASETS  # Import shared dataset list


def load_image(image_path):
    """
    Loads an image (2D or 3D) and converts it to a displayable format.
    - If the image is 3D (e.g., TIFF stack), it extracts the middle slice.
    - If the image is grayscale, it normalizes it for display.
    """
    if image_path.endswith(".tif") or image_path.endswith(".tiff"):
        img = tiff.imread(image_path)
    else:
        img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    if img is None:
        print(f"Error: Could not read image {image_path}")
        return None

    # Handle 3D images by extracting the middle Z-slice
    if len(img.shape) == 3:
        mid_slice = img.shape[0] // 2  # Middle slice
        img = img[mid_slice]

    # Normalize grayscale images
    if len(img.shape) == 2:  # Grayscale image
        img = (img - np.min(img)) / (np.max(img) - np.min(img) + 1e-8)  # Normalize

    return img


def display_dataset_samples():
    """
    Loops through all datasets, loads the first image and label, and displays them.
    """
    for dataset_cls in DATASETS:
        dataset = dataset_cls()

        image_paths = dataset.get_image_paths()
        segmentation_path = dataset.get_segmentation_path()

        if not image_paths:
            print(f"Skipping {dataset_cls.__name__} (No images found)")
            continue

        # Load the first image
        image_path = image_paths[0]
        image = load_image(image_path)

        # Load segmentation (if available)
        label = None
        if segmentation_path and os.path.exists(segmentation_path):
            label = load_image(segmentation_path)

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
