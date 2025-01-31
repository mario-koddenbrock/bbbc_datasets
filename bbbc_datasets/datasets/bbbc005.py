from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


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

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC005"

    def __init__(self):
        dataset_info = {
            "image_paths": [f"{self.BASE_URL}/BBBC005_v1_images.zip"],
            "label_path": f"{self.BASE_URL}/BBBC005_v1_ground_truth.zip",
            "metadata_paths": [f"{self.BASE_URL}/BBBC005_results_bray.csv"],
            "local_path": "data/BBBC005",
        }

        super().__init__("BBBC005", dataset_info)
