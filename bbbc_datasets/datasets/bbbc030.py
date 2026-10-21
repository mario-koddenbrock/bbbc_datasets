import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset
from bbbc_datasets.metadata import DatasetMetadata


class BBBC030(BaseBBBCDataset):
    """
    BBBC030 Dataset: Chinese Hamster Ovary (CHO) cells (DIC images).

    - **Biological Application:**
      DIC images of Chinese Hamster Ovary cells taken on an Olympus Cell-R microscope
      with a 20x lens at the time the cells initiated attachment to the bottom of the
      dish. Used for DIC reconstruction algorithm ranking via ROC/AUC comparison.

    - **Images:**
      60 DIC images of CHO cells, PNG format.

    - **Segmentations:**
      Hand-segmented cell contours (outlines) stored as PNG files with the same names
      as the images.

    - **Source:** https://bbbc.broadinstitute.org/BBBC030
    """

    METADATA = DatasetMetadata(
        name="BBBC030",
        title="BBBC030 Dataset: Chinese Hamster Ovary (CHO) cells (DIC images).",
        source="https://bbbc.broadinstitute.org/BBBC030",
        dim="2D",
        imaging_mode="dic",
        modality="grayscale",
        resolution_um=None,
        image_size=(1032, 1376),
        data_type="real",
        instrument="Olympus Cell-R (20x)",
        n_images=60,
        task="segmentation",
        label_type="outlines",
        doi=None,
        license="CC-BY-3.0",
    )

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC030"

    def __init__(self, *args, **kwargs):
        self.KEY = "BBBC030"
        self.image_paths = [os.path.join(self.BASE_URL, "images.zip")]
        self.label_path = os.path.join(self.BASE_URL, "ground_truth.zip")
        self.metadata_paths = None
        self.is_3d = False

        super().__init__(*args, **kwargs)
