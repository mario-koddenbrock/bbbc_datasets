import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset
from bbbc_datasets.metadata import DatasetMetadata


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

    METADATA = DatasetMetadata(
        name="BBBC009",
        title="BBBC009 Dataset: Human red blood cells (DIC images).",
        source="https://bbbc.broadinstitute.org/BBBC009",
        dim="2D",
        imaging_mode="dic",
        modality="grayscale",
        resolution_um=None,
        image_size=(600, 800),
        data_type="real",
        instrument=None,
        n_images=5,
        task="segmentation",
        label_type="outlines",
        doi="10.1038/nmeth.2083",
        license="CC0-1.0",
    )

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
