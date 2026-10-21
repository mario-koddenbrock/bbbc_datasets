import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset
from bbbc_datasets.metadata import DatasetMetadata


class Sartorius(BaseBBBCDataset):
    """
    Sartorius Dataset: TODO
    """

    METADATA = DatasetMetadata(
        name="Sartorius",
        title="Sartorius dataset",
        source="https://www.kaggle.com/competitions/sartorius-cell-instance-segmentation/data",
        dim="2D",
        imaging_mode="fluorescence",
        modality="grayscale",
        resolution_um=None,
        image_size=None,
        data_type="real",
        instrument=None,
        n_images=None,
        task="segmentation",
        label_type="instance",
        doi=None,
        license=None,
    )


def __init__(self, *args, **kwargs):

    # TODO https://www.kaggle.com/competitions/sartorius-cell-instance-segmentation/data

    self.KEY = "Sartorius"
    self.image_paths = [""]
    self.label_path = None
    self.metadata_paths = None
    self.is_3d = False

    super().__init__(*args, **kwargs)
