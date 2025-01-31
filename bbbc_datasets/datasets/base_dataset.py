import os
import zipfile

import requests
from tqdm import tqdm


class BaseBBBCDataset:
    """
    Base class for BBBC datasets, handling downloading, extraction, and file management.

    - Automatically downloads dataset files if they are not available locally.
    - Stores datasets in a shared system-wide folder (`/opt/bbbc_datasets/` or `~/.bbbc_datasets/`).
    - Supports structured access to images, labels, and metadata.
    """

    # Define a shared system-wide storage location
    GLOBAL_STORAGE_PATH = os.path.expanduser("~/.bbbc_datasets/")
    IMAGE_SUBDIR = "images"
    LABEL_SUBDIR = "labels"

    IMAGE_FILTER = [".png", ".jpg", ".jpeg", ".tif", ".tiff", ".ics"]

    def __init__(self, dataset_name, dataset_info):
        """
        Initialize the dataset with name and file paths.

        :param dataset_name: The name of the dataset (e.g., "BBBC003").
        :param dataset_info: Dictionary containing paths to images, label masks, and metadata.
        """
        self.ground_truth = None
        self.dataset_name = dataset_name
        self.dataset_info = dataset_info
        self.local_path = os.path.join(self.GLOBAL_STORAGE_PATH, dataset_name)

        # Ensure the dataset directory exists in the shared location
        os.makedirs(self.local_path, exist_ok=True)

        # Download missing files
        self._download_files()

    def _download_files(self):
        """
        Checks for missing dataset files and downloads them if necessary.
        """
        for key, urls in self.dataset_info.items():

            # always ignore local_path
            if key == "local_path":
                continue

            # ifnore empty values
            if not urls:
                continue

            # ignore metadata_paths for now
            if key == "metadata_paths":
                continue

            if key.endswith("_path") or key.endswith("_paths"):
                if isinstance(urls, list):
                    for url in urls:
                        self._download_and_extract(key, url)
                elif urls:
                    self._download_and_extract(key, urls)

    def _download_and_extract(self, key, url):
        """
        Downloads and extracts a dataset file if it is missing.
        """
        if not url.startswith("http"):
            return  # Skip invalid URLs

        filename = os.path.join(self.local_path, os.path.basename(url))
        target_folder = self.IMAGE_SUBDIR if "image" in key else self.LABEL_SUBDIR
        target_path = os.path.join(self.local_path, target_folder)

        if not os.path.exists(filename):
            print(f"Downloading {filename}...")
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                total_size = int(response.headers.get("content-length", 0))
                with open(filename, "wb") as f, tqdm(
                    desc=filename,
                    total=total_size,
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                ) as bar:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            bar.update(len(chunk))

        if os.path.exists(filename) and not os.path.exists(target_path):
            # Extract if it's a zip file
            if filename.endswith(".zip"):
                self._extract_zip(filename, target_path)
            elif filename.endswith(".csv"):
                self.ground_truth = filename
            elif filename.endswith(".tif"):
                self.ground_truth = filename
            else:
                print(f"Failed to download {url}")

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
