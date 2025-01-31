import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


class BBBC032(BaseBBBCDataset):
    """
    BBBC032 Dataset: 3D Mouse Embryo Blastocyst Cells.

    - **Biological Application:**
      This dataset is used for testing segmentation algorithms in 3D images, where nuclei clustering
      occurs in XY, XZ, and YZ planes. The dataset also contains GAPDH transcripts for quantification.

    - **Images:**
      - Acquired using PerkinElmer Ultraview VoX spinning disk microscope and Leica SP8.
      - Distance between Z-slices: 0.5 µm.
      - Multi-channel imaging with different markers:
        - 647 channel: BMP4 transcripts.
        - 568 channel: GAPDH transcripts.
        - 488 channel: WGA.
        - 405 channel: Hoechst (Nuclear stain).
      - Image dimensions:
        - Width: 103.424 µm (1024 pixels).
        - Height: 135.744 µm (1344 pixels).
        - Depth: 86 µm (172 slices).

    - **Segmentations:**
      - Ground truth 3D images contain manually annotated and segmented nuclei.

    - **Source:** https://bbbc.broadinstitute.org/BBBC032
    """

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC032"

    def __init__(self):
        self.local_path = os.path.join(self.GLOBAL_STORAGE_PATH, "BBBC032")
        self.image_paths = [os.path.join(self.BASE_URL, "BBBC032_v1_dataset.zip")]
        self.label_path = os.path.join(
            self.BASE_URL, "BBBC032_v1_DatasetGroundTruth.tif"
        )
        self.metadata_paths = None

        super().__init__("BBBC032")
