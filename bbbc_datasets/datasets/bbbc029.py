from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


class BBBC029(BaseBBBCDataset):
    """
    BBBC029 Dataset: Synthetic Differential Interference Contrast (DIC) Images.

    - **Biological Application:**
      The dataset consists of synthetic DIC images used to evaluate DIC reconstruction algorithms.
      The accuracy of reconstruction can be measured using Mean Squared Error (MSE) between reconstructed and ground truth images.

    - **Images:**
      - 218 simulated DIC images of 20 different binary and grayscale objects with various rotations.
      - Available in both noise-free and 20 dB white Gaussian noise versions.
      - Includes the DIC point spread function.

    - **Segmentations:**
      - Ground truth images used for DIC image generation.
      - Ground truth is the same for noise-free and noisy DIC images.

    - **Source:** https://bbbc.broadinstitute.org/BBBC029
    """

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC029"

    def __init__(self):
        dataset_info = {
            "image_paths": [f"{self.BASE_URL}/images.zip"],
            "segmentation_path": f"{self.BASE_URL}/ground_truth.zip",
            "metadata_paths": [],
            "local_path": "data/BBBC029",
        }

        super().__init__("BBBC029", dataset_info)
