import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


class BBBC035(BaseBBBCDataset):
    """
    BBBC035 Dataset: Simulated HL60 Cells from the Cell Tracking Challenge.

    - **Biological Application:**
      This dataset consists of synthetic time-lapse images depicting HL60 cell nuclei stained with Hoechst.
      The images provide an opportunity to test image analysis software by comparing segmentation results
      to the available ground truth for each time point. As time progresses, the number of clustered nuclei
      increases, making segmentation and tracking more complex.

    - **Images:**
      - Images were synthetically produced by MitoGen (CytoPacq).
      - Simulated using Zeiss Axiovert 100S with a Micromax 1300-YHS camera and Plan-Apochromat 40X/1.3 (oil) objective.
      - Time-lapse data with a time step of 29 minutes.
      - Dimensions:
        - Width: 79.1101 - 80.7196 µm (639-652 pixels).
        - Height: 43.2073 - 79.4816 µm (349-642 pixels).
        - Depth: 59 µm (59 slices).

    - **Segmentations:**
      - Ground truth available for foreground/background segmentation at each time point.

    - **Source:** https://bbbc.broadinstitute.org/BBBC035
    """

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC035"

    def __init__(self, *args, **kwargs):
        self.KEY = "BBBC035"
        self.image_paths = [os.path.join(self.BASE_URL, "BBBC035_v1_dataset.zip")]
        self.label_path = os.path.join(
            self.BASE_URL, "BBBC035_v1_DatasetGroundTruth.zip"
        )
        self.metadata_paths = None
        self.is_3d = False

        super().__init__(*args, **kwargs)
