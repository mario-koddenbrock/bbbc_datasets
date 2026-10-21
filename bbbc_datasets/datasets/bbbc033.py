import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset
from bbbc_datasets.metadata import DatasetMetadata


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

    METADATA = DatasetMetadata(
        name="BBBC033",
        title="BBBC033 Dataset: 3D Mouse Trophoblast Stem Cells.",
        source="https://bbbc.broadinstitute.org/BBBC033",
        dim="2D",
        imaging_mode="fluorescence",
        modality="grayscale",
        resolution_um=None,
        image_size=None,
        data_type="real",
        instrument=None,
        n_images=2,
        task="segmentation",
        label_type="foreground",
        doi=None,
        license=None,
    )

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC033"

    def __init__(self, *args, **kwargs):
        self.KEY = "BBBC033"
        self.image_paths = [os.path.join(self.BASE_URL, "BBBC033_v1_dataset.zip")]
        self.label_path = os.path.join(
            self.BASE_URL, "BBBC033_v1_DatasetGroundTruth.tif"
        )
        self.metadata_paths = None
        self.is_3d = False

        super().__init__(*args, **kwargs)
