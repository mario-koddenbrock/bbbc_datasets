import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


class BBBC001(BaseBBBCDataset):
    """
    BBBC001 Dataset: Human HT29 colon-cancer cells for counting.

    - **Biological Application:**
      These images are of human HT29 colon cancer cells, a cell line widely used to study
      normal and neoplastic processes. The images come from Moffat et al.'s RNAi screen,
      where cells treated with a mitotic regulator (Rock1_1885_k27) were screened for
      mitotic regulators by identifying and counting cells.

    - **Images:**
      Six fields of view of 512x512 pixels (Hoechst 33342 DNA channel, 8-bit TIFF).
      Acquired on a Cellomics ArrayScan at the Whitehead-MIT Bioimaging Center.

    - **Ground Truth:**
      Tab-delimited text file with the cell counts per image from two human counters.

    - **Source:** https://bbbc.broadinstitute.org/BBBC001
    """

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC001"

    def __init__(self, *args, **kwargs):
        self.KEY = "BBBC001"
        self.image_paths = [
            os.path.join(self.BASE_URL, "BBBC001_v1_images_tif.zip")
        ]
        self.label_path = None
        self.metadata_paths = [
            os.path.join(self.BASE_URL, "BBBC001_v1_counts.txt")
        ]
        self.is_3d = False

        super().__init__(*args, **kwargs)
