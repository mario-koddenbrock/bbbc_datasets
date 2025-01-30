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

    DATASETS = {
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

    def __init__(self, dataset_name="WT-ID550"):
        """
        Initialize the dataset for a specific phenotype and sequence ID.

        :param dataset_name: The dataset variation to download (WT-ID550, OE-ID350, PD-ID450, etc.).
        """
        if dataset_name not in self.DATASETS:
            raise ValueError(
                f"Invalid dataset name: {dataset_name}. Choose from {list(self.DATASETS.keys())}"
            )

        dataset_info = {
            "image_paths": [f"{self.BASE_URL}/{self.DATASETS[dataset_name]}"],
            "segmentation_path": None,  # Ground truth masks & metadata are inherently generated.
            "metadata_paths": [],
            "local_path": f"data/BBBC046/{dataset_name}",
        }

        super().__init__(f"BBBC046_{dataset_name}", dataset_info)
