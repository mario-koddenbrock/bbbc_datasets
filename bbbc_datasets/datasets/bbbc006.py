import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


class BBBC006(BaseBBBCDataset):
    """
    BBBC006 Dataset: Z-stack fluorescence microscopy images of human U2OS cells.

    - **Biological Application:**
      Evaluates the effect of focus variations on foreground segmentation in high-content screening.

    - **Images:**
      - 32 z-stack focal planes per field of view.
      - Two fluorescence markers:
        - Hoechst (w1): Stains nuclei.
        - Phalloidin (w2): Stains cell bodies.

    - **Segmentations:**
      - Ground truth segmentation available for in-focus images (z = 11 to z = 23).
      - Masks are 8-bit grayscale PNGs (each segmented nucleus has a unique integer label).

    - **Metadata:**
      - Nucleus count data and field of view information.

    - **Source:** https://bbbc.broadinstitute.org/BBBC006
    """

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC006"

    def __init__(self, z_plane=16):
        """
        Initialize the dataset for a specific z-plane.

        :param z_plane: The z-stack focal plane to download (0-32, default = 16 for optimal focus).
        """
        if not (0 <= z_plane <= 32):
            raise ValueError(f"Invalid z-plane: {z_plane}. Choose between 0 and 32.")

        self.z_plane = z_plane
        self.local_path = os.path.join(
            self.GLOBAL_STORAGE_PATH, "BBBC006", f"z_{z_plane:02}"
        )
        self.image_paths = [
            os.path.join(self.BASE_URL, f"BBBC006_v1_images_z_{z_plane:02}.zip")
        ]
        self.label_path = os.path.join(self.BASE_URL, "BBBC006_v1_labels.zip")
        self.metadata_paths = [
            os.path.join(self.BASE_URL, "BBBC006_v1_counts.csv"),
            os.path.join(self.BASE_URL, "BBBC006_results_bray.csv"),
        ]

        super().__init__(f"BBBC006_z_{z_plane:02}")
