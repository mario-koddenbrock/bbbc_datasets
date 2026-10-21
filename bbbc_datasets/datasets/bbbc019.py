import os
import zipfile

import requests
from tqdm import tqdm

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset
from bbbc_datasets.utils.file_io import load_image


class BBBC019(BaseBBBCDataset):
    """
    BBBC019 Dataset: Collective cell migration (wound healing, DIC images).

    - **Biological Application:**
      Wound-healing (scratch) assays imaged with DIC/phase-contrast microscopy, the
      gold standard for studying cell motility and migration. The task is to segment
      cell clusters in bright-field images across highly variable imaging conditions.

    - **Images:**
      165 DIC images partitioned into eight subsets (the BBBC page lists 171,
      but the current archives contain fewer Init images):
      TScratch (24), Melanoma (20), Init (22), SN15 (54), Scatter (6),
      Microfluidic (13), HEK293 (12), and MDCK (14).

    - **Segmentations:**
      One binary ground truth bitmap per input image (PNG, white = foreground),
      provided in the "manual" folder of each subset archive.

    - **Source:** https://bbbc.broadinstitute.org/BBBC019
    """

    BASE_URL = "https://data.broadinstitute.org/bbbc/BBBC019"

    SUBSETS = (
        "TScratch",
        "Melanoma",
        "Init",
        "SN15",
        "Scatter",
        "Microfluidic",
        "HEK293",
        "MDCK",
    )

    def __init__(self, subset=None, *args, **kwargs):
        """
        Initialize the dataset, optionally restricted to a single subset.

        :param subset: One of TScratch, Melanoma, Init, SN15, Scatter, Microfluidic,
                       HEK293, MDCK. If None, all subsets are downloaded.
        """
        if subset is not None and subset not in self.SUBSETS:
            raise ValueError(
                f"Invalid subset: {subset}. Choose from {list(self.SUBSETS)}"
            )

        self.subset = subset
        self.KEY = f"BBBC019_{subset}" if subset else "BBBC019"
        self.is_3d = False

        selected = (subset,) if subset else self.SUBSETS
        self.image_paths = [
            os.path.join(self.BASE_URL, f"{name}.zip") for name in selected
        ]
        self.label_path = None
        self.metadata_paths = None

        super().__init__(*args, **kwargs)

    def get_label(self, image_path):
        """
        Returns the binary ground truth mask for a given image path.

        Ground truth files are named "<image_stem>.png" or "<image_stem>_manual.png"
        inside the "manual" folder of each subset.
        """
        stem = os.path.splitext(os.path.basename(image_path))[0]
        label_paths = self.get_label_paths()
        for candidate in (f"{stem}.png", f"{stem}_manual.png"):
            matches = [p for p in label_paths if os.path.basename(p) == candidate]
            if matches:
                return load_image(matches[0])
        return super().get_label(image_path)

    def _download_files(self):
        """
        Downloads the subset archives and splits each one into images/ and labels/,
        discarding the algorithm-output folders (multiCellSeg, topman, ...).
        """
        os.makedirs(self.local_path, exist_ok=True)
        for url in self.image_paths:
            self._download_and_extract_subset(url)

    def _download_and_extract_subset(self, url):
        subset = os.path.basename(url)[:-4]
        images_dir = os.path.join(self.local_path, self.IMAGE_SUBDIR, subset)
        labels_dir = os.path.join(self.local_path, self.LABEL_SUBDIR, subset)
        marker = self._marker_path(url, "image")

        if os.path.exists(marker):
            return

        local_file = os.path.join(self.local_path, os.path.basename(url))
        if not os.path.exists(local_file):
            print(f"Downloading {local_file}...")
            response = requests.get(url, stream=True)
            if response.status_code != 200:
                raise FileNotFoundError(f"Failed to download {url}")
            total_size = int(response.headers.get("content-length", 0))
            with open(local_file, "wb") as f, tqdm(
                desc=local_file,
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))

        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(labels_dir, exist_ok=True)
        with zipfile.ZipFile(local_file, "r") as zip_ref:
            for member in zip_ref.namelist():
                parts = member.split("/")
                if len(parts) != 3 or parts[0] != subset:
                    continue
                folder, filename = parts[1], parts[2]
                if (
                    filename.startswith("._")
                    or filename in ("desktop.ini", ".DS_Store")
                ):
                    continue
                if folder == "images" and filename.lower().endswith(
                    (".jpg", ".jpeg", ".tif", ".tiff", ".png")
                ):
                    self._extract_member(zip_ref, member, os.path.join(images_dir, filename))
                elif folder == "manual" and filename.lower().endswith(".png"):
                    self._extract_member(zip_ref, member, os.path.join(labels_dir, filename))

        os.remove(local_file)
        os.makedirs(os.path.dirname(marker), exist_ok=True)
        with open(marker, "w") as f:
            f.write(url)

    @staticmethod
    def _extract_member(zip_ref, member, dest_path):
        with zip_ref.open(member) as src, open(dest_path, "wb") as dst:
            dst.write(src.read())
