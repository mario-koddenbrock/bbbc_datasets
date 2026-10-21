import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset
from bbbc_datasets.metadata import DatasetMetadata


class BBBC034(BaseBBBCDataset):
    """
    BBBC034 Dataset: 3D Induced Pluripotent Human Stem Cells (hiPSC).

    - **Biological Application:**
      This dataset is used for testing segmentation algorithms in 3D images of human induced pluripotent stem cells.
      Clustering and intensity variations in nuclei pose challenges for segmentation.
      Edge and center regions of colonies exhibit different morphology and intensity.

    - **Images:**
      - Acquired using Zeiss AxioObserver microscope with C-Apochromat 100x/1.25 water immersion objective.
      - Hamamatsu ORCA-Flash 4.0 camera used for imaging.
      - Channels:
        - **Channel 1 (C=0):** CellMask Deep Red plasma membrane.
        - **Channel 2 (C=1):** GFP edited channel.
        - **Channel 3 (C=2):** DNA channel.
        - **Channel 4 (C=3):** Brightfield.
      - Dimensions:
        - Width: 66.56 µm (1024 pixels).
        - Height: 66.56 µm (1024 pixels).
        - Depth: 15.08 µm (52 slices).
      - Additional **center and edge colony images**:
        - **Channel 1 (C=1):** CellMask Deep Red plasma membrane.
        - **Channel 3 (C=3):** EGFP beta-actin.
        - **Channel 5 (C=5):** Hoechst DNA.

    - **Segmentations:**
      - Ground truth available for 3D image set, provided as a **CSV file**.
      - No ground truth is available for center/edge colony images.

    - **Source:** https://bbbc.broadinstitute.org/BBBC034
    """

    METADATA = DatasetMetadata(
        name="BBBC034",
        title="BBBC034 Dataset: 3D Induced Pluripotent Human Stem Cells (hiPSC).",
        source="https://bbbc.broadinstitute.org/BBBC034",
        dim="2D",
        imaging_mode="brightfield_fluorescence",
        modality="grayscale",
        resolution_um=None,
        image_size=None,
        data_type="real",
        instrument=None,
        n_images=10,  # verified count; the catalog lists 9
        task="segmentation",
        label_type="foreground",
        doi=None,
        license=None,
    )

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC034"

    def __init__(self, *args, **kwargs):
        self.KEY = "BBBC034"
        self.image_paths = [os.path.join(self.BASE_URL, "BBBC034_v1_dataset.zip")]
        self.label_path = [
            os.path.join(self.BASE_URL, "BBBC034_v1_DatasetGroundTruth.zip")
        ]
        self.metadata_paths = None

        self.is_3d = False

        super().__init__(*args, **kwargs)
