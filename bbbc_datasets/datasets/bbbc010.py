from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


class BBBC010(BaseBBBCDataset):
    """
    BBBC010 Dataset: Live/dead assay of C. elegans exposed to pathogens.

    - **Biological Application:**
      Used for screening novel anti-infectives by distinguishing between live and dead C. elegans worms.
      Positive control (ampicillin-treated worms) appear curved and smooth (alive).
      Negative control (untreated worms) appear rod-like and textured (dead).

    - **Images:**
      - 100 images from a 384-well plate.
      - Brightfield (Channel 1) and GFP (Channel 2).
      - Image size: 696 x 520 pixels, 16-bit TIF format.

    - **Segmentations:**
      - **Foreground/background segmentation:** Human-corrected binary images.
      - **Individual worm outlines:** Binary segmentation images for individual worms.

    - **Source:** https://bbbc.broadinstitute.org/BBBC010
    """

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC010"

    def __init__(self):
        dataset_info = {
            "image_paths": [f"{self.BASE_URL}/BBBC010_v2_images.zip"],
            "segmentation_path": f"{self.BASE_URL}/BBBC010_v1_foreground.zip",
            "additional_segmentation_paths": [
                f"{self.BASE_URL}/BBBC010_v1_foreground_eachworm.zip"
            ],
            "metadata_paths": [],
            "local_path": "data/BBBC010",
        }

        super().__init__("BBBC010", dataset_info)
