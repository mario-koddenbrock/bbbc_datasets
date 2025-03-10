import os

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

    def __init__(self, snr="high", *args, **kwargs):
        """
        Initialize the dataset for a specific SNR level.

        :param snr: Signal-to-noise ratio level ("low" or "high").
        """
        if snr not in self.SNR_LEVELS:
            raise ValueError(
                f"Invalid SNR level: {snr}. Choose from {list(self.SNR_LEVELS.keys())}"
            )

        snr_str = self.SNR_LEVELS[snr]
        self.KEY = f"BBBC027_{snr_str}"

        self.image_paths = [
            os.path.join(self.BASE_URL, f"BBBC027_{snr_str}_images_part1.zip"),
            os.path.join(self.BASE_URL, f"BBBC027_{snr_str}_images_part2.zip"),
            os.path.join(self.BASE_URL, f"BBBC027_{snr_str}_images_part3.zip"),
        ]
        self.label_path = [
            os.path.join(self.BASE_URL, f"BBBC027_{snr_str}_foreground_part1.zip"),
            os.path.join(self.BASE_URL, f"BBBC027_{snr_str}_foreground_part2.zip"),
            os.path.join(self.BASE_URL, f"BBBC027_{snr_str}_foreground_part3.zip"),
        ]
        self.metadata_paths = None
        self.is_3d = True

        super().__init__(*args, **kwargs)

        #
        # self.IMAGE_SUBDIR = []
        # self.SEGMENTATION_SUBDIR = []
        #
        # for k in range(1, 4):
        #     self.IMAGE_SUBDIR.append(f"BBBC027_{snr_str}_images_part{k}")
        #     self.SEGMENTATION_SUBDIR.append(f"BBBC027_{snr_str}_foreground_part{k}")
