import os.path

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


class BBBC046(BaseBBBCDataset):
    """
    BBBC046 Dataset: FiloData3D - Synthetic 3D Time-Lapse Imaging of A549 Cells with Filopodia.

    - **Biological Application:**
      This dataset consists of synthetic 3D time-lapse images of A549 lung cancer cells with distinct morphologies:
      - Wild-type (WT): Sporadic filopodia with transient appearance.
      - CRMP-2-overexpressing (OE): Numerous short-lived filopodia.
      - CRMP-2-phospho-defective (PD): Long, branching filopodia with whole-experiment lifetimes.

      The dataset is used to study the segmentation and tracking of 3D filopodia under different signal-to-noise (SNR) and anisotropy ratio (AR) conditions.

    - **Images:**
      - 180 synthetic 3D time-lapse sequences of single A549 cells.
      - 3 sequences for each phenotype (WT, OE, PD).
      - 20 variations per sequence, covering 5 SNR levels and 4 AR conditions.
      - 30 frames per sequence, simulated with FiloGen and confocal microscopy settings.

    - **Segmentations & Metadata:**
      - Labeled image masks of cell bodies and filopodial branches.
      - CSV files describing filopodia tip positions and branch lengths over time.

    - **Source:** https://bbbc.broadinstitute.org/BBBC046
    """

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC046"

    PHENOTYPES = {
        "OE-ID350": "OE-ID350.zip",
        "OE-ID351": "OE-ID351.zip",
        "OE-ID352": "OE-ID352.zip",
        "PD-ID450": "PD-ID450.zip",
        "PD-ID451": "PD-ID451.zip",
        "PD-ID452": "PD-ID452.zip",
        "WT-ID550": "WT-ID550.zip",
        "WT-ID551": "WT-ID551.zip",
        "WT-ID552": "WT-ID552.zip",
    }

    FLOURESCENCE_LEVELS = {
        "0.25": "factor-0.25",
        "0.5": "factor-0.5",
        "1.0": "factor-1.0",
        "2.0": "factor-2.0",
        "4.0": "factor-4.0",
    }

    ANISOTROPY_RATIOS = {
        1: "AR-1",
        2: "AR-2",
        4: "AR-4",
        8: "AR-8",
    }

    def __init__(
        self, phenotype="WT-ID550", fluorescence_level="0.25", anisotropy_ratio=1
    ):
        """
        Initialize the dataset for a specific phenotype and sequence ID.

        :param phenotypes: The dataset variation to download (WT-ID550, OE-ID350, PD-ID450, etc.).
        """
        if phenotype not in self.PHENOTYPES:
            raise ValueError(
                f"Invalid dataset name: {phenotype}. Choose from {list(self.PHENOTYPES.keys())}"
            )

        self.IMAGE_SUBDIR = "all"
        self.local_path = os.path.join(self.GLOBAL_STORAGE_PATH, "BBBC046", phenotype)
        self.is_3d = False
        self.image_paths = [os.path.join(self.BASE_URL, self.PHENOTYPES[phenotype])]
        self.label_path = (
            None  # Ground truth masks & metadata are inherently generated.
        )
        self.metadata_paths = None

        super().__init__(f"BBBC046_{phenotype}")

        self.IMAGE_SUBDIR = os.path.join(
            "all",
            f"{phenotype}-{self.ANISOTROPY_RATIOS[anisotropy_ratio]}",
            self.FLOURESCENCE_LEVELS[fluorescence_level],
        )

        self.LABEL_SUBDIR = os.path.join(
            "all",
            f"{phenotype}-{self.ANISOTROPY_RATIOS[anisotropy_ratio]}",
        )

    def get_label_paths(self):
        """
        Returns the label mask file path (if available).
        """
        images = self._get_paths(self.LABEL_SUBDIR, recursive=False)
        return images
