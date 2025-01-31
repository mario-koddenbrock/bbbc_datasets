import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


class BBBC024(BaseBBBCDataset):
    """
    BBBC024 Dataset: 3D Synthetic HL60 Cell Line Images with Varying Clustering Probability and SNR.

    - **Biological Application:**
      Evaluates the performance of segmentation algorithms in handling clustered nuclei in 3D images.
      The dataset consists of synthetic images with different clustering probabilities and signal-to-noise ratios (SNR).

    - **Images:**
      - Four subsets based on clustering probability (0%, 25%, 50%, 75%).
      - Each subset has two variants: High SNR and Low SNR.
      - Each subset contains 30 images.

    - **Segmentations:**
      - Ground truth segmentation masks available for foreground/background separation.
      - Masks are stored as labeled 16-bit grayscale images.

    - **Source:** https://bbbc.broadinstitute.org/BBBC024
    """

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC024"

    CLUSTERING_PROBABILITIES = {0: "c00", 25: "c25", 50: "c50", 75: "c75"}

    SNR_LEVELS = {"low": "lowSNR", "high": "highSNR"}

    def __init__(self, clustering_probability=0, snr="high"):
        """
        Initialize the dataset for a specific clustering probability and SNR level.

        :param clustering_probability: Clustering probability (0, 25, 50, 75).
        :param snr: Signal-to-noise ratio level ("low" or "high").
        """
        if clustering_probability not in self.CLUSTERING_PROBABILITIES:
            raise ValueError(
                f"Invalid clustering probability: {clustering_probability}. Choose from {list(self.CLUSTERING_PROBABILITIES.keys())}"
            )

        if snr not in self.SNR_LEVELS:
            raise ValueError(
                f"Invalid SNR level: {snr}. Choose from {list(self.SNR_LEVELS.keys())}"
            )

        self.prob_str = self.CLUSTERING_PROBABILITIES[clustering_probability]
        self.snr_str = self.SNR_LEVELS[snr]
        self.local_path = os.path.join(
            self.GLOBAL_STORAGE_PATH, "BBBC024", f"{self.prob_str}_{self.snr_str}"
        )

        self.image_paths = [
            os.path.join(
                self.BASE_URL, f"BBBC024_v1_{self.prob_str}_{self.snr_str}_images.zip"
            ),
            os.path.join(
                self.BASE_URL,
                f"BBBC024_v1_{self.prob_str}_{self.snr_str}_images_TIFF.zip",
            ),
        ]
        self.label_path = os.path.join(
            self.BASE_URL, f"BBBC024_v1_{self.prob_str}_{self.snr_str}_foreground.zip"
        )
        self.metadata_paths = None

        super().__init__(f"BBBC024_{self.prob_str}_{self.snr_str}")
