import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


class BBBC002(BaseBBBCDataset):
    """
    BBBC002 Dataset: Drosophila Kc167 cells for counting.

    - **Biological Application:**
      Five samples of Drosophila melanogaster Kc167 cells stained with the DNA stain
      Hoechst 33342. One sample (nodsRNA) is wild type, the other four (48, 340, Anillin,
      mad2) have different gene knockdowns via RNAi.

    - **Images:**
      10 fields of view per sample (50 total), single DNA channel, 512x512 pixels,
      8-bit TIFF. Acquired on a Zeiss Axiovert 200M microscope.

    - **Ground Truth:**
      Tab-delimited text file with the cell counts per image from two human counters.

    - **Source:** https://bbbc.broadinstitute.org/BBBC002
    """

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC002"

    def __init__(self, *args, **kwargs):
        self.KEY = "BBBC002"
        self.image_paths = [
            os.path.join(self.BASE_URL, "BBBC002_v1_images.zip")
        ]
        self.label_path = None
        self.metadata_paths = [
            os.path.join(self.BASE_URL, "BBBC002_v1_counts.txt")
        ]
        self.is_3d = False

        super().__init__(*args, **kwargs)
