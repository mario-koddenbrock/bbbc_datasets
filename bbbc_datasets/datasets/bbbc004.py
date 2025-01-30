from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


class BBBC004(BaseBBBCDataset):
    """
    BBBC004 Dataset: Synthetic fluorescence microscopy images of nuclei with varying clustering probabilities.

    - **Biological Application:**
      This dataset is used to evaluate the performance of nuclei segmentation and counting algorithms
      under different levels of nuclear clustering.

    - **Images:**
      Five subsets of 20 images each, with overlap probabilities: [0, 0.15, 0.3, 0.45, 0.6].

    - **Segmentations:**
      Ground truth binary segmentation masks for foreground detection.

    - **Ground Truth:**
      Each image contains exactly 300 objects.

    - **Source:** https://bbbc.broadinstitute.org/BBBC004
    """

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC004"

    OVERLAP_PROBABILITIES = {
        0.00: "000",
        0.15: "015",
        0.30: "030",
        0.45: "045",
        0.60: "060",
    }

    def __init__(self, overlap_probability=0.00):
        """
        Initialize the dataset with a specific overlap probability.

        :param overlap_probability: The clustering probability of nuclei (0, 0.15, 0.3, 0.45, 0.6)
        """
        if overlap_probability not in self.OVERLAP_PROBABILITIES:
            raise ValueError(
                f"Invalid overlap probability: {overlap_probability}. Choose from {list(self.OVERLAP_PROBABILITIES.keys())}"
            )

        prob_str = self.OVERLAP_PROBABILITIES[overlap_probability]

        dataset_info = {
            "image_paths": [f"{self.BASE_URL}/BBBC004_v1_{prob_str}_images.zip"],
            "segmentation_path": f"{self.BASE_URL}/BBBC004_v1_{prob_str}_foreground.zip",
            "metadata_paths": [],
            "local_path": f"data/BBBC004/{prob_str}",
        }

        super().__init__(f"BBBC004_{prob_str}", dataset_info)
