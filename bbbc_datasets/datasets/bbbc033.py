from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


class BBBC033(BaseBBBCDataset):
    """
    BBBC033 Dataset: 3D Mouse Trophoblast Stem Cells.

    - **Biological Application:**
      This dataset is used for testing segmentation algorithms in 3D images, where nuclei clustering
      forms a monolayer that is difficult to segment. The dataset includes manually annotated ground truth.

    - **Images:**
      - Acquired using PerkinElmer Ultraview VoX spinning disk microscope and Leica SP8.
      - Distance between Z-slices: 0.5 µm.
      - 3D imaging of clustered monolayers of mouse trophoblast stem cells.

    - **Segmentations:**
      - Ground truth 3D images contain manually annotated and segmented nuclei.

    - **Source:** https://bbbc.broadinstitute.org/BBBC033
    """

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC033"

    def __init__(self):
        dataset_info = {
            "image_paths": [f"{self.BASE_URL}/BBBC033_v1_dataset.zip"],
            "label_path": f"{self.BASE_URL}/BBBC033DatasetGroundTruth.tif",
            "metadata_paths": [],
            "local_path": "data/BBBC033",
        }

        super().__init__("BBBC033", dataset_info)
