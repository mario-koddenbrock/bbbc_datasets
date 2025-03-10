import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


class BBBC028(BaseBBBCDataset):
    """
    BBBC028 Dataset: Polymerized Structures in Differential Interference Contrast (DIC) Microscopy.

    - **Biological Application:**
      The dataset includes DIC images of polymerized structures used for evaluating image reconstruction algorithms.
      The fluorescent images serve as ground truth for quality control measurements.

    - **Images:**
      - 60 DIC images of 6 different polymerized shapes (e.g., triangle, circle, multi-height objects).
      - Images were captured using an Olympus Cell-R microscope with a 20x lens.

    - **Segmentations:**
      - Ground truth consists of fluorescent images of the same structures captured under appropriate excitation light.
      - These fluorescent images can be used for evaluating DIC reconstruction using Mean Squared Error (MSE) metrics.

    - **Source:** https://bbbc.broadinstitute.org/BBBC028
    """

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC028"


def __init__(self, *args, **kwargs):
    self.local_path = os.path.join(self.download_dir, "BBBC028")
    self.image_paths = [os.path.join(self.BASE_URL, "images.zip")]
    self.label_path = os.path.join(self.BASE_URL, "ground_truth.zip")
    self.metadata_paths = None
    self.is_3d = False
    # TODO: What is the 3rd dimension of the mask?
    super().__init__("BBBC028", *args, **kwargs)
