from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


class BBBC050(BaseBBBCDataset):
    """
    BBBC050 Dataset: Nuclei of Mouse Embryonic Cells.

    - **Biological Application:**
      This dataset contains time-series 3D fluorescence images of early mouse embryogenesis, capturing
      the spatial and temporal dynamics of cell nuclei. It is used for nuclei segmentation using deep
      learning techniques.

    - **Images:**
      - **Train Set:**
        - Early mouse embryo nuclei labeled with mRFP1 fused to chromatin marker histone H2B.
        - Acquired using an IX71 microscope with a 20x oil lens.
        - **Spatial Resolution:** (x, y, z) = (0.8, 0.8, 1.75) µm/pixel.
        - **Temporal Resolution:** 10 min.
        - **Embryos:** 11.
      - **Test Set:**
        - Early mouse embryo nuclei labeled with mCherry fused to chromatin marker histone H2B.
        - Acquired using a CV1000 microscope with a 20x oil lens.
        - **Spatial Resolution:** (x, y, z) = (0.8, 0.8, 2.0) µm/pixel.
        - **Temporal Resolution:** 10 min.
        - **Embryos:** 4.

    - **Segmentations:**
      - Manually annotated ground truth segmentations available in three versions:
        - **GroundTruth_NSN:** All nuclei regions labeled with the same label.
        - **GroundTruth_NDN:** All central regions labeled with the same label.
        - **GroundTruth_QCANet:** All nuclei regions labeled with distinct labels.

    - **Source:** https://bbbc.broadinstitute.org/BBBC050
    """

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC050"

    def __init__(self):
        dataset_info = {
            "image_paths": [f"{self.BASE_URL}/Images.zip"],
            "segmentation_path": f"{self.BASE_URL}/GroundTruth.zip",
            "metadata_paths": [],
            "local_path": "data/BBBC050",
        }

        super().__init__("BBBC050", dataset_info)
