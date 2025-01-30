from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


class BBBC027(BaseBBBCDataset):
    """
    BBBC027 Dataset: 3D Synthetic Colon Tissue Images with Varying SNR.

    - **Biological Application:**
      Evaluates the performance of segmentation algorithms in handling clustered nuclei in 3D colon tissue images.
      The dataset is provided in two different signal-to-noise ratio (SNR) levels: high and low.

    - **Images:**
      - 30 images available in both high SNR and low SNR variants.
      - Images are divided into three parts for each SNR level.

    - **Segmentations:**
      - Ground truth segmentation masks available for foreground/background separation.
      - Binary masks are provided.

    - **Source:** https://bbbc.broadinstitute.org/BBBC027
    """

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC027"

    SNR_LEVELS = {"low": "lowSNR", "high": "highSNR"}

    def __init__(self, snr="high"):
        """
        Initialize the dataset for a specific SNR level.

        :param snr: Signal-to-noise ratio level ("low" or "high").
        """
        if snr not in self.SNR_LEVELS:
            raise ValueError(
                f"Invalid SNR level: {snr}. Choose from {list(self.SNR_LEVELS.keys())}"
            )

        snr_str = self.SNR_LEVELS[snr]

        dataset_info = {
            "image_paths": [
                f"{self.BASE_URL}/BBBC027_{snr_str}_images_part1.zip",
                f"{self.BASE_URL}/BBBC027_{snr_str}_images_part2.zip",
                f"{self.BASE_URL}/BBBC027_{snr_str}_images_part3.zip",
            ],
            "segmentation_path": [
                f"{self.BASE_URL}/BBBC027_{snr_str}_foreground_part1.zip",
                f"{self.BASE_URL}/BBBC027_{snr_str}_foreground_part2.zip",
                f"{self.BASE_URL}/BBBC027_{snr_str}_foreground_part3.zip",
            ],
            "metadata_paths": [],
            "local_path": f"data/BBBC027/{snr_str}",
        }

        super().__init__(f"BBBC027_{snr_str}", dataset_info)
