import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset
from bbbc_datasets.utils.file_io import load_image


class BBBC044(BaseBBBCDataset):
    """
    BBBC044 Dataset: Mouse hippocampal presynaptic terminals (vGlut-1 and vGat).

    - **Biological Application:**
      Confocal stacks of mouse hippocampal presynaptic terminals, used to validate
      automatic detection and counting of puncta (presynaptic terminals) labeled with
      vGlut-1 EGFP and vGat.

    - **Images:**
      12 confocal stacks of 1024x1024x15 (0.14 um z-step), 8-bit TIFF:
      6 vGlut-1 and 6 vGat, acquired on a Zeiss LSM 710 at 63x magnification.

    - **Ground Truth:**
      Two experts marked the puncta centroids inside a bounded validation region of
      each stack. The ground truth is provided as RGB overlay images
      (R = original, G = expert's centroids, B = validation region), named
      "<image_stem>_expert1.tif" / "<image_stem>_expert2.tif", plus a CSV with the
      centroid coordinates and expert counts. get_label returns the expert1 overlay.

    - **Source:** https://bbbc.broadinstitute.org/BBBC044
    """

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC044"

    MARKERS = ("vglut1", "vgat")

    def __init__(self, marker=None, *args, **kwargs):
        """
        Initialize the dataset, optionally restricted to a marker.

        :param marker: One of "vglut1" or "vgat". If None, both markers are available.
        """
        if marker is not None and marker.lower() not in self.MARKERS:
            raise ValueError(
                f"Invalid marker: {marker}. Choose from {list(self.MARKERS)}"
            )

        self.marker = marker
        self.KEY = f"BBBC044_{marker}" if marker else "BBBC044"
        self.image_paths = [
            os.path.join(self.BASE_URL, "BBBC044_v1_original_images.zip")
        ]
        self.label_path = os.path.join(self.BASE_URL, "BBBC044_v1_validation.zip")
        self.metadata_paths = None
        self.is_3d = True

        super().__init__(*args, **kwargs)

    def get_image_paths(self):
        """
        Returns the list of image paths, optionally filtered by marker.
        """
        images = super().get_image_paths()
        if self.marker is None:
            return images
        return [p for p in images if self.marker.lower() in p]

    def get_label(self, image_path, expert=1):
        """
        Returns the RGB ground-truth overlay ("<stem>_expert<expert>.tif")
        for a given image path.
        """
        stem = os.path.splitext(os.path.basename(image_path))[0]
        target_name = f"{stem}_expert{expert}.tif"

        label_paths = self.get_label_paths()
        matches = [p for p in label_paths if os.path.basename(p) == target_name]

        if matches:
            return load_image(matches[0])
        raise FileNotFoundError(f"Validation overlay not found for {image_path}")
