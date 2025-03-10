import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


class Sartorius(BaseBBBCDataset):
    """
    Sartorius Dataset: TODO
    """


def __init__(self, *args, **kwargs):

    # TODO https://www.kaggle.com/competitions/sartorius-cell-instance-segmentation/data

    self.local_path = os.path.join(self.download_dir, "Sartorius")
    self.image_paths = [
        "",
    ]
    self.label_path = None
    self.metadata_paths = None
    self.is_3d = False

    super().__init__("Cellpose", *args, **kwargs)
