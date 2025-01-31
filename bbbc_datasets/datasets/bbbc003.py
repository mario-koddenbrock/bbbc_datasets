import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


class BBBC003(BaseBBBCDataset):
    """
    BBBC003 Dataset: DIC microscopy images of mouse embryos for segmentation analysis.

    - **Biological Application:**
      Fluorescence microscopy cannot be used for embryo viability assessment in in vitro fertilization.
      Instead, DIC imaging is used, though automatic segmentation remains a challenge due to shading effects.

    - **Images:**
      15 images of size 640x480 pixels, acquired using a Nikon Eclipse TE200 microscope
      with a 20x, 0.45 NA objective lens.

    - **Segmentations:**
      Ground truth masks available for foreground segmentation.

    - **Additional Data:**
      Cell count data for each image is provided.

    - **Source:** https://bbbc.broadinstitute.org/BBBC003
    """

    def __init__(self):
        self.local_path = os.path.join(self.GLOBAL_STORAGE_PATH, "BBBC003")
        self.image_paths = [
            "https://data.broadinstitute.org/bbbc/BBBC003/BBBC003_v1_images.zip"
        ]
        self.label_path = (
            "https://data.broadinstitute.org/bbbc/BBBC003/BBBC003_v1_foreground.zip"
        )
        self.metadata_paths = [
            "https://data.broadinstitute.org/bbbc/BBBC003/BBBC003_v1_counts.txt"
        ]

        super().__init__("BBBC003")
