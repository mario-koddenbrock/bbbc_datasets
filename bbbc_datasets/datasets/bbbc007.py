import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


class BBBC007(BaseBBBCDataset):
    """
    BBBC007 Dataset: Drosophila Kc167 cells for cell boundary segmentation.

    - **Biological Application:**
      Drosophila melanogaster Kc167 cells stained for DNA (nuclei) and actin (cell body).
      Segmenting nuclei and foreground is comparatively easy for these images, so the
      focus is on finding the boundaries between adjacent cells.

    - **Images:**
      16 images of roughly 512x512 pixels with ~80 cells per image, each stored as two
      grayscale 8-bit TIFF channels: DNA ("..._D_...") and actin ("..._F_...").
      Acquired on a motorized Zeiss Axioplan 2.

    - **Segmentations:**
      Hand-outlined nuclei and cells, stored as monochrome 8-bit TIFF files with the
      same names as the images.

    - **Source:** https://bbbc.broadinstitute.org/BBBC007
    """

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC007"

    def __init__(self, *args, **kwargs):
        self.KEY = "BBBC007"
        self.image_paths = [
            os.path.join(self.BASE_URL, "BBBC007_v1_images.zip")
        ]
        self.label_path = os.path.join(self.BASE_URL, "BBBC007_v1_outlines.zip")
        self.metadata_paths = None
        self.is_3d = False

        super().__init__(*args, **kwargs)
