import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset
from bbbc_datasets.utils.file_io import load_image


class BBBC018(BaseBBBCDataset):
    """
    BBBC018 Dataset: Human HT29 colon-cancer cells (diverse phenotypes).

    - **Biological Application:**
      HT29 images enriched for each of 14 diverse morphologies (actin blebs, actin dots,
      anaphase/telephase, motile, etc.), drawn from the top-scoring sample of each
      classifier of Jones et al. (PNAS 2009). Used to measure segmentation robustness
      to morphological variation.

    - **Images:**
      56 fields of view (4 per morphology), each with three 512x512 channels
      (Hoechst DNA, pH3, phalloidin-actin) stored as ArrayScan DIB files
      ("<wellidx>-DNA.DIB", "<wellidx>-pH3.DIB", "<wellidx>-actin.DIB"),
      i.e. 168 image files.

    - **Segmentations:**
      Hand-drawn outlines as PNG files: "<wellidx>-nuclei.png" (nuclei outlines,
      matching the DNA and pH3 channels) and "<wellidx>-cells.png" (cell body
      outlines, matching the actin channel). Well 10779 has no outlines (the images
      were too blurred to segment with confidence), so get_label raises
      FileNotFoundError for that well's three images.

    - **Source:** https://bbbc.broadinstitute.org/BBBC018
    """

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC018"

    # Map each image channel to the outline kind that belongs to it.
    CHANNEL_TO_OUTLINE = {"DNA": "nuclei", "pH3": "nuclei", "actin": "cells"}

    def __init__(self, *args, **kwargs):
        self.KEY = "BBBC018"
        self.image_paths = [
            os.path.join(self.BASE_URL, "BBBC018_v1_images.zip")
        ]
        self.label_path = os.path.join(self.BASE_URL, "BBBC018_v1_outlines.zip")
        self.metadata_paths = None
        self.is_3d = False

        super().__init__(*args, **kwargs)

    def get_label(self, image_path):
        """
        Returns the outline mask for a given image path.

        The DIB channel of the image decides which outline kind is returned:
        DNA/pH3 images get the nuclei outlines, actin images get the cell outlines.
        """
        stem = os.path.splitext(os.path.basename(image_path))[0]
        wellidx, _, channel = stem.partition("-")
        outline_kind = self.CHANNEL_TO_OUTLINE.get(channel, "nuclei")
        target_name = f"{wellidx}-{outline_kind}.png"

        label_paths = self.get_label_paths()
        matches = [p for p in label_paths if os.path.basename(p) == target_name]

        if matches:
            return load_image(matches[0])

        # Fallback: any outline of this well (usually the nuclei outlines)
        matches = [
            p for p in label_paths if os.path.basename(p).startswith(f"{wellidx}-")
        ]
        if matches:
            return load_image(matches[0])

        raise FileNotFoundError(f"Outline mask not found for {image_path}")
