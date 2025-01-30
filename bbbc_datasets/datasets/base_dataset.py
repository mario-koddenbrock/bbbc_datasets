import os
import zipfile

import requests


class BaseBBBCDataset:
    """
    Base class for BBBC datasets, handling downloading, extraction, and file management.

    - Automatically downloads dataset files if they are not available locally.
    - Stores datasets in a shared system-wide folder (`/opt/bbbc_datasets/` or `~/.bbbc_datasets/`).
    - Supports structured access to images, segmentations, and metadata.
    """

    # Define a shared system-wide storage location
    GLOBAL_STORAGE_PATH = os.path.expanduser("~/.bbbc_datasets/")

    def __init__(self, dataset_name, dataset_info):
        """
        Initialize the dataset with name and file paths.

        :param dataset_name: The name of the dataset (e.g., "BBBC003").
        :param dataset_info: Dictionary containing paths to images, segmentation masks, and metadata.
        """
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
            if key.endswith("_path") or key.endswith("_paths"):
                if isinstance(urls, list):
                    for url in urls:
                        self._download_and_extract(url)
                elif urls:
                    self._download_and_extract(urls)

    def _download_and_extract(self, url):
        """
        Downloads and extracts a dataset file if it is missing.
        """
        if not url.startswith("http"):
            return  # Skip invalid URLs

        filename = os.path.join(self.local_path, os.path.basename(url))
        if not os.path.exists(filename):
            print(f"Downloading {filename}...")
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(filename, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                print(f"Downloaded {filename}")

                # Extract if it's a zip file
                if filename.endswith(".zip"):
                    self._extract_zip(filename)

            else:
                print(f"Failed to download {url}")

    def _extract_zip(self, zip_path):
        """
        Extracts a zip file to the dataset directory.
        """
        print(f"Extracting {zip_path}...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(self.local_path)
        print(f"Extracted to {self.local_path}")

    def get_image_paths(self):
        """
        Returns the list of image file paths.
        """
        return self._list_files(subdir="images")

    def get_segmentation_path(self):
        """
        Returns the segmentation mask file path (if available).
        """
        return self._list_files(subdir="segmentation")

    def get_metadata_paths(self):
        """
        Returns the metadata file paths (if available).
        """
        return self._list_files(subdir="metadata")

    def _list_files(self, subdir):
        """
        Returns a list of files in a specific dataset subdirectory.
        """
        dir_path = os.path.join(self.local_path, subdir)
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
