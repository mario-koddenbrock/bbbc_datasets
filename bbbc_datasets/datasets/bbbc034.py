from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


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

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC034"

    def __init__(self):
        dataset_info = {
            "image_paths": [f"{self.BASE_URL}/BBBC034_v1_dataset.zip"],
            "label_path": None,  # No direct segmentation images, only CSV metadata.
            "metadata_paths": [f"{self.BASE_URL}/BBBC034DatasetGroundTruth.csv"],
            "local_path": "data/BBBC034",
        }

        super().__init__("BBBC034", dataset_info)
