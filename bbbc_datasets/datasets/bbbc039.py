from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


class BBBC039(BaseBBBCDataset):
    """
    BBBC039 Dataset: Nuclei of U2OS Cells in a Chemical Screen.

    - **Biological Application:**
      This dataset is part of a high-throughput chemical screen on U2OS cells, featuring 200 bioactive compounds.
      The dataset focuses on segmentation algorithms that can accurately separate individual nuclei regardless of shape and density.
      Around 23,000 single nuclei have been manually annotated to provide ground truth segmentation.

    - **Images:**
      - 200 fluorescence microscopy images from the DNA (Hoechst) channel.
      - Each image corresponds to a single field of view from a high-throughput chemical screen.
      - TIFF format with 520x696 pixels at 16-bit depth.

    - **Segmentations:**
      - Ground truth annotations are provided as PNG masks encoding individual nuclei.
      - Touching nuclei are assigned distinct colors to enable accurate instance segmentation.
      - Masks need to be decoded into labeled matrices for use in segmentation evaluation.

    - **Metadata:**
      - Images are split into training, validation, and test subsets.
      - A metadata package defines the partitions and image details.

    - **Source:** https://bbbc.broadinstitute.org/BBBC039
    """

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC039"

    def __init__(self):
        dataset_info = {
            "image_paths": [f"{self.BASE_URL}/images.zip"],
            "label_path": f"{self.BASE_URL}/masks.zip",
            "metadata_paths": [f"{self.BASE_URL}/metadata.zip"],
            "local_path": "data/BBBC039",
        }

        super().__init__("BBBC039", dataset_info)
