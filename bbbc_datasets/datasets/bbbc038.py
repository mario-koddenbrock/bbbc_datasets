import os

import numpy as np

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset
from bbbc_datasets.utils.file_io import load_image


class BBBC038(BaseBBBCDataset):
    """
    BBBC038 Dataset: Kaggle 2018 Data Science Bowl - Nuclei Segmentation.

    - **Biological Application:**
      This dataset was created for the Kaggle 2018 Data Science Bowl to challenge segmentation algorithms
      in detecting and segmenting nuclei across a diverse range of biological contexts.
      The dataset includes thousands of images containing nuclei from various organisms, imaging techniques,
      and experimental conditions.

    - **Images:**
      - The dataset includes images from multiple sources, including human, mouse, and fly samples.
      - Nuclei appear in different contexts such as cultured monolayers, tissues, and embryos.
      - Imaging techniques include fluorescent and histology stains.
      - The dataset is divided into:
        - **Stage 1 Training Set:** Includes images and corresponding segmentation masks.
        - **Stage 1 Test Set:** Unlabeled images for testing.
        - **Stage 2 Test Set:** Additional test images, including conditions not present in Stage 1.

    - **Segmentations:**
      - Ground truth segmentation masks are provided for each nucleus separately.
      - Masks do not overlap (each pixel belongs to only one mask).
      - Labels and annotations available as CSV files.

    - **Metadata:**
      - Includes additional annotations and ground truth solutions for test sets.

    - **Source:** https://bbbc.broadinstitute.org/BBBC038
    """

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC038"

    def __init__(self, *args, **kwargs):
        """
        Initialize the dataset for a specific dataset version.

        """

        self.IMAGE_SUBDIR = "all"
        self.local_path = os.path.join(self.download_dir, "BBBC038")
        self.image_paths = [
            "https://github.com/lopuhin/kaggle-dsbowl-2018-dataset-fixes/archive/refs/heads/master.zip"
        ]
        self.label_path = None
        self.metadata_paths = None
        self.is_3d = False

        super().__init__("BBBC038", *args, **kwargs)

    def get_image_paths(self):
        """
        Returns the list of image file paths.
        """
        images = self._get_paths(self.IMAGE_SUBDIR)

        # filter images that do not conatin the word "masks"
        images = [image for image in images if "masks" not in image]

        return images

    def get_label(self, image_path):
        """
        Returns the label mask for a given image path.
        """

        parent_folder = os.path.dirname(image_path)
        mask_folder = parent_folder.replace("images", "masks")

        # read the corresponding masks
        mask_files = os.listdir(mask_folder)

        image = load_image(image_path)
        mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
        for idx, mask_file in enumerate(mask_files):
            current_mask = load_image(os.path.join(mask_folder, mask_file))

            # setting all the pixels in the mask to the index of the mask
            mask[current_mask > 0] = idx + 1

        return mask
