import os

import cv2
import numpy as np
import tifffile as tiff
import torch
from PIL import Image
from torch.utils.data import Dataset

from tests import DATASETS  # Import shared dataset list


def _human_bytes(size):
    """Formats a byte count as a human readable string."""
    size = float(size)
    for unit in ("B", "kB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return f"{size:,.0f} B" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


class BBBCDataset(Dataset):
    """
    PyTorch-compatible dataset for loading BBBC datasets with full 3D support.

    - Supports both 2D and 3D images.
    - Optionally applies transformations (PyTorch `torchvision.transforms`).
    - Returns (image, label) pairs where available.

    Args:
        dataset_cls: The BBBC dataset class to load.
        transform (callable, optional): Optional transform to apply to images.
        target_transform (callable, optional): Optional transform for labels.
    """

    def __init__(self, dataset_cls, transform=None, target_transform=None):
        self.dataset = dataset_cls()
        self.image_paths = self.dataset.get_image_paths()
        self.label_paths = self.dataset.get_label_paths()

        if not self.image_paths:
            raise RuntimeError(f"No images found in {dataset_cls.__name__}")

        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        image = self.load_image(image_path)

        label = None
        label_array = self.dataset.get_label(image_path)
        if label_array is not None:
            label = self.array_to_tensor(np.asarray(label_array))

        # Apply transforms if provided
        if self.transform:
            image = self.transform(image)
        if self.target_transform and label is not None:
            label = self.target_transform(label)

        return image, label

    def load_image(self, image_path):
        """
        Loads an image (2D or full 3D) and converts it to a PyTorch tensor.
        """
        ext = image_path.lower()
        if ext.endswith((".tif", ".tiff")):
            try:
                img = tiff.imread(image_path)  # Load 3D TIFF or 2D image
            except Exception:
                # Some (older) TIFFs are not fully conformant; PIL is more lenient.
                img = np.array(Image.open(image_path))
        elif ext.endswith(".dib"):
            img = np.array(Image.open(image_path))  # ArrayScan DIB (BMP)
        else:
            img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)  # Load 2D image

        if img is None:
            raise ValueError(f"Error: Could not read image {image_path}")

        return self.array_to_tensor(img)

    @staticmethod
    def array_to_tensor(img):
        """
        Normalizes a 2D/3D/RGB numpy array to [0, 1] and converts it to a tensor.
        """
        # Convert to float first (also handles 1-bit/bool masks)
        img = np.asarray(img).astype(np.float32)

        # Normalize to [0, 1]
        img = (img - np.min(img)) / (np.max(img) - np.min(img) + 1e-8)

        # Convert to tensor
        if len(img.shape) == 2:  # 2D grayscale image
            img = torch.tensor(img, dtype=torch.float32).unsqueeze(0)  # (C, H, W)
        elif len(img.shape) == 3:
            if img.shape[2] in (3, 4):  # (H, W, C) color image
                img = torch.tensor(img, dtype=torch.float32).permute(2, 0, 1)  # (C, H, W)
            else:  # 3D volume (Z, H, W)
                img = torch.tensor(img, dtype=torch.float32).unsqueeze(0)  # (C, Z, H, W)
        elif len(img.shape) == 4:
            if img.shape[3] in (3, 4):  # (Z, H, W, C) color volume
                img = torch.tensor(img, dtype=torch.float32).permute(3, 0, 1, 2)  # (C, Z, H, W)
            else:  # (C, Z, H, W) channel-first volume
                img = torch.tensor(img, dtype=torch.float32)

        return img


