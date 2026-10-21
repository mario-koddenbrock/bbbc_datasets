import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset
from bbbc_datasets.metadata import DatasetMetadata


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

    METADATA = DatasetMetadata(
        name="BBBC029",
        title="BBBC029 Dataset: Synthetic Differential Interference Contrast (DIC) Images.",
        source="https://bbbc.broadinstitute.org/BBBC029",
        dim="2D",
        imaging_mode="dic",
        modality="grayscale",
        resolution_um=None,
        image_size=None,
        data_type="synthetic",
        instrument=None,
        n_images=218,
        task="segmentation",
        label_type="foreground",
        doi=None,
        license=None,
    )

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC029"

    def __init__(self, *args, **kwargs):
        self.KEY = "BBBC029"
        self.image_paths = [os.path.join(self.BASE_URL, "images.zip")]
        self.label_path = os.path.join(self.BASE_URL, "ground_truth.zip")
        self.metadata_paths = None
        self.is_3d = False

        super().__init__(*args, **kwargs)
