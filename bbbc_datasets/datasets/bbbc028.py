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

    def __init__(self):
        dataset_info = {
            "image_paths": [f"{self.BASE_URL}/images.zip"],
            "segmentation_path": f"{self.BASE_URL}/ground_truth.zip",
            "metadata_paths": [],
            "local_path": "data/BBBC028",
        }

        super().__init__("BBBC028", dataset_info)