class DatasetManager:
    """
    Manages all BBBC datasets and provides utilities.

    - Lists available datasets.
    - Loads datasets dynamically as PyTorch Datasets.
    - Displays dataset information.
    """

    @staticmethod
    def list_available_datasets(filter_3d=None):
        """
        Lists all available BBBC datasets without downloading them.
        :param filter_3d: If True, lists only 3D datasets. If False, lists only 2D datasets. If None, lists all datasets.
        """
        print("📂 Available BBBC Datasets:")
        filtered_datasets = DatasetManager.filter_datasets(filter_3d)
        for dataset_cls in filtered_datasets:
            print(
                f"- {dataset_cls.__name__}: {dataset_cls.__doc__.splitlines()[1].strip()}"
            )

    @staticmethod
    def get_dataset(name, transform=None, target_transform=None):
        """
        Loads a dataset by name.

        Args:
            name (str): The dataset class name (e.g., "BBBC003").
            transform: Optional image transformations.
            target_transform: Optional label transformations.

        Returns:
            BBBCDataset instance.
        """
        for dataset_cls in DATASETS:
            if dataset_cls.__name__ == name:
                return BBBCDataset(dataset_cls, transform, target_transform)

        raise ValueError(
            f"Dataset {name} not found. Use DatasetManager.list_datasets() to see available datasets."
        )

    @staticmethod
    def get_metadata(name):
        """
        Returns the fixed-schema ``DatasetMetadata`` of a dataset
        (see ``bbbc_datasets.metadata``) without downloading anything.

        Args:
            name (str): The dataset class name (e.g., "BBBC019").

        Returns:
            DatasetMetadata
        """
        for dataset_cls in DATASETS:
            if dataset_cls.__name__ == name:
                return dataset_cls.METADATA

        raise ValueError(
            f"Dataset {name} not found. Use DatasetManager.list_available_datasets() to see available datasets."
        )

    @staticmethod
    def get_dataset_info(name):
        """
        Returns metadata about a dataset (declared files, remote sizes,
        local download state) without downloading anything.

        This uses the default dataset configuration. For a specific
        variant (e.g. a single BBBC019 subset), construct the class
        yourself with download_files=False and call
        ``instance.get_dataset_info()`` instead.

        Args:
            name (str): The dataset class name (e.g., "BBBC019").

        Returns:
            dict: See ``BaseBBBCDataset.get_dataset_info()``.
        """
        for dataset_cls in DATASETS:
            if dataset_cls.__name__ == name:
                return dataset_cls(download_files=False).get_dataset_info()

        raise ValueError(
            f"Dataset {name} not found. Use DatasetManager.list_available_datasets() to see available datasets."
        )

    @staticmethod
    def describe_dataset(name):
        """
        Prints a human-readable summary of a dataset without downloading it.

        Shows the description, 2D/3D type, local storage path, download
        state, every declared file with its size and reachability, and
        the total download size (when all sizes are known).

        Args:
            name (str): The dataset class name (e.g., "BBBC044").
        """
        info = DatasetManager.get_dataset_info(name)

        state = "downloaded" if info["downloaded"] else "not downloaded"
        if info["local_size"]:
            state += f" ({_human_bytes(info['local_size'])} local)"

        meta = info["metadata"]
        print(f"📋 {info['name']} ({info['key']}) — {info['description']}")
        print(f"   Type:     {'3D' if info['is_3d'] else '2D'}")
        print(f"   Mode:     {meta.imaging_mode}, {meta.modality}")
        print(
            f"   Content:  {meta.data_type}, {meta.n_images} images, "
            f"task={meta.task}, labels={meta.label_type or 'none'}"
        )
        if meta.instrument:
            print(f"   Instrument: {meta.instrument}")
        if meta.doi or meta.license:
            print(f"   Reference:  {' '.join(x for x in (meta.doi and f'doi:{meta.doi}', meta.license) if x)}")
        print(f"   Location: {info['local_path']}")
        print(f"   Status:   {state}")
        print("   Files:")
        for file_info in info["files"]:
            mark = "✓" if file_info["reachable"] else "✗"
            size = (
                _human_bytes(file_info["size"])
                if file_info["size"] is not None
                else "unknown size"
            )
            local = "  (local)" if file_info["local"] else ""
            print(
                f"     [{file_info['role']:<8}] "
                f"{os.path.basename(file_info['url']):<36} "
                f"{size:>12}  {mark}{local}"
            )
        if info["total_remote_size"] is not None:
            print(f"   Total download: {_human_bytes(info['total_remote_size'])}")

    @staticmethod
    def gallery(output_dir="gallery", names=None, examples=3, max_size=300, with_labels=True):
        """
        Generates downscaled example images for each dataset into
        ``<output_dir>/<name>/example-<i>.png`` (image side by side
        with its label mask when available).

        Args:
            output_dir: Directory to write the thumbnails into.
            names: Dataset class names (default: all datasets).
            examples: Number of example images per dataset.
            max_size: Longest side of each rendered panel in pixels.
            with_labels: Whether to append the label mask when available.

        Returns:
            dict mapping dataset name to the saved file paths (empty
            list when the dataset is not downloaded locally).
        """
        from bbbc_datasets.gallery import save_gallery

        return save_gallery(
            output_dir,
            names=names,
            examples=examples,
            max_size=max_size,
            with_labels=with_labels,
        )

    @staticmethod
    def filter_datasets(filter_3d=None, **metadata_filters):
        """
        Filters the datasets by their fixed metadata
        (see ``bbbc_datasets.metadata.DatasetMetadata``) without
        instantiating or downloading anything.

        Args:
            filter_3d: Legacy shorthand — ``True`` keeps 3D datasets,
                ``False`` keeps 2D ones. Cannot be combined with ``dim``.
            **metadata_filters: Exact matches on any metadata field,
                e.g. ``data_type="synthetic"``, ``imaging_mode="dic"``,
                ``label_type="foreground"``, ``task="counting"``.
                Unknown field names raise ValueError.

        Returns:
            Filtered list of dataset classes.
        """
        if filter_3d is not None:
            if "dim" in metadata_filters:
                raise ValueError("Use either filter_3d or dim=, not both")
            metadata_filters["dim"] = "3D" if filter_3d else "2D"
        return [
            dataset_cls
            for dataset_cls in DATASETS
            if dataset_cls.METADATA.matches(**metadata_filters)
        ]


if __name__ == "__main__":
    # Example Usage
    DatasetManager.list_available_datasets()

    # Load a dataset
    dataset = DatasetManager.get_dataset("BBBC003")
    print(f"\nLoaded {len(dataset)} samples from BBBC003")
