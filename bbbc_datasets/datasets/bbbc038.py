from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


class BBBC038(BaseBBBCDataset):
    """
    BBBC038 Dataset: Kaggle 2018 Data Science Bowl - Nuclei Segmentation.

    - **Biological Application:**
      This dataset was created for the Kaggle 2018 Data Science Bowl to challenge segmentation algorithms
      in detecting and segmenting nuclei across a diverse range of biological contexts.
      The dataset includes thousands of images containing nuclei from various organisms, imaging techniques,
      and experimental conditions.

    - **Images:**
      - The dataset includes images from multiple sources, including human, mouse, and fly samples.
      - Nuclei appear in different contexts such as cultured monolayers, tissues, and embryos.
      - Imaging techniques include fluorescent and histology stains.
      - The dataset is divided into:
        - **Stage 1 Training Set:** Includes images and corresponding segmentation masks.
        - **Stage 1 Test Set:** Unlabeled images for testing.
        - **Stage 2 Test Set:** Additional test images, including conditions not present in Stage 1.

    - **Segmentations:**
      - Ground truth segmentation masks are provided for each nucleus separately.
      - Masks do not overlap (each pixel belongs to only one mask).
      - Labels and annotations available as CSV files.

    - **Metadata:**
      - Includes additional annotations and ground truth solutions for test sets.

    - **Source:** https://bbbc.broadinstitute.org/BBBC038
    """

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC038"

    def __init__(self, dataset_version="stage1_train"):
        """
        Initialize the dataset for a specific dataset version.

        :param dataset_version: One of ("stage1_train", "stage1_test", "stage2_test_final").
        """
        allowed_versions = ["stage1_train", "stage1_test", "stage2_test_final"]
        if dataset_version not in allowed_versions:
            raise ValueError(
                f"Invalid dataset version: {dataset_version}. Choose from {allowed_versions}"
            )

        dataset_info = {
            "image_paths": [f"{self.BASE_URL}/{dataset_version}.zip"],
            "label_path": (
                f"{self.BASE_URL}/stage1_train_labels.csv"
                if dataset_version == "stage1_train"
                else None
            ),
            "metadata_paths": [
                f"{self.BASE_URL}/metadata.xlsx",
                (
                    f"{self.BASE_URL}/stage1_solution.csv"
                    if dataset_version == "stage1_train"
                    else None
                ),
                (
                    f"{self.BASE_URL}/stage2_solution_final.csv"
                    if dataset_version == "stage2_test_final"
                    else None
                ),
            ],
            "local_path": f"data/BBBC038/{dataset_version}",
        }

        super().__init__(f"BBBC038_{dataset_version}", dataset_info)
