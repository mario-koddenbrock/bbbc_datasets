import os

import numpy as np

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset
from bbbc_datasets.metadata import DatasetMetadata
from bbbc_datasets.utils.file_io import load_image


class BBBC020(BaseBBBCDataset):
    """
    BBBC020 Dataset: Murine bone-marrow derived macrophages (overlapping cells).

    - **Biological Application:**
      Bone-marrow derived macrophages from C57BL/6 mice, used to study the role of
      TLR4, Myd88 and MAPK in macrophage spreading. The irregular shape and heavy
      overlap of the cells make segmentation a challenging benchmark.

    - **Images:**
      25 time points, each with three 8-bit TIF channels: DAPI (c5, nuclei),
      CD11b/APC (c1, cell surface) and a merged (c1+c5) image.

    - **Segmentations:**
      One outline mask per cell: "<image_stem>_<channel>_<number>.TIF".
      Nuclei outlines are provided for the DAPI channel, cell outlines for the
      CD11b channel. get_label aggregates all per-cell outlines of an image into a
      single binary mask.

    - **Note:**
      BBBC reports that "BBBC020_v1_outlines_nuclei" appears incomplete. The archive
      actually contains at least one empty outline file (jw-15min 5_c5_43.TIF), so
      get_label skips unreadable outlines instead of failing.

    - **Source:** https://bbbc.broadinstitute.org/BBBC020
    """

    METADATA = DatasetMetadata(
        name="BBBC020",
        title="BBBC020 Dataset: Murine bone-marrow derived macrophages (overlapping cells).",
        source="https://bbbc.broadinstitute.org/BBBC020",
        dim="2D",
        imaging_mode="fluorescence",
        modality="multichannel",
        resolution_um=None,
        image_size=(1040, 1388),
        data_type="real",
        instrument=None,
        n_images=75,
        task="segmentation",
        label_type="instance",
        doi="10.1038/nmeth.2083",
        license="CC-BY-NC-SA-3.0",
    )

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC020"

    def __init__(self, *args, **kwargs):
        self.KEY = "BBBC020"
        self.image_paths = [
            os.path.join(self.BASE_URL, "BBBC020_v1_images.zip")
        ]
        self.label_path = [
            os.path.join(self.BASE_URL, "BBBC020_v1_outlines_nuclei.zip"),
            os.path.join(self.BASE_URL, "BBBC020_v1_outlines_cells.zip"),
        ]
        self.metadata_paths = None
        self.is_3d = False

        super().__init__(*args, **kwargs)

    def get_label(self, image_path):
        """
        Returns a binary mask with all per-cell outlines of the image aggregated.

        The merged "(c1+c5)" images receive the union of the cell and nucleus
        outlines; single-channel images receive the outlines of that channel.
        """
        stem = os.path.splitext(os.path.basename(image_path))[0]
        if "(c1+c5)" in stem:
            prefixes = [stem.replace("_(c1+c5)", "_c1"), stem.replace("_(c1+c5)", "_c5")]
        else:
            prefixes = [stem]

        label_paths = self.get_label_paths()
        mask = None
        skipped = []
        for prefix in prefixes:
            for path in label_paths:
                label_stem = os.path.splitext(os.path.basename(path))[0]
                if not label_stem.startswith(prefix + "_"):
                    continue
                if not label_stem[len(prefix) + 1 :].isdigit():
                    continue
                try:
                    outline = load_image(path)
                except Exception:
                    # Some outline files in the original archive are truncated
                    # or empty; skip them instead of failing the whole image.
                    skipped.append(path)
                    continue
                outline_mask = (np.asarray(outline) > 0).astype(np.uint8)
                mask = outline_mask if mask is None else np.maximum(mask, outline_mask)

        if skipped:
            print(
                f"Warning: skipped {len(skipped)} unreadable outline file(s) for "
                f"{os.path.basename(image_path)} (e.g. {os.path.basename(skipped[0])})"
            )

        if mask is None:
            return super().get_label(image_path)
        return mask
