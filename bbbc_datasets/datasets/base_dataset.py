import os
import zipfile
import difflib

import pandas as pd
import numpy as np
import requests
from tqdm import tqdm

from bbbc_datasets.utils.file_io import load_image


class BaseBBBCDataset:
    """
    Base class for BBBC datasets, handling downloading, extraction, and file management.

    - Automatically downloads dataset files if they are not available locally.
    - Stores datasets in a shared system-wide folder (`/opt/bbbc_datasets/` or `~/.bbbc_datasets/`).
    - Supports structured access to images, labels, and metadata.
    """

    # Define a shared system-wide storage location
    DEFAULT_PATH = os.path.expanduser("~/.bbbc_datasets/")
    IMAGE_SUBDIR = "images"
    LABEL_SUBDIR = "labels"

    IMAGE_FILTER = [".png", ".jpg", ".jpeg", ".tif", ".tiff", ".ics"]

    local_path = None
    label_path = None
    image_paths = None
    is_3d = False

    def __init__(self, dataset_name, download_dir=None):
        """
        Initialize the dataset with name and file paths.

        :param dataset_name: The name of the dataset (e.g., "BBBC003").
        :param dataset_info: Dictionary containing paths to images, label masks, and metadata.
        """
        self.ground_truth = None
        self.dataset_name = dataset_name

        if not self.local_path:
            raise ValueError("local_path not defined")

        # Ensure the dataset directory exists in the shared location
        os.makedirs(self.local_path, exist_ok=True)

        if not download_dir:
            self.download_dir = self.DEFAULT_PATH
        else:
            self.download_dir = download_dir

        # Download missing files
        self._download_files()

        if self.label_path and isinstance(self.label_path, str):
            local_file, unzip_folder = self.get_download_folder(
                self.label_path, "label_path"
            )
            if self.label_path.endswith(".csv"):
                self.ground_truth = local_file
            elif self.label_path.endswith(".tif"):
                self.ground_truth = local_file

    def _download_files(self):
        """
        Checks for missing dataset files and downloads them if necessary.
        """

        if isinstance(self.image_paths, list):
            for url in self.image_paths:
                self._download_and_extract("image", url)
        elif self.image_paths:
            self._download_and_extract("image", self.image_paths)

        if isinstance(self.label_path, list):
            for url in self.label_path:
                self._download_and_extract("label", url)
        elif self.label_path:
            self._download_and_extract("label", self.label_path)

    def _download_and_extract(self, key, url):
        """
        Downloads and extracts a dataset file if it is missing.
        """
        if not url.startswith("http"):
            raise ValueError("url must start with http://")

        local_file, unzip_folder = self.get_download_folder(url, key)

        if not os.path.exists(local_file):
            print(f"Downloading {local_file}...")
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                total_size = int(response.headers.get("content-length", 0))
                with open(local_file, "wb") as f, tqdm(
                    desc=local_file,
                    total=total_size,
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                ) as bar:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            bar.update(len(chunk))
            else:
                raise FileNotFoundError(f"Failed to download {url}")

        if os.path.exists(local_file) and not os.path.exists(unzip_folder):
            # Extract if it's a zip file
            if local_file.endswith(".zip"):
                self._extract_zip(local_file, unzip_folder)

    def get_download_folder(self, url, key):
        local_file = os.path.join(self.local_path, os.path.basename(url))
        folder_name = self.IMAGE_SUBDIR if "image" in key else self.LABEL_SUBDIR
        unzip_folder = os.path.join(self.local_path, folder_name)
        return local_file, unzip_folder

    def _extract_zip(self, zip_path, extract_to=None):
        """
        Extracts a zip file to the specified directory or the dataset directory.
        """
        target_path = extract_to if extract_to else self.local_path
        print(f"Extracting {zip_path} to {target_path}...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(target_path)

    def _get_paths(self, subdir, recursive=True):
        """
        Returns the list of image file paths.
        """

        dir_path = os.path.join(self.local_path, subdir)
        files = self._list_files(dir_path=dir_path)

        # recursively search for images in the list of files
        if recursive:
            for file in files:
                if os.path.isdir(file):
                    files.extend(self._list_files(dir_path=file))

        images = [f for f in files if f.lower().endswith(tuple(self.IMAGE_FILTER))]
        return images

    def get_image_paths(self):
        """
        Returns the list of image file paths.
        """
        images = self._get_paths(self.IMAGE_SUBDIR)
        return images

    def get_label(self, image_path):
        """
        Returns the label mask for a given image path.
        """
        if self.ground_truth:
            if self.ground_truth.endswith(".tif"):
                return load_image(self.ground_truth)
            elif self.ground_truth.endswith(".csv"):
                gt_all = pd.read_csv(self.ground_truth)
                image_id = os.path.basename(image_path).split(".")[0]
                gt_image = gt_all[gt_all["ImageId"] == image_id]
                pixels = gt_image["EncodedPixels"]

                image = load_image(image_path)
                labels = np.zeros_like(image)

                for pxls in pixels:
                    if isinstance(pxls, str):
                        pxls = pxls.split(" ")
                        pxls = [int(p) for p in pxls]
                        for i in range(0, len(pxls), 2):
                            labels[pxls[i] : pxls[i + 1]] = 1
                return labels
            else:
                raise NotImplementedError("Label type not supported.")

        # Find the corresponding label mask
        label_paths = self.get_label_paths()

        if not label_paths:
            return None

        # find the label path the most similar to the image path
        label_path = difflib.get_close_matches(
            image_path, label_paths, n=1, cutoff=0.25
        )

        if not label_path:
            raise FileNotFoundError(f"Label mask not found for {image_path}")
        else:
            label_path = label_path[0]

        if os.path.exists(label_path):
            return load_image(label_path)
        else:
            raise FileNotFoundError(f"Label mask not found for {image_path}")

    def get_label_paths(self):
        """
        Returns the label mask file path (if available).
        """
        images = self._get_paths(self.LABEL_SUBDIR)
        return images

    def get_metadata_paths(self):
        """
        Returns the metadata file paths (if available).
        """
        dir_path = os.path.join(self.local_path, "metadata")
        return self._list_files(dir_path=dir_path)

    def _list_files(self, dir_path):
        """
        Returns a list of files in a specific dataset subdirectory.
        """

        if os.path.exists(dir_path):
            return [os.path.join(dir_path, f) for f in os.listdir(dir_path)]
        return []

    @staticmethod
    def validate_url(url):
        """
        Checks if a given URL is reachable.
        """
        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False
