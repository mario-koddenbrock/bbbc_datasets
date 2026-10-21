import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


class BBBC009(BaseBBBCDataset):
    """
    BBBC009 Dataset: Human red blood cells (DIC images).

    - **Biological Application:**
      Differential interference contrast (DIC) images of human red blood cells, used to
      evaluate the accuracy of DIC image transformation/segmentation algorithms.

    - **Images:**
      Five DIC images of red blood cells, 8-bit TIFF.

    - **Segmentations:**
      Hand-drawn cell outlines, stored as 8-bit TIFF files with the same names as the
      images. White denotes the foreground (cell) region.

    - **Source:** https://bbbc.broadinstitute.org/BBBC009
    """

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC009"

    def __init__(self, *args, **kwargs):
        self.KEY = "BBBC009"
        self.image_paths = [
            os.path.join(self.BASE_URL, "BBBC009_v1_images.zip")
        ]
        self.label_path = os.path.join(self.BASE_URL, "BBBC009_v1_outlines.zip")
        self.metadata_paths = None
        self.is_3d = False

        super().__init__(*args, **kwargs)
