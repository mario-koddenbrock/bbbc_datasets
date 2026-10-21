import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset
from bbbc_datasets.metadata import DatasetMetadata


class BBBC005(BaseBBBCDataset):
    """
    BBBC005 Dataset: Simulated fluorescence microscopy images with varying focus blur.

    - **Biological Application:**
      Evaluates the impact of focus blur on foreground/background segmentation in high-content screening.

    - **Images:**
      - 19,200 images with different levels of focus blur.
      - Simulated using the SIMCEP platform.
      - Plate layout nomenclature:
        - **Row** = Blur level
        - **Column** = Cell count.

    - **Segmentations:**
      - Ground truth masks available for fully in-focus images (**F1** files).
      - Stored as binary masks (white = foreground, black = background).

    - **Metadata:**
      - Cell counts and blur levels are encoded in image filenames.
      - Additional metadata is stored in `BBBC005_results_bray.csv`.

    - **Source:** https://bbbc.broadinstitute.org/BBBC005
    """

    METADATA = DatasetMetadata(
        name="BBBC005",
        title="BBBC005 Dataset: Simulated fluorescence microscopy images with varying focus blur.",
        source="https://bbbc.broadinstitute.org/BBBC005",
        dim="2D",
        imaging_mode="fluorescence",
        modality="grayscale",
        resolution_um=None,
        image_size=None,
        data_type="synthetic",
        instrument=None,
        n_images=19200,
        task="segmentation",
        label_type="foreground",
        doi=None,
        license=None,
    )

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC005"

    def __init__(self, *args, **kwargs):
        self.KEY = "BBBC005"
        self.image_paths = [os.path.join(self.BASE_URL, "BBBC005_v1_images.zip")]
        self.label_path = os.path.join(self.BASE_URL, "BBBC005_v1_ground_truth.zip")
        self.metadata_paths = [os.path.join(self.BASE_URL, "BBBC005_results_bray.csv")]
        self.is_3d = False

        super().__init__(*args, **kwargs)
