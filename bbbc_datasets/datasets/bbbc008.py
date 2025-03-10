import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


class BBBC008(BaseBBBCDataset):
    """
    BBBC008 Dataset: Fluorescence microscopy images of human HT29 colon cancer cells.

    - **Biological Application:**
      This dataset is used for segmentation and cell counting of HT29 colon cancer cells.

    - **Images:**
      - 12 images, each containing three fluorescence channels:
        - Hoechst (DNA, Channel 1).
        - Phalloidin (Actin, Channel 3).
        - pH3 (Mitotic cells, Channel 2 - Not used for segmentation).

    - **Segmentations:**
      - Foreground-background segmentation masks available.
      - Manually refined after initial thresholding.

    - **Source:** https://bbbc.broadinstitute.org/BBBC008
    """

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC008"


def __init__(self, *args, **kwargs):
    self.local_path = os.path.join(self.download_dir, "BBBC008")
    self.image_paths = [os.path.join(self.BASE_URL, "BBBC008_v1_images.zip")]
    self.label_path = os.path.join(self.BASE_URL, "BBBC008_v1_foreground.zip")
    self.metadata_paths = None
    self.is_3d = False

    super().__init__("BBBC008", *args, **kwargs)
