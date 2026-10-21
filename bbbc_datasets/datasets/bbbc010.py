import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset
from bbbc_datasets.metadata import DatasetMetadata


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

    METADATA = DatasetMetadata(
        name="BBBC010",
        title="BBBC010 Dataset: Live/dead assay of C. elegans exposed to pathogens.",
        source="https://bbbc.broadinstitute.org/BBBC010",
        dim="2D",
        imaging_mode="brightfield_fluorescence",
        modality="grayscale",
        resolution_um=None,
        image_size=None,
        data_type="real",
        instrument=None,
        n_images=200,
        task="segmentation",
        label_type="foreground",
        doi=None,
        license=None,
    )

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC010"

    def __init__(self, *args, **kwargs):
        self.KEY = "BBBC010"
        self.image_paths = [os.path.join(self.BASE_URL, "BBBC010_v2_images.zip")]
        self.label_path = os.path.join(self.BASE_URL, "BBBC010_v1_foreground.zip")
        self.additional_label_paths = [
            os.path.join(self.BASE_URL, "BBBC010_v1_foreground_eachworm.zip")
        ]
        self.metadata_paths = None
        self.is_3d = False

        super().__init__(*args, **kwargs)
